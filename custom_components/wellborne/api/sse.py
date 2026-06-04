"""Server-Sent Events live-data listener for the Wellborne/ATESS cloud.

Holds ONE persistent connection to the vendor's eventSource stream and logs every raw
frame as a string at DEBUG. This is the capture stage: frames are NOT parsed into
entities yet — the goal is to record the real `{result,msg,obj}` envelopes pushed during
an actual charge so the parser can be built next.

CONNECTION SHAPE (matches the official app exactly): the app's bundled `event_source.html`
+ `eventsource.js` (the `event-source-polyfill` library) connect with::

    loadUrl = requestUrl + 'token=' + token + '&chargerId=' + chargerId
              + '&connectorId=' + connectorId + '&imea=' + deviceId
    new EventSourcePolyfill(loadUrl, { headers: {
        'Authorization': token, 'appVersion': ..., 'phoneModel': ...,
        'Accept-Language': ..., 'appOS': 'android' } })

So our request carries ``token``/``chargerId``/``connectorId``/``imea`` query params and a
RAW ``Authorization`` header (the login token, NOT ``Bearer ...``).

RECONNECT/HEARTBEAT (matches the polyfill defaults): heartbeatTimeout 45000ms (sock_read=45),
initialRetryDelayMillis 1000ms, exponential x2 capped at maxRetryDelayMillis 16000ms, reset to
1000ms on any received data. A server ``retry: <ms>`` line overrides the base delay (clamped),
and ``id:`` values are tracked and resent as ``Last-Event-ID`` on reconnect.

BAN SAFETY (the single deliberate deviation from the app): the app never self-throttles because
it holds one long-lived connection. We do — a ``Requesting too often`` frame triggers a hard
~120s backoff (``SSE_THROTTLE_BACKOFF``) before retrying.
"""

from __future__ import annotations

import asyncio
from dataclasses import dataclass
import json
import logging
import random
import time
from typing import TYPE_CHECKING, Any

import aiohttp

from ..const import API_BASE_URL, SSE_BACKOFF_BASE, SSE_BACKOFF_MAX, SSE_READ_TIMEOUT, SSE_THROTTLE_BACKOFF, Endpoints

if TYPE_CHECKING:
    from collections.abc import AsyncIterator

    from ..coordinator import WellborneDataUpdateCoordinator
    from .client import WellborneApiClient

_LOGGER = logging.getLogger(__name__)

# A frame `obj` whose status is >= this is "connected" (3 = connected/charging). The vendor's
# chargingStatus stays 0 even while delivering power, so status is the reliable connected flag.
_CONNECTED_STATUS = 3

# A "HH:MM:SS" duration string splits into exactly this many parts.
_HMS_PARTS = 3


def _to_float(value: Any) -> float | None:
    """Parse a vendor string/number to float, or None for null/garbage. Never raises."""
    if value is None:
        return None
    try:
        return float(value)
    except (TypeError, ValueError):
        return None


def _to_int(value: Any) -> int | None:
    """Parse a value to int, or None for null/garbage. Never raises."""
    if value is None:
        return None
    try:
        return int(value)
    except (TypeError, ValueError):
        return None


def _parse_duration_seconds(value: Any) -> int | None:
    """Parse a vendor ``charingTimeText`` "HH:MM:SS" into total seconds. None if malformed."""
    if not isinstance(value, str):
        return None
    parts = value.split(":")
    if len(parts) != _HMS_PARTS:
        return None
    try:
        hours, minutes, seconds = (int(p) for p in parts)
    except ValueError:
        return None
    return hours * 3600 + minutes * 60 + seconds


def _parse_cost(value: Any) -> tuple[float | None, str | None]:
    """Parse a vendor cost like "0.04€" into (amount, raw_text). Amount None if unparseable."""
    if value is None:
        return None, None
    text = str(value)
    # Strip everything that is not part of a number (currency symbols, spaces).
    numeric = "".join(ch for ch in text if ch.isdigit() or ch in ".-")
    return _to_float(numeric), text


@dataclass(frozen=True, slots=True)
class SseLiveSnapshot:
    """Immutable, null-safe view of one live SSE ``obj`` frame.

    All electrical values are parsed from the vendor's STRING fields into floats (or None when
    the charger reported null / garbage). Units: ``power_w`` in W (sum of the three per-phase kW
    fields * 1000), currents in A, voltages in V, ``energy_kwh`` is the session energy in kWh.
    ``duration_minutes``/``duration_seconds`` come from ``charingTimeText`` (vendor typo), NOT
    from any wall-clock subtraction.
    """

    power_w: float | None
    current_l1: float | None
    current_l2: float | None
    current_l3: float | None
    voltage_l1: float | None
    voltage_l2: float | None
    voltage_l3: float | None
    energy_kwh: float | None
    duration_seconds: int | None
    duration_minutes: int | None
    cost: float | None
    cost_text: str | None
    status: int | None
    connected: bool

    @classmethod
    def from_envelope_text(cls, line_text: str) -> SseLiveSnapshot | None:
        """Parse a full ``data: {...}`` SSE line into a snapshot, or None if it has no obj."""
        text = line_text
        if text.startswith("data:"):
            text = text[len("data:") :].strip()
        try:
            envelope = json.loads(text)
        except (ValueError, TypeError):
            return None
        if not isinstance(envelope, dict):
            return None
        return parse_sse_obj(envelope.get("obj"))


def parse_sse_obj(obj: Any) -> SseLiveSnapshot | None:
    """Parse a live frame ``obj`` dict into an :class:`SseLiveSnapshot`. None if not a dict.

    Defensive by design: every field is parsed independently and a null/garbage value yields
    None for that field (never an exception). ``power_w`` is the sum of the three per-phase kW
    fields converted to W; if ANY phase is missing/null it is reported as None rather than a
    partial sum.
    """
    if not isinstance(obj, dict):
        return None

    phases = [_to_float(obj.get(key)) for key in ("power", "powerL2", "powerL3")]
    power_w = round(sum(phases) * 1000, 2) if all(p is not None for p in phases) else None

    duration_seconds = _parse_duration_seconds(obj.get("charingTimeText"))
    duration_minutes = duration_seconds // 60 if duration_seconds is not None else None
    cost, cost_text = _parse_cost(obj.get("cost"))
    status = _to_int(obj.get("status"))

    return SseLiveSnapshot(
        power_w=power_w,
        current_l1=_to_float(obj.get("current")),
        current_l2=_to_float(obj.get("currentL2")),
        current_l3=_to_float(obj.get("currentL3")),
        voltage_l1=_to_float(obj.get("voltage")),
        voltage_l2=_to_float(obj.get("voltageL2")),
        voltage_l3=_to_float(obj.get("voltageL3")),
        energy_kwh=_to_float(obj.get("energyKWH")),
        duration_seconds=duration_seconds,
        duration_minutes=duration_minutes,
        cost=cost,
        cost_text=cost_text,
        status=status,
        connected=status is not None and status >= _CONNECTED_STATUS,
    )


# Substring that marks a throttle/rate-limit frame (triggers the hard backoff).
_THROTTLE_MARKER = "Requesting too often"

# HTTP status for a successfully opened stream.
HTTP_OK = 200

# Connector index the app always subscribes with.
DEFAULT_CONNECTOR_ID = "1"


class WellborneSseClient:
    """Single-connection SSE listener that logs raw live-data frames.

    Reuses the authenticated :class:`WellborneApiClient` (session + headers). The connection
    shape, heartbeat and reconnect policy mirror the official app's ``event-source-polyfill``.
    """

    def __init__(
        self,
        client: WellborneApiClient,
        charger_id: str,
        device_id: str,
        coordinator: WellborneDataUpdateCoordinator | None = None,
    ) -> None:
        """Initialize the listener.

        ``device_id`` is the ``imea`` query param the app derives from the phone (the server
        appears to just echo/log it). The caller passes a STABLE synthetic id for this HA
        install (e.g. ``f"ha-{entry.entry_id[:16]}"``) so it survives restarts.

        ``coordinator`` (optional) receives every parsed live snapshot via
        ``update_live_snapshot`` so the live sensors can read fresh values; the coordinator
        owns the entity-update throttle. When omitted the listener only logs raw frames.
        """
        self._client = client
        self._charger_id = charger_id
        self._device_id = device_id
        self._coordinator = coordinator
        self._monotonic = time.monotonic  # injectable clock for tests
        self._response: aiohttp.ClientResponse | None = None
        self._stopped = False
        self._connected_logged = False
        # Polyfill-style reconnect state.
        self._base_delay: float = SSE_BACKOFF_BASE  # current base (server `retry:` can override)
        self._last_event_id: str | None = None  # resent as `Last-Event-ID` on reconnect
        self._got_data = False  # data seen on the current connection -> reset failure count

    def _backoff_delay(self, attempt: int, *, throttled: bool) -> float:
        """Return the reconnect delay (seconds) with jitter.

        Normal drops: exponential from the current base (initially 1s, doubling) capped at 16s,
        mirroring the polyfill. A throttle forces a hard floor (>= 120s). Jitter is derived from
        ``random`` so concurrent reconnects do not align.
        """
        if throttled:
            base = SSE_THROTTLE_BACKOFF
        else:
            base = min(self._base_delay * (2 ** max(attempt - 1, 0)), SSE_BACKOFF_MAX)
        jitter = random.uniform(0, min(base * 0.1, 1.0))  # noqa: S311 - jitter, not crypto
        return base + jitter

    async def async_run(self) -> None:
        """Run the listener: open one connection, read frames, reconnect with backoff."""
        attempt = 0
        while not self._stopped:
            throttled = False
            try:
                throttled = await self._connect_and_read()
            except asyncio.CancelledError:
                raise
            except Exception as err:  # any failure -> backoff + retry (ban-safe)
                _LOGGER.info("WB-SSE disconnected (charger=%s): %s", self._charger_id, err)
            else:
                _LOGGER.info("WB-SSE disconnected (charger=%s): stream ended", self._charger_id)

            if self._stopped:
                break

            # A connection that actually delivered data is healthy: restart the failure
            # counter so the next reconnect begins at the polyfill base (1s), not the cap.
            if self._got_data and not throttled:
                attempt = 0
            self._got_data = False

            attempt += 1
            delay = self._backoff_delay(attempt, throttled=throttled)
            _LOGGER.debug(
                "WB-SSE reconnecting in %.1fs (attempt=%d, throttled=%s)",
                delay,
                attempt,
                throttled,
            )
            await asyncio.sleep(delay)

    def _build_request(self) -> tuple[str, dict[str, str], dict[str, str]]:
        """Build the (url, params, headers) for the SSE subscribe request.

        Matches the app: ``token``/``chargerId``/``connectorId``/``imea`` query params, a RAW
        ``Authorization`` header (login token, not ``Bearer ...``) plus the app headers, and
        ``Last-Event-ID`` when a prior ``id:`` was seen.
        """
        token = self._client._token or ""  # noqa: SLF001 - raw login token, by design
        url = f"{API_BASE_URL}{Endpoints.EVENT_SOURCE_SUBSCRIBE}"
        params = {
            "token": token,
            "chargerId": self._charger_id,
            "connectorId": DEFAULT_CONNECTOR_ID,
            "imea": self._device_id,
        }
        # Reuse the app headers, but override Authorization to the RAW token and add SSE Accept.
        headers = {
            **self._client._get_headers(),  # noqa: SLF001 - reuse appVersion/phoneModel/etc.
            "Authorization": token,
            "Accept": "text/event-stream",
        }
        if self._last_event_id is not None:
            headers["Last-Event-ID"] = self._last_event_id
        return url, params, headers

    async def _connect_and_read(self) -> bool:
        """Open the SSE stream and consume it. Return True if a throttle frame was seen."""
        session = await self._client._get_session()  # noqa: SLF001
        url, params, headers = self._build_request()
        timeout = aiohttp.ClientTimeout(total=None, sock_read=SSE_READ_TIMEOUT)

        async with session.get(url, params=params, headers=headers, timeout=timeout) as response:
            self._response = response
            if response.status != HTTP_OK:
                _LOGGER.info(
                    "WB-SSE non-200 status %s (charger=%s)",
                    response.status,
                    self._charger_id,
                )
                return False
            if not self._connected_logged:
                _LOGGER.info("WB-SSE connected (charger=%s)", self._charger_id)
                self._connected_logged = True
            try:
                return await self._consume_lines(response.content)
            finally:
                self._response = None

    async def _consume_lines(self, lines: AsyncIterator[bytes]) -> bool:
        """Log raw lines at DEBUG. Return True if a throttle frame was seen.

        Lines starting with ``:`` or blank are SSE heartbeats/keepalive: they are NOT logged
        as payload and do NOT count as a drop. ``id:`` and ``retry:`` lines update the reconnect
        state (Last-Event-ID / base delay). Any received data resets the backoff base to the
        polyfill initial (1s). A ``Requesting too often`` frame stops the read so the caller can
        apply the hard throttle backoff.
        """
        async for raw in lines:
            line_text = raw.decode("utf-8", errors="replace").rstrip("\r\n")
            if not line_text or line_text.startswith(":"):
                # Heartbeat / keepalive — connection is healthy, do not treat as a drop.
                continue
            # Any received line means a live connection: reset backoff to the polyfill initial
            # and mark the connection healthy so async_run restarts the failure counter.
            self._base_delay = SSE_BACKOFF_BASE
            self._got_data = True
            self._handle_field(line_text)
            _LOGGER.debug("WB-SSE raw: %s", line_text)
            if _THROTTLE_MARKER in line_text:
                _LOGGER.info("WB-SSE throttled (charger=%s): backing off hard", self._charger_id)
                return True
            self._dispatch_snapshot(line_text)
        return False

    def _dispatch_snapshot(self, line_text: str) -> None:
        """Parse a data frame into a live snapshot and hand it to the coordinator.

        Only ``data:`` envelopes carry live values. Parsing is null-safe and never raises; a
        frame with no parseable obj is ignored. The coordinator owns the entity-update throttle.
        """
        if self._coordinator is None or not line_text.startswith("data:"):
            return
        snapshot = SseLiveSnapshot.from_envelope_text(line_text)
        if snapshot is not None:
            self._coordinator.update_live_snapshot(snapshot)

    def _handle_field(self, line_text: str) -> None:
        """Track SSE ``id:`` and ``retry:`` fields like the polyfill does."""
        if line_text.startswith("id:"):
            self._last_event_id = line_text[len("id:") :].strip()
            return
        if line_text.startswith("retry:"):
            value = line_text[len("retry:") :].strip()
            try:
                retry_ms = int(value)
            except ValueError:
                return
            # Clamp to the sane polyfill range (1000-16000 ms) before adopting as the base.
            clamped_ms = max(SSE_BACKOFF_BASE * 1000, min(retry_ms, SSE_BACKOFF_MAX * 1000))
            self._base_delay = clamped_ms / 1000

    async def async_stop(self) -> None:
        """Stop the listener and close any open response."""
        self._stopped = True
        if self._response is not None and not self._response.closed:
            self._response.close()
        self._response = None
