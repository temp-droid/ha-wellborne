"""Tests for the Wellborne SSE live-data listener.

No real network: the SSE reader is fed a fake async byte-line stream and the backoff
policy is asserted directly. The connection shape (params/headers matching the official
app) and the single-connection / ban-safe backoff property are the most important things
under test.
"""

from __future__ import annotations

import asyncio
import json
import logging
import random
from typing import TYPE_CHECKING
from unittest.mock import AsyncMock, MagicMock

import pytest

from custom_components.wellborne.api.sse import SseLiveSnapshot, WellborneSseClient, parse_sse_obj
from custom_components.wellborne.const import (
    API_BASE_URL,
    SSE_BACKOFF_BASE,
    SSE_BACKOFF_MAX,
    SSE_PUSH_THROTTLE,
    SSE_THROTTLE_BACKOFF,
    Endpoints,
)
from custom_components.wellborne.coordinator.coordinator import WellborneDataUpdateCoordinator

from ..conftest import TEST_CHARGER_ID

if TYPE_CHECKING:
    from collections.abc import AsyncIterator

TEST_DEVICE_ID = "ha-0123456789abcdef"
TEST_TOKEN = "raw-login-token-xyz"  # noqa: S105 - test fixture, not a real secret

# Ground-truth charging frame `obj` captured from the real charger (values are STRINGS).
CHARGING_OBJ = {
    "status": 3,
    "chargingStatus": 0,
    "power": "2.27",
    "powerL2": "2.24",
    "powerL3": "2.22",
    "current": "10.11",
    "currentL2": "9.98",
    "currentL3": "9.68",
    "voltage": "224.60",
    "voltageL2": "224.30",
    "voltageL3": "230.10",
    "energyKWH": "0.10",
    "charingTimeText": "00:01:38",
    "cost": "0.04€",
    "chargerId": "OHG0C19125",
    "connectorId": 1,
    "phase": "3",
}

# Ground-truth idle frame `obj`: numeric fields are null, status is 2.
IDLE_OBJ = {
    "status": 2,
    "chargingStatus": 0,
    "power": None,
    "powerL2": None,
    "powerL3": None,
    "current": None,
    "currentL2": None,
    "currentL3": None,
    "voltage": None,
    "voltageL2": None,
    "voltageL3": None,
    "energyKWH": None,
    "charingTimeText": None,
    "cost": None,
    "chargerId": "OHG0C19125",
    "connectorId": 1,
    "phase": "3",
}


async def _aiter_lines(lines: list[bytes]) -> AsyncIterator[bytes]:
    """Yield byte lines like an aiohttp StreamReader does."""
    for line in lines:
        yield line


@pytest.fixture
def sse_client() -> WellborneSseClient:
    """Create an SSE client backed by a mock API client with a raw token + app headers."""
    client = MagicMock()
    client._token = TEST_TOKEN
    client._get_headers.return_value = {
        "Content-Type": "application/json; charset=UTF-8",
        "Accept-Language": "en-US",
        "phoneModel": "HomeAssistant",
        "appVersion": "1.0.4",
        "appOS": "android",
        "User-Agent": "okhttp/4.8.0",
        "Authorization": f"Bearer {TEST_TOKEN}",  # _get_headers adds Bearer; we must override it
    }
    return WellborneSseClient(client, TEST_CHARGER_ID, TEST_DEVICE_ID)


@pytest.mark.unit
def test_build_request_matches_app_shape(sse_client: WellborneSseClient) -> None:
    """Request carries token/chargerId/connectorId=1/imea params and a RAW Authorization."""
    url, params, headers = sse_client._build_request()

    assert url == f"{API_BASE_URL}{Endpoints.EVENT_SOURCE_SUBSCRIBE}"
    # Query params replace the old userId approach entirely.
    assert params == {
        "token": TEST_TOKEN,
        "chargerId": TEST_CHARGER_ID,
        "connectorId": "1",
        "imea": TEST_DEVICE_ID,
    }
    assert "userId" not in params
    # Authorization is the RAW token (NOT "Bearer ..."), matching the app.
    assert headers["Authorization"] == TEST_TOKEN
    assert headers["Accept"] == "text/event-stream"
    # App headers are reused from _get_headers().
    assert headers["appVersion"] == "1.0.4"
    assert headers["phoneModel"] == "HomeAssistant"
    assert headers["appOS"] == "android"
    assert headers["Accept-Language"] == "en-US"
    # No Last-Event-ID until an `id:` line has been seen.
    assert "Last-Event-ID" not in headers


@pytest.mark.unit
async def test_consume_lines_logs_raw_data_frames_at_debug(
    sse_client: WellborneSseClient,
    caplog: pytest.LogCaptureFixture,
) -> None:
    """Every non-heartbeat line is logged RAW at DEBUG; payloads are not parsed."""
    payload = b'data: {"result":0,"msg":"ok","obj":{"power":3680}}'
    lines = [
        payload,
        b":",  # heartbeat
        b"",  # blank keepalive
        b'data: {"result":0,"obj":{"energy":1.2}}',
    ]

    with caplog.at_level(logging.DEBUG, logger="custom_components.wellborne.api.sse"):
        throttled = await sse_client._consume_lines(_aiter_lines(lines))

    assert throttled is False
    raw_logs = [r.getMessage() for r in caplog.records if "WB-SSE raw:" in r.getMessage()]
    # Both data frames logged raw; heartbeat/blank lines NOT logged as payload.
    assert any('"power":3680' in m for m in raw_logs)
    assert any('"energy":1.2' in m for m in raw_logs)
    assert len(raw_logs) == 2


@pytest.mark.unit
async def test_consume_lines_throttle_frame_returns_true(
    sse_client: WellborneSseClient,
) -> None:
    """A 'Requesting too often' frame stops the read and signals the hard backoff."""
    lines = [
        b'data: {"result":0,"obj":{}}',
        b'data: {"result":500,"msg":"Requesting too often, please try later"}',
        b'data: {"result":0,"obj":{"never":"read"}}',
    ]
    throttled = await sse_client._consume_lines(_aiter_lines(lines))
    assert throttled is True


@pytest.mark.unit
def test_normal_drop_uses_exponential_backoff(sse_client: WellborneSseClient) -> None:
    """Normal-drop backoff mirrors the polyfill: 1 -> 2 -> 4 -> 8 -> 16s, capped at 16s."""
    random.seed(0)  # deterministic jitter
    # base: attempt 1 -> 1, 2 -> 2, 3 -> 4, 4 -> 8, 5 -> 16 (cap), 6 -> 16 (cap)
    d1 = sse_client._backoff_delay(1, throttled=False)
    d2 = sse_client._backoff_delay(2, throttled=False)
    d3 = sse_client._backoff_delay(3, throttled=False)
    d4 = sse_client._backoff_delay(4, throttled=False)
    d5 = sse_client._backoff_delay(5, throttled=False)
    d6 = sse_client._backoff_delay(6, throttled=False)

    # Each delay is base + jitter in [0, min(base*0.1, 1.0)]: doubling, then capped at 16s.
    assert SSE_BACKOFF_BASE <= d1 <= SSE_BACKOFF_BASE + 1.0
    assert 2 <= d2 <= 3
    assert 4 <= d3 <= 5
    assert 8 <= d4 <= 9
    assert SSE_BACKOFF_MAX <= d5 <= SSE_BACKOFF_MAX + 1.0
    assert SSE_BACKOFF_MAX <= d6 <= SSE_BACKOFF_MAX + 1.0


@pytest.mark.unit
async def test_received_data_resets_backoff(sse_client: WellborneSseClient) -> None:
    """Any received data resets the backoff base to the polyfill initial (1s)."""
    # Simulate an earlier server `retry:` having bumped the base up.
    sse_client._base_delay = SSE_BACKOFF_MAX
    await sse_client._consume_lines(_aiter_lines([b'data: {"result":0}']))
    assert sse_client._base_delay == SSE_BACKOFF_BASE


@pytest.mark.unit
async def test_retry_field_updates_base_delay(sse_client: WellborneSseClient) -> None:
    """A `retry: N` line sets the base reconnect delay (clamped to 1000-16000 ms)."""
    await sse_client._consume_lines(_aiter_lines([b"retry: 5000"]))
    assert sse_client._base_delay == 5.0

    # Below the floor clamps up to 1s; above the ceiling clamps down to 16s.
    await sse_client._consume_lines(_aiter_lines([b"retry: 100"]))
    assert sse_client._base_delay == SSE_BACKOFF_BASE
    await sse_client._consume_lines(_aiter_lines([b"retry: 999999"]))
    assert sse_client._base_delay == SSE_BACKOFF_MAX


@pytest.mark.unit
async def test_id_field_resent_as_last_event_id(sse_client: WellborneSseClient) -> None:
    """An `id:` line is tracked and resent as the `Last-Event-ID` header on reconnect."""
    assert "Last-Event-ID" not in sse_client._build_request()[2]

    await sse_client._consume_lines(_aiter_lines([b"id: 42", b'data: {"result":0}']))

    assert sse_client._last_event_id == "42"
    headers = sse_client._build_request()[2]
    assert headers["Last-Event-ID"] == "42"


@pytest.mark.unit
def test_throttle_uses_long_backoff(sse_client: WellborneSseClient) -> None:
    """A throttle forces a hard backoff of at least 120s regardless of attempt index."""
    d = sse_client._backoff_delay(1, throttled=True)
    assert d >= SSE_THROTTLE_BACKOFF


@pytest.mark.unit
async def test_async_run_stops_cleanly_on_cancellation(
    sse_client: WellborneSseClient,
) -> None:
    """Cancelling the run task stops the loop cleanly (no swallowed CancelledError)."""

    # Make the connect step block so the task is parked inside async_run when cancelled.
    async def _never() -> bool:
        await asyncio.Event().wait()
        return False

    sse_client._connect_and_read = AsyncMock(side_effect=_never)

    task = asyncio.create_task(sse_client.async_run())
    await asyncio.sleep(0)  # let it enter the loop
    task.cancel()

    with pytest.raises(asyncio.CancelledError):
        await task


@pytest.mark.unit
async def test_async_run_throttle_then_stop_does_not_reconnect(
    sse_client: WellborneSseClient,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """After a throttle frame the loop applies the LONG backoff, then stops without reconnecting."""
    slept: list[float] = []

    async def _fake_sleep(delay: float) -> None:
        slept.append(delay)
        # Stop after the first (throttle) backoff so the loop exits instead of reconnecting.
        await sse_client.async_stop()

    monkeypatch.setattr("custom_components.wellborne.api.sse.asyncio.sleep", _fake_sleep)
    sse_client._connect_and_read = AsyncMock(return_value=True)  # throttle seen

    await sse_client.async_run()

    # Exactly one backoff happened and it was the hard throttle floor.
    assert len(slept) == 1
    assert slept[0] >= SSE_THROTTLE_BACKOFF
    # Only one connection attempt — never reconnected after the throttle.
    assert sse_client._connect_and_read.await_count == 1


# =============================================================================
# Live snapshot parsing
# =============================================================================


@pytest.mark.unit
def test_parse_charging_obj() -> None:
    """A charging `obj` parses to floats with correct units and duration/cost."""
    snap = parse_sse_obj(CHARGING_OBJ)

    assert snap is not None
    # power_w = (2.27 + 2.24 + 2.22) kW * 1000 = 6730 W
    assert snap.power_w == pytest.approx(6730.0)
    assert snap.current_l1 == pytest.approx(10.11)
    assert snap.current_l2 == pytest.approx(9.98)
    assert snap.current_l3 == pytest.approx(9.68)
    assert snap.voltage_l1 == pytest.approx(224.60)
    assert snap.voltage_l2 == pytest.approx(224.30)
    assert snap.voltage_l3 == pytest.approx(230.10)
    assert snap.energy_kwh == pytest.approx(0.10)
    # "00:01:38" = 1 min 38 s = 98 total seconds -> 1 whole minute.
    assert snap.duration_seconds == 98
    assert snap.duration_minutes == 1
    assert snap.cost == pytest.approx(0.04)
    assert snap.cost_text == "0.04€"
    assert snap.status == 3
    assert snap.connected is True


@pytest.mark.unit
def test_parse_idle_obj_all_none() -> None:
    """An idle `obj` (nulls, status 2) parses to all-None live values, not charging."""
    snap = parse_sse_obj(IDLE_OBJ)

    assert snap is not None
    assert snap.power_w is None
    assert snap.current_l1 is None
    assert snap.current_l2 is None
    assert snap.current_l3 is None
    assert snap.voltage_l1 is None
    assert snap.voltage_l2 is None
    assert snap.voltage_l3 is None
    assert snap.energy_kwh is None
    assert snap.duration_minutes is None
    assert snap.duration_seconds is None
    assert snap.cost is None
    assert snap.status == 2
    assert snap.connected is False


@pytest.mark.unit
def test_parse_malformed_values_never_raise() -> None:
    """Garbage / partial fields parse to None per-field without raising."""
    obj = {
        "status": "not-an-int",
        "power": "abc",
        "powerL2": "2.0",
        "powerL3": None,
        "current": "",
        "voltage": "garbage",
        "energyKWH": "NaNN",
        "charingTimeText": "1:2",  # malformed (not HH:MM:SS)
        "cost": "free",
    }
    snap = parse_sse_obj(obj)

    assert snap is not None
    # Any null/garbage phase makes the total power None (we don't report a partial sum).
    assert snap.power_w is None
    assert snap.current_l1 is None
    assert snap.voltage_l1 is None
    assert snap.energy_kwh is None
    assert snap.duration_minutes is None
    assert snap.cost is None
    # status was garbage -> None -> not connected.
    assert snap.status is None
    assert snap.connected is False


@pytest.mark.unit
def test_parse_non_dict_returns_none() -> None:
    """A non-dict obj (None / list / str) returns None, never raises."""
    assert parse_sse_obj(None) is None
    assert parse_sse_obj([]) is None
    assert parse_sse_obj("nope") is None


@pytest.mark.unit
def test_parse_data_frame_extracts_obj() -> None:
    """`parse_sse_obj` accepts the full data envelope text and pulls obj out."""
    envelope = {"result": 0, "msg": "ok", "obj": CHARGING_OBJ}
    snap = SseLiveSnapshot.from_envelope_text(f"data: {json.dumps(envelope)}")
    assert snap is not None
    assert snap.power_w == pytest.approx(6730.0)
    assert snap.connected is True


# =============================================================================
# Throttled push into the coordinator
# =============================================================================


@pytest.mark.unit
async def test_frames_pushed_to_coordinator_throttled(
    sse_client: WellborneSseClient,
) -> None:
    """Many frames within the throttle window notify the coordinator at most once.

    Every parsed frame stores the latest snapshot, but the entity-update push is throttled
    to once per SSE_PUSH_THROTTLE seconds using an injected monotonic clock.
    """
    now = 1000.0

    def _clock() -> float:
        return now

    coordinator = MagicMock()
    coordinator.update_live_snapshot = MagicMock()
    sse_client._coordinator = coordinator
    sse_client._monotonic = _clock

    # Three data frames back-to-back at the SAME clock instant.
    frame = f'data: {{"result":0,"obj":{json.dumps(CHARGING_OBJ)}}}'
    await sse_client._consume_lines(_aiter_lines([frame.encode(), frame.encode(), frame.encode()]))

    # Coordinator is told about every frame (it does its own throttling of listener notifies).
    assert coordinator.update_live_snapshot.call_count == 3
    # And each call carried a parsed snapshot.
    snap = coordinator.update_live_snapshot.call_args.args[0]
    assert isinstance(snap, SseLiveSnapshot)
    assert snap.power_w == pytest.approx(6730.0)


@pytest.mark.unit
def test_coordinator_notify_throttled(monkeypatch: pytest.MonkeyPatch) -> None:
    """Coordinator stores every snapshot but notifies listeners at most once per window."""
    clock = {"t": 100.0}
    coordinator = MagicMock(spec=WellborneDataUpdateCoordinator)
    # Bind the REAL methods/state to the mock so we exercise the throttle logic directly.
    coordinator._live_snapshot = None
    coordinator._live_snapshot_at = None
    coordinator._live_pushed_at = None
    coordinator.async_update_listeners = MagicMock()
    coordinator._live_monotonic = lambda: clock["t"]

    update = WellborneDataUpdateCoordinator.update_live_snapshot

    snap = parse_sse_obj(CHARGING_OBJ)

    # First push notifies.
    update(coordinator, snap)
    assert coordinator.async_update_listeners.call_count == 1

    # Second push <4s later: stored but does NOT notify.
    clock["t"] += SSE_PUSH_THROTTLE - 0.1
    update(coordinator, snap)
    assert coordinator.async_update_listeners.call_count == 1

    # Third push after the window: notifies again.
    clock["t"] += SSE_PUSH_THROTTLE
    update(coordinator, snap)
    assert coordinator.async_update_listeners.call_count == 2

    # Latest snapshot is always stored.
    assert coordinator._live_snapshot is snap
