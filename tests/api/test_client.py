"""Tests for the Wellborne API client."""

from __future__ import annotations

from typing import Any

from aiohttp import ClientConnectionError
from aioresponses import aioresponses
import pytest
from yarl import URL

from custom_components.wellborne.api import (
    ApiConnectionError,
    ApiResponseError,
    AuthenticationError,
    SessionExpiredError,
    WellborneApiClient,
)
from custom_components.wellborne.api.client import _redact_sensitive
from custom_components.wellborne.const import API_BASE_URL, Endpoints

from ..conftest import TEST_CHARGER_ID, TEST_EMAIL, TEST_PASSWORD


class TestWellborneApiClient:
    """Test cases for WellborneApiClient."""

    @pytest.fixture
    def client(self) -> WellborneApiClient:
        """Create a client instance for testing."""
        return WellborneApiClient(email=TEST_EMAIL)

    @pytest.mark.unit
    async def test_init(self, client: WellborneApiClient) -> None:
        """Test client initialization."""
        assert client._email == TEST_EMAIL
        assert client._token is None
        assert not client.is_authenticated

    @pytest.mark.unit
    async def test_password_hashing(self) -> None:
        """Test password is hashed with MD5."""
        password = "test_password"  # noqa: S105
        hashed = WellborneApiClient._hash_password(password)

        # MD5 hash should be 32 hex characters
        assert len(hashed) == 32
        assert all(c in "0123456789abcdef" for c in hashed)

        # Same input should produce same output
        assert WellborneApiClient._hash_password(password) == hashed

    @pytest.mark.unit
    async def test_login_success(
        self,
        client: WellborneApiClient,
        api_login_response: dict[str, Any],
    ) -> None:
        """Test successful login."""
        with aioresponses() as mocked:
            mocked.post(
                f"{API_BASE_URL}{Endpoints.LOGIN}",
                payload=api_login_response,
            )

            result = await client.async_login(TEST_PASSWORD)

            assert client.is_authenticated
            assert client._token is not None
            assert result["email"] == TEST_EMAIL

        await client.close()

    @pytest.mark.unit
    async def test_login_invalid_credentials(
        self,
        client: WellborneApiClient,
        api_auth_error_response: dict[str, Any],
    ) -> None:
        """Test login with invalid credentials."""
        with aioresponses() as mocked:
            mocked.post(
                f"{API_BASE_URL}{Endpoints.LOGIN}",
                payload=api_auth_error_response,
            )

            with pytest.raises(AuthenticationError, match="Login failed"):
                await client.async_login("wrong_password")

            assert not client.is_authenticated

        await client.close()

    @pytest.mark.unit
    async def test_login_connection_error(
        self,
        client: WellborneApiClient,
    ) -> None:
        """Test login with connection error."""
        with aioresponses() as mocked:
            mocked.post(
                f"{API_BASE_URL}{Endpoints.LOGIN}",
                exception=ClientConnectionError("Network error"),
            )

            with pytest.raises(ApiConnectionError):
                await client.async_login(TEST_PASSWORD)

        await client.close()

    @pytest.mark.unit
    async def test_get_chargers(
        self,
        client: WellborneApiClient,
        api_login_response: dict[str, Any],
        api_charger_list_response: dict[str, Any],
    ) -> None:
        """Test getting charger list."""
        with aioresponses() as mocked:
            # Login first
            mocked.post(
                f"{API_BASE_URL}{Endpoints.LOGIN}",
                payload=api_login_response,
            )
            mocked.post(
                f"{API_BASE_URL}{Endpoints.CHARGER_LIST}",
                payload=api_charger_list_response,
            )

            await client.async_login(TEST_PASSWORD)
            chargers = await client.async_get_chargers()

            assert len(chargers) == 1
            assert chargers[0].charger_id == TEST_CHARGER_ID
            assert chargers[0].alias == "Test Charger"
            assert chargers[0].max_power == 22

        await client.close()

    @pytest.mark.unit
    async def test_is_charging(
        self,
        client: WellborneApiClient,
        api_login_response: dict[str, Any],
        api_is_charging_response: dict[str, Any],
    ) -> None:
        """Test checking charging status."""
        with aioresponses() as mocked:
            mocked.post(
                f"{API_BASE_URL}{Endpoints.LOGIN}",
                payload=api_login_response,
            )
            mocked.post(
                f"{API_BASE_URL}{Endpoints.IS_CHARGING}",
                payload=api_is_charging_response,
            )

            await client.async_login(TEST_PASSWORD)
            is_charging = await client.async_is_charging(TEST_CHARGER_ID)

            assert is_charging is False

        await client.close()

    @pytest.mark.unit
    async def test_is_charging_when_active(
        self,
        client: WellborneApiClient,
        api_login_response: dict[str, Any],
    ) -> None:
        """Test checking charging status when charging is active."""
        response = {"result": 0, "msg": "success", "obj": True}

        with aioresponses() as mocked:
            mocked.post(
                f"{API_BASE_URL}{Endpoints.LOGIN}",
                payload=api_login_response,
            )
            mocked.post(
                f"{API_BASE_URL}{Endpoints.IS_CHARGING}",
                payload=response,
            )

            await client.async_login(TEST_PASSWORD)
            is_charging = await client.async_is_charging(TEST_CHARGER_ID)

            assert is_charging is True

        await client.close()

    @pytest.mark.unit
    async def test_start_charging(
        self,
        client: WellborneApiClient,
        api_login_response: dict[str, Any],
    ) -> None:
        """Test starting a charging session."""
        response = {"result": 0, "msg": "success", "obj": None}

        with aioresponses() as mocked:
            mocked.post(
                f"{API_BASE_URL}{Endpoints.LOGIN}",
                payload=api_login_response,
            )
            mocked.post(
                f"{API_BASE_URL}{Endpoints.REMOTE_START}",
                payload=response,
            )

            await client.async_login(TEST_PASSWORD)
            # Should not raise
            await client.async_start_charging(TEST_CHARGER_ID)

        await client.close()

    @pytest.mark.unit
    async def test_stop_charging(
        self,
        client: WellborneApiClient,
        api_login_response: dict[str, Any],
    ) -> None:
        """Test stopping a charging session."""
        response = {"result": 0, "msg": "success", "obj": None}

        with aioresponses() as mocked:
            mocked.post(
                f"{API_BASE_URL}{Endpoints.LOGIN}",
                payload=api_login_response,
            )
            mocked.post(
                f"{API_BASE_URL}{Endpoints.REMOTE_STOP}",
                payload=response,
            )

            await client.async_login(TEST_PASSWORD)
            # Should not raise
            await client.async_stop_charging(TEST_CHARGER_ID)

        await client.close()

    @pytest.mark.unit
    async def test_set_max_current(
        self,
        client: WellborneApiClient,
        api_login_response: dict[str, Any],
    ) -> None:
        """Test setting maximum current."""
        response = {"result": 0, "msg": "success", "obj": None}

        with aioresponses() as mocked:
            mocked.post(
                f"{API_BASE_URL}{Endpoints.LOGIN}",
                payload=api_login_response,
            )
            mocked.post(
                f"{API_BASE_URL}{Endpoints.UPDATE_MAX_CURRENT}",
                payload=response,
            )

            await client.async_login(TEST_PASSWORD)
            await client.async_set_max_current(TEST_CHARGER_ID, 16)

        await client.close()

    @pytest.mark.unit
    async def test_set_solar_mode(
        self,
        client: WellborneApiClient,
        api_login_response: dict[str, Any],
    ) -> None:
        """Test setting solar charging mode."""
        response = {"result": 0, "msg": "success", "obj": None}

        with aioresponses() as mocked:
            mocked.post(
                f"{API_BASE_URL}{Endpoints.LOGIN}",
                payload=api_login_response,
            )
            mocked.post(
                f"{API_BASE_URL}{Endpoints.SAVE_SOLAR_MODE}",
                payload=response,
            )

            await client.async_login(TEST_PASSWORD)
            await client.async_set_solar_mode(TEST_CHARGER_ID, "1")

        await client.close()

    @pytest.mark.unit
    async def test_session_expired_triggers_error(
        self,
        client: WellborneApiClient,
        api_login_response: dict[str, Any],
        api_session_expired_response: dict[str, Any],
    ) -> None:
        """Test that session expiration raises SessionExpiredError."""
        with aioresponses() as mocked:
            mocked.post(
                f"{API_BASE_URL}{Endpoints.LOGIN}",
                payload=api_login_response,
            )
            mocked.post(
                f"{API_BASE_URL}{Endpoints.CHARGER_LIST}",
                payload=api_session_expired_response,
            )

            await client.async_login(TEST_PASSWORD)

            with pytest.raises(SessionExpiredError):
                await client.async_get_chargers()

        await client.close()

    @pytest.mark.unit
    async def test_api_error_response(
        self,
        client: WellborneApiClient,
        api_login_response: dict[str, Any],
        api_error_response: dict[str, Any],
    ) -> None:
        """Test handling of API error responses."""
        with aioresponses() as mocked:
            mocked.post(
                f"{API_BASE_URL}{Endpoints.LOGIN}",
                payload=api_login_response,
            )
            mocked.post(
                f"{API_BASE_URL}{Endpoints.CHARGER_LIST}",
                payload=api_error_response,
            )

            await client.async_login(TEST_PASSWORD)

            with pytest.raises(ApiResponseError, match="Operation failed"):
                await client.async_get_chargers()

        await client.close()

    @pytest.mark.unit
    async def test_get_charger_config(
        self,
        client: WellborneApiClient,
        api_login_response: dict[str, Any],
        api_charger_config_response: dict[str, Any],
    ) -> None:
        """Test getting charger configuration."""
        with aioresponses() as mocked:
            mocked.post(
                f"{API_BASE_URL}{Endpoints.LOGIN}",
                payload=api_login_response,
            )
            mocked.post(
                f"{API_BASE_URL}{Endpoints.GET_CHARGER_CONFIG}",
                payload=api_charger_config_response,
            )

            await client.async_login(TEST_PASSWORD)
            config = await client.async_get_charger_config(TEST_CHARGER_ID)

            assert config["maximumOutputCurrent"] == "16.00"
            assert config["connectorLock"] == "true"

        await client.close()

    @pytest.mark.unit
    async def test_get_home_config(
        self,
        client: WellborneApiClient,
        api_login_response: dict[str, Any],
        api_home_config_response: dict[str, Any],
    ) -> None:
        """Test getting home configuration."""
        with aioresponses() as mocked:
            mocked.post(
                f"{API_BASE_URL}{Endpoints.LOGIN}",
                payload=api_login_response,
            )
            mocked.post(
                f"{API_BASE_URL}{Endpoints.GET_HOME_CONFIG}",
                payload=api_home_config_response,
            )

            await client.async_login(TEST_PASSWORD)
            config = await client.async_get_home_config(TEST_CHARGER_ID)

            assert config["solarChargingMode"] == "0"
            assert config["delayedCharging"]["status"] == 2

        await client.close()

    @pytest.mark.unit
    async def test_logout(
        self,
        client: WellborneApiClient,
        api_login_response: dict[str, Any],
    ) -> None:
        """Test logout clears token."""
        logout_response = {"result": 0, "msg": "success", "obj": None}

        with aioresponses() as mocked:
            mocked.post(
                f"{API_BASE_URL}{Endpoints.LOGIN}",
                payload=api_login_response,
            )
            mocked.post(
                f"{API_BASE_URL}{Endpoints.LOGOUT}",
                payload=logout_response,
            )

            await client.async_login(TEST_PASSWORD)
            assert client.is_authenticated

            await client.async_logout()
            assert not client.is_authenticated
            assert client._token is None

        await client.close()

    @pytest.mark.unit
    async def test_headers_include_auth_token(
        self,
        client: WellborneApiClient,
        api_login_response: dict[str, Any],
    ) -> None:
        """Test that authenticated requests include the auth token."""
        with aioresponses() as mocked:
            mocked.post(
                f"{API_BASE_URL}{Endpoints.LOGIN}",
                payload=api_login_response,
            )

            await client.async_login(TEST_PASSWORD)

            headers = client._get_headers(with_auth=True)
            assert "Authorization" in headers
            assert headers["Authorization"].startswith("Bearer ")

        await client.close()

    @pytest.mark.unit
    async def test_headers_without_auth(
        self,
        client: WellborneApiClient,
    ) -> None:
        """Test headers without authentication."""
        headers = client._get_headers(with_auth=False)
        assert "Authorization" not in headers
        assert headers["Content-Type"] == "application/json; charset=UTF-8"

    @pytest.mark.unit
    async def test_close_session(
        self,
        client: WellborneApiClient,
        api_login_response: dict[str, Any],
    ) -> None:
        """Test closing the client session."""
        with aioresponses() as mocked:
            mocked.post(
                f"{API_BASE_URL}{Endpoints.LOGIN}",
                payload=api_login_response,
            )

            await client.async_login(TEST_PASSWORD)

        # Should not raise
        await client.close()

    @pytest.mark.unit
    async def test_unlock_connector(
        self,
        client: WellborneApiClient,
        api_login_response: dict[str, Any],
    ) -> None:
        """Test unlocking the connector."""
        response = {"result": 0, "msg": "success", "obj": None}

        with aioresponses() as mocked:
            mocked.post(
                f"{API_BASE_URL}{Endpoints.LOGIN}",
                payload=api_login_response,
            )
            mocked.post(
                f"{API_BASE_URL}{Endpoints.UNLOCK_CONNECTOR}",
                payload=response,
            )

            await client.async_login(TEST_PASSWORD)
            await client.async_unlock_connector(TEST_CHARGER_ID)

        await client.close()

    @pytest.mark.unit
    async def test_prompt_charge(
        self,
        client: WellborneApiClient,
        api_login_response: dict[str, Any],
    ) -> None:
        """Test immediate charge (bypass delay)."""
        response = {"result": 0, "msg": "success", "obj": None}

        with aioresponses() as mocked:
            mocked.post(
                f"{API_BASE_URL}{Endpoints.LOGIN}",
                payload=api_login_response,
            )
            mocked.post(
                f"{API_BASE_URL}{Endpoints.PROMPT_CHARGE}",
                payload=response,
            )

            await client.async_login(TEST_PASSWORD)
            await client.async_prompt_charge(TEST_CHARGER_ID)

        await client.close()

    @pytest.mark.unit
    async def test_set_connector_lock(
        self,
        client: WellborneApiClient,
        api_login_response: dict[str, Any],
    ) -> None:
        """Test enabling/disabling connector lock."""
        response = {"result": 0, "msg": "success", "obj": None}

        with aioresponses() as mocked:
            mocked.post(
                f"{API_BASE_URL}{Endpoints.LOGIN}",
                payload=api_login_response,
            )
            mocked.post(
                f"{API_BASE_URL}{Endpoints.UPDATE_CONNECTOR_LOCK}",
                payload=response,
            )

            await client.async_login(TEST_PASSWORD)
            await client.async_set_connector_lock(TEST_CHARGER_ID, enabled=True)

        await client.close()

    @pytest.mark.unit
    async def test_connector_lock_switch_uses_config_endpoint_not_unlock_action(
        self,
        client: WellborneApiClient,
        api_login_response: dict[str, Any],
    ) -> None:
        """Regression: connector_lock switch (persistent config) and unlock_connector button (momentary action) use distinct endpoints.

        async_set_connector_lock -> Endpoints.UPDATE_CONNECTOR_LOCK (/getConfiguration/updateConnectorLock)
        async_unlock_connector   -> Endpoints.UNLOCK_CONNECTOR       (/charger/unlockConnector)

        The two must never be confused: set_connector_lock carries a "value" flag and persists
        state; unlock_connector is a one-shot latch release with no flag.
        """
        response = {"result": 0, "msg": "success", "obj": None}

        # --- Part 1: set_connector_lock(enabled=False) hits UPDATE_CONNECTOR_LOCK ---
        # Only UPDATE_CONNECTOR_LOCK is registered; hitting UNLOCK_CONNECTOR would
        # raise ConnectionError (unregistered URL), making the wrong-endpoint bug visible.
        with aioresponses() as mocked:
            mocked.post(f"{API_BASE_URL}{Endpoints.LOGIN}", payload=api_login_response)
            mocked.post(f"{API_BASE_URL}{Endpoints.UPDATE_CONNECTOR_LOCK}", payload=response)

            await client.async_login(TEST_PASSWORD)
            await client.async_set_connector_lock(TEST_CHARGER_ID, enabled=False)

            # Verify the request body contained value="false", not an unlock flag
            key = ("POST", URL(f"{API_BASE_URL}{Endpoints.UPDATE_CONNECTOR_LOCK}"))
            assert key in mocked.requests, "UPDATE_CONNECTOR_LOCK was not called"
            sent_kwargs = mocked.requests[key][0].kwargs
            sent_body = sent_kwargs.get("json") or sent_kwargs.get("data") or {}
            assert sent_body.get("value") == "false", f"Expected value='false' in body, got: {sent_body}"
            assert "chargerId" in sent_body, "Expected chargerId in body"

        await client.close()

        # --- Part 2: async_unlock_connector hits UNLOCK_CONNECTOR (not UPDATE_CONNECTOR_LOCK) ---
        client2 = WellborneApiClient(email=TEST_EMAIL)
        with aioresponses() as mocked:
            mocked.post(f"{API_BASE_URL}{Endpoints.LOGIN}", payload=api_login_response)
            mocked.post(f"{API_BASE_URL}{Endpoints.UNLOCK_CONNECTOR}", payload=response)

            await client2.async_login(TEST_PASSWORD)
            await client2.async_unlock_connector(TEST_CHARGER_ID)

            unlock_key = ("POST", URL(f"{API_BASE_URL}{Endpoints.UNLOCK_CONNECTOR}"))
            config_key = ("POST", URL(f"{API_BASE_URL}{Endpoints.UPDATE_CONNECTOR_LOCK}"))
            assert unlock_key in mocked.requests, "UNLOCK_CONNECTOR was not called"
            assert config_key not in mocked.requests, "async_unlock_connector must NOT call UPDATE_CONNECTOR_LOCK"

        await client2.close()

    @pytest.mark.unit
    async def test_set_max_power(
        self,
        client: WellborneApiClient,
        api_login_response: dict[str, Any],
    ) -> None:
        """Test setting maximum power."""
        response = {"result": 0, "msg": "success", "obj": None}

        with aioresponses() as mocked:
            mocked.post(
                f"{API_BASE_URL}{Endpoints.LOGIN}",
                payload=api_login_response,
            )
            mocked.post(
                f"{API_BASE_URL}{Endpoints.UPDATE_MAX_POWER}",
                payload=response,
            )

            await client.async_login(TEST_PASSWORD)
            await client.async_set_max_power(TEST_CHARGER_ID, 11000)

        await client.close()

    @pytest.mark.unit
    async def test_set_lcd_enabled(
        self,
        client: WellborneApiClient,
        api_login_response: dict[str, Any],
    ) -> None:
        """Test enabling/disabling LCD."""
        response = {"result": 0, "msg": "success", "obj": None}

        with aioresponses() as mocked:
            mocked.post(
                f"{API_BASE_URL}{Endpoints.LOGIN}",
                payload=api_login_response,
            )
            mocked.post(
                f"{API_BASE_URL}{Endpoints.UPDATE_LCD}",
                payload=response,
            )

            await client.async_login(TEST_PASSWORD)
            await client.async_set_lcd_enabled(TEST_CHARGER_ID, enabled=True)

        await client.close()

    @pytest.mark.unit
    async def test_get_load_balancing(
        self,
        client: WellborneApiClient,
        api_login_response: dict[str, Any],
    ) -> None:
        """Test getting load balancing configuration."""
        response = {
            "result": 0,
            "msg": "success",
            "obj": {
                "enabled": True,
                "maxCurrent": 32,
                "chargerCount": 2,
            },
        }

        with aioresponses() as mocked:
            mocked.post(
                f"{API_BASE_URL}{Endpoints.LOGIN}",
                payload=api_login_response,
            )
            mocked.post(
                f"{API_BASE_URL}{Endpoints.GET_LOAD_BALANCING}",
                payload=response,
            )

            await client.async_login(TEST_PASSWORD)
            result = await client.async_get_load_balancing(TEST_CHARGER_ID)

            assert result["enabled"] is True
            assert result["maxCurrent"] == 32

        await client.close()

    @pytest.mark.unit
    async def test_set_load_balancing(
        self,
        client: WellborneApiClient,
        api_login_response: dict[str, Any],
    ) -> None:
        """Test setting load balancing configuration."""
        response = {"result": 0, "msg": "success", "obj": None}

        with aioresponses() as mocked:
            mocked.post(
                f"{API_BASE_URL}{Endpoints.LOGIN}",
                payload=api_login_response,
            )
            mocked.post(
                f"{API_BASE_URL}{Endpoints.SET_LOAD_BALANCING}",
                payload=response,
            )

            await client.async_login(TEST_PASSWORD)
            await client.async_set_load_balancing(TEST_CHARGER_ID, enabled=True, max_current=32)

        await client.close()

    @pytest.mark.unit
    async def test_get_time_rate(
        self,
        client: WellborneApiClient,
        api_login_response: dict[str, Any],
    ) -> None:
        """Test getting time rate configuration."""
        response = {
            "result": 0,
            "msg": "success",
            "obj": {
                "rate1": {"start": "00:00", "end": "06:00", "price": 0.15},
                "rate2": {"start": "06:00", "end": "22:00", "price": 0.25},
            },
        }

        with aioresponses() as mocked:
            mocked.post(
                f"{API_BASE_URL}{Endpoints.LOGIN}",
                payload=api_login_response,
            )
            mocked.post(
                f"{API_BASE_URL}{Endpoints.GET_TIME_RATE}",
                payload=response,
            )

            await client.async_login(TEST_PASSWORD)
            result = await client.async_get_time_rate(TEST_CHARGER_ID)

            assert "rate1" in result

        await client.close()

    @pytest.mark.unit
    async def test_save_time_rate(
        self,
        client: WellborneApiClient,
        api_login_response: dict[str, Any],
    ) -> None:
        """Test saving time rate configuration."""
        response = {"result": 0, "msg": "success", "obj": None}

        with aioresponses() as mocked:
            mocked.post(
                f"{API_BASE_URL}{Endpoints.LOGIN}",
                payload=api_login_response,
            )
            mocked.post(
                f"{API_BASE_URL}{Endpoints.SAVE_TIME_RATE}",
                payload=response,
            )

            await client.async_login(TEST_PASSWORD)
            await client.async_save_time_rate(
                TEST_CHARGER_ID,
                rates=[{"start": "00:00", "end": "06:00", "price": 0.15}],
            )

        await client.close()

    @pytest.mark.unit
    async def test_get_off_peak_time(
        self,
        client: WellborneApiClient,
        api_login_response: dict[str, Any],
    ) -> None:
        """Test getting off-peak time settings."""
        response = {
            "result": 0,
            "msg": "success",
            "obj": {
                "enabled": True,
                "weekdayStart": "22:00",
                "weekdayEnd": "06:00",
                "weekendStart": "00:00",
                "weekendEnd": "00:00",
            },
        }

        with aioresponses() as mocked:
            mocked.post(
                f"{API_BASE_URL}{Endpoints.LOGIN}",
                payload=api_login_response,
            )
            mocked.post(
                f"{API_BASE_URL}{Endpoints.GET_OFF_PEAK_TIME}",
                payload=response,
            )

            await client.async_login(TEST_PASSWORD)
            result = await client.async_get_off_peak_time(TEST_CHARGER_ID)

            assert result["enabled"] is True
            assert result["weekdayStart"] == "22:00"

        await client.close()

    @pytest.mark.unit
    async def test_set_off_peak_time(
        self,
        client: WellborneApiClient,
        api_login_response: dict[str, Any],
    ) -> None:
        """Test setting off-peak time."""
        response = {"result": 0, "msg": "success", "obj": None}

        with aioresponses() as mocked:
            mocked.post(
                f"{API_BASE_URL}{Endpoints.LOGIN}",
                payload=api_login_response,
            )
            mocked.post(
                f"{API_BASE_URL}{Endpoints.SET_OFF_PEAK_TIME}",
                payload=response,
            )

            await client.async_login(TEST_PASSWORD)
            await client.async_set_off_peak_time(
                TEST_CHARGER_ID,
                weekday_start="22:00",
                weekday_end="06:00",
            )

        await client.close()

    @pytest.mark.unit
    async def test_set_off_peak_enabled(
        self,
        client: WellborneApiClient,
        api_login_response: dict[str, Any],
    ) -> None:
        """Test enabling off-peak mode."""
        response = {"result": 0, "msg": "success", "obj": None}

        with aioresponses() as mocked:
            mocked.post(
                f"{API_BASE_URL}{Endpoints.LOGIN}",
                payload=api_login_response,
            )
            mocked.post(
                f"{API_BASE_URL}{Endpoints.SET_OFF_PEAK_ENABLE}",
                payload=response,
            )

            await client.async_login(TEST_PASSWORD)
            await client.async_set_off_peak_enabled(TEST_CHARGER_ID, enabled=True)

        await client.close()

    @pytest.mark.unit
    async def test_get_firmware_status(
        self,
        client: WellborneApiClient,
        api_login_response: dict[str, Any],
    ) -> None:
        """Test getting firmware update status."""
        response = {
            "result": 0,
            "msg": "success",
            "obj": {
                "updateAvailable": False,
                "currentVersion": "1.2.3",
                "latestVersion": "1.2.3",
            },
        }

        with aioresponses() as mocked:
            mocked.post(
                f"{API_BASE_URL}{Endpoints.LOGIN}",
                payload=api_login_response,
            )
            mocked.post(
                f"{API_BASE_URL}{Endpoints.GET_FIRMWARE_STATUS}",
                payload=response,
            )

            await client.async_login(TEST_PASSWORD)
            result = await client.async_get_firmware_status(TEST_CHARGER_ID)

            assert result["updateAvailable"] is False
            assert result["currentVersion"] == "1.2.3"

        await client.close()

    @pytest.mark.unit
    async def test_get_transactions_month(
        self,
        client: WellborneApiClient,
        api_login_response: dict[str, Any],
    ) -> None:
        """Test getting monthly transaction records."""
        response = {
            "result": 0,
            "msg": "success",
            "obj": {
                "energyTotal": 150.5,
                "totalSessions": 12,
            },
        }

        with aioresponses() as mocked:
            mocked.post(
                f"{API_BASE_URL}{Endpoints.LOGIN}",
                payload=api_login_response,
            )
            mocked.post(
                f"{API_BASE_URL}{Endpoints.TRANSACTION_MONTH}",
                payload=response,
            )

            await client.async_login(TEST_PASSWORD)
            result = await client.async_get_transactions_month(TEST_CHARGER_ID, "2025-01")

            assert result["energyTotal"] == 150.5

        await client.close()

    @pytest.mark.unit
    async def test_get_transactions_year(
        self,
        client: WellborneApiClient,
        api_login_response: dict[str, Any],
    ) -> None:
        """Test getting yearly transaction records."""
        response = {
            "result": 0,
            "msg": "success",
            "obj": {
                "energyTotal": 1500.5,
                "totalSessions": 120,
            },
        }

        with aioresponses() as mocked:
            mocked.post(
                f"{API_BASE_URL}{Endpoints.LOGIN}",
                payload=api_login_response,
            )
            mocked.post(
                f"{API_BASE_URL}{Endpoints.TRANSACTION_YEAR}",
                payload=response,
            )

            await client.async_login(TEST_PASSWORD)
            result = await client.async_get_transactions_year(TEST_CHARGER_ID, "2025")

            assert result["energyTotal"] == 1500.5

        await client.close()

    @pytest.mark.unit
    async def test_get_wifi_info(
        self,
        client: WellborneApiClient,
        api_login_response: dict[str, Any],
    ) -> None:
        """Test getting WiFi information."""
        response = {
            "result": 0,
            "msg": "success",
            "obj": {
                "ssid": "HomeNetwork",
                "signal": -45,
            },
        }

        with aioresponses() as mocked:
            mocked.post(
                f"{API_BASE_URL}{Endpoints.LOGIN}",
                payload=api_login_response,
            )
            mocked.post(
                f"{API_BASE_URL}{Endpoints.GET_WIFI_INFO}",
                payload=response,
            )

            await client.async_login(TEST_PASSWORD)
            result = await client.async_get_wifi_info(TEST_CHARGER_ID)

            assert result["ssid"] == "HomeNetwork"

        await client.close()

    @pytest.mark.unit
    async def test_set_scheduled_by_energy(
        self,
        client: WellborneApiClient,
        api_login_response: dict[str, Any],
    ) -> None:
        """Test setting scheduled charging by energy amount."""
        response = {"result": 0, "msg": "success", "obj": None}

        with aioresponses() as mocked:
            mocked.post(
                f"{API_BASE_URL}{Endpoints.LOGIN}",
                payload=api_login_response,
            )
            mocked.post(
                f"{API_BASE_URL}{Endpoints.SET_SCHEDULED_BY_ENERGY}",
                payload=response,
            )

            await client.async_login(TEST_PASSWORD)
            await client.async_set_scheduled_by_energy(
                TEST_CHARGER_ID,
                connector_id="1",
                energy_kwh=30.0,
                cycle="1234567",
                cycle_time="22:00",
            )

        await client.close()

    @pytest.mark.unit
    async def test_set_scheduled_by_full(
        self,
        client: WellborneApiClient,
        api_login_response: dict[str, Any],
    ) -> None:
        """Test setting scheduled charging until full."""
        response = {"result": 0, "msg": "success", "obj": None}

        with aioresponses() as mocked:
            mocked.post(
                f"{API_BASE_URL}{Endpoints.LOGIN}",
                payload=api_login_response,
            )
            mocked.post(
                f"{API_BASE_URL}{Endpoints.SET_SCHEDULED_BY_FULL}",
                payload=response,
            )

            await client.async_login(TEST_PASSWORD)
            await client.async_set_scheduled_by_full(
                TEST_CHARGER_ID,
                connector_id="1",
                cycle="1234567",
                cycle_time="22:00",
            )

        await client.close()

    @pytest.mark.unit
    async def test_set_scheduled_by_end_time(
        self,
        client: WellborneApiClient,
        api_login_response: dict[str, Any],
    ) -> None:
        """Test setting scheduled charging by end time."""
        response = {"result": 0, "msg": "success", "obj": None}

        with aioresponses() as mocked:
            mocked.post(
                f"{API_BASE_URL}{Endpoints.LOGIN}",
                payload=api_login_response,
            )
            mocked.post(
                f"{API_BASE_URL}{Endpoints.SET_SCHEDULED_BY_END_TIME}",
                payload=response,
            )

            await client.async_login(TEST_PASSWORD)
            await client.async_set_scheduled_by_end_time(
                TEST_CHARGER_ID,
                connector_id="1",
                end_time="07:00",
                cycle="1234567",
                cycle_time="22:00",
            )

        await client.close()

    @pytest.mark.unit
    async def test_async_get_charger_data(
        self,
        client: WellborneApiClient,
        api_login_response: dict[str, Any],
        api_charger_list_response: dict[str, Any],
        api_charger_config_response: dict[str, Any],
        api_home_config_response: dict[str, Any],
    ) -> None:
        """Test getting combined charger data."""
        is_charging_response = {"result": 0, "msg": "success", "obj": False}
        delayed_response = {
            "result": 0,
            "msg": "success",
            "obj": {"delayTime": 0, "status": 2, "selectStatus": 0},
        }
        scheduled_response = {
            "result": 0,
            "msg": "success",
            "obj": {"enabled": False, "cycle": "", "cycleTime": ""},
        }
        off_peak_response = {
            "result": 0,
            "msg": "success",
            "obj": {
                "status": 0,
                "weekdayStart": "22:00",
                "weekdayEnd": "06:00",
                "weekendStart": "00:00",
                "weekendEnd": "00:00",
            },
        }
        transactions_response = {"result": 0, "msg": "success", "obj": []}
        monthly_response = {"result": 0, "msg": "success", "obj": {"energyTotal": 50.5, "sessionCount": 5}}
        yearly_response = {"result": 0, "msg": "success", "obj": {"energyTotal": 500.0, "sessionCount": 50}}
        firmware_response = {
            "result": 0,
            "msg": "success",
            "obj": {"updateAvailable": False, "currentVersion": "1.2.3", "latestVersion": "1.2.3"},
        }
        wifi_response = {"result": 0, "msg": "success", "obj": {"ssid": "HomeWifi", "signal": -50}}
        load_balancing_response = {"result": 0, "msg": "success", "obj": {"enabled": False, "maxCurrent": 32}}

        with aioresponses() as mocked:
            mocked.post(f"{API_BASE_URL}{Endpoints.LOGIN}", payload=api_login_response)
            mocked.post(f"{API_BASE_URL}{Endpoints.CHARGER_LIST}", payload=api_charger_list_response)
            mocked.post(f"{API_BASE_URL}{Endpoints.IS_CHARGING}", payload=is_charging_response)
            mocked.post(f"{API_BASE_URL}{Endpoints.GET_CHARGER_CONFIG}", payload=api_charger_config_response)
            mocked.post(f"{API_BASE_URL}{Endpoints.GET_HOME_CONFIG}", payload=api_home_config_response)
            mocked.post(f"{API_BASE_URL}{Endpoints.GET_DELAYED_CHARGING}", payload=delayed_response)
            mocked.post(f"{API_BASE_URL}{Endpoints.GET_SCHEDULED_TASK}", payload=scheduled_response)
            mocked.post(f"{API_BASE_URL}{Endpoints.GET_OFF_PEAK_TIME}", payload=off_peak_response)
            mocked.post(f"{API_BASE_URL}{Endpoints.TRANSACTION_LIST}", payload=transactions_response)
            mocked.post(f"{API_BASE_URL}{Endpoints.TRANSACTION_MONTH}", payload=monthly_response)
            mocked.post(f"{API_BASE_URL}{Endpoints.TRANSACTION_YEAR}", payload=yearly_response)
            mocked.post(f"{API_BASE_URL}{Endpoints.GET_FIRMWARE_STATUS}", payload=firmware_response)
            mocked.post(f"{API_BASE_URL}{Endpoints.GET_WIFI_INFO}", payload=wifi_response)
            mocked.post(f"{API_BASE_URL}{Endpoints.GET_LOAD_BALANCING}", payload=load_balancing_response)

            await client.async_login(TEST_PASSWORD)
            data = await client.async_get_charger_data(TEST_CHARGER_ID)

            # Verify the returned data
            assert data.charger.charger_id == TEST_CHARGER_ID
            assert data.status.is_charging is False
            assert data.status.max_current == 16.0
            assert data.wifi_info is not None
            assert data.wifi_info.ssid == "HomeWifi"
            assert data.wifi_info.signal == -50
            assert data.load_balancing.enabled is False
            assert data.firmware is not None
            assert data.firmware.current_version == "1.2.3"

        await client.close()

    @pytest.mark.unit
    async def test_async_get_charger_data_while_charging(
        self,
        client: WellborneApiClient,
        api_login_response: dict[str, Any],
        api_charger_list_response: dict[str, Any],
        api_charger_config_response: dict[str, Any],
        api_home_config_response: dict[str, Any],
    ) -> None:
        """Test getting combined charger data while charging."""
        is_charging_response = {"result": 0, "msg": "success", "obj": True}
        delayed_response = {"result": 0, "msg": "success", "obj": {"delayTime": 0, "status": 2, "selectStatus": 0}}
        scheduled_response = {"result": 0, "msg": "success", "obj": {"enabled": False, "cycle": "", "cycleTime": ""}}
        off_peak_response = {
            "result": 0,
            "msg": "success",
            "obj": {"status": 0, "weekdayStart": "22:00", "weekdayEnd": "06:00"},
        }
        # Use real API format: paginated with dataList, transactionId, energyKWH, startDate/startTime
        transactions_response = {
            "result": 0,
            "msg": "success",
            "obj": {
                "pageNow": 1,
                "pageTotal": 1,
                "dataList": [
                    {
                        "transactionId": 123,
                        "energyKWH": "10.5",
                        "startDate": "01/01 2025",
                        "startTime": "10:00:00",
                        "stopTime": None,
                        "chargingTime": None,
                    },
                    {
                        "transactionId": 122,
                        "energyKWH": "15.0",
                        "startDate": "12/31 2024",
                        "startTime": "08:00:00",
                        "stopTime": "10:00:00",
                        "chargingTime": "02:00:00",
                    },
                ],
            },
        }
        meter_values_response = {
            "result": 0,
            "msg": "success",
            "obj": [
                {
                    "voltage": 230.5,
                    "voltageL2": 231.0,
                    "voltageL3": 229.5,
                    "current": 16.0,
                    "currentL2": 15.8,
                    "currentL3": 16.2,
                    "energy": 10.5,
                    "phase": "3-phase",
                    "time": "2025-01-01 12:00:00",
                }
            ],
        }
        monthly_response = {"result": 0, "msg": "success", "obj": {"energyTotal": 50.5, "sessionCount": 5}}
        yearly_response = {"result": 0, "msg": "success", "obj": {"energyTotal": 500.0, "sessionCount": 50}}
        firmware_response = {"result": 0, "msg": "success", "obj": {"updateAvailable": True, "currentVersion": "1.2.2"}}
        wifi_response = {"result": 0, "msg": "success", "obj": {"ssid": "HomeWifi", "signal": -45}}
        load_balancing_response = {
            "result": 0,
            "msg": "success",
            "obj": {"enablePowerAllocationCharge": "1", "totalDomesticPower": "25"},
        }

        with aioresponses() as mocked:
            mocked.post(f"{API_BASE_URL}{Endpoints.LOGIN}", payload=api_login_response)
            mocked.post(f"{API_BASE_URL}{Endpoints.CHARGER_LIST}", payload=api_charger_list_response)
            mocked.post(f"{API_BASE_URL}{Endpoints.IS_CHARGING}", payload=is_charging_response)
            mocked.post(f"{API_BASE_URL}{Endpoints.GET_CHARGER_CONFIG}", payload=api_charger_config_response)
            mocked.post(f"{API_BASE_URL}{Endpoints.GET_HOME_CONFIG}", payload=api_home_config_response)
            mocked.post(f"{API_BASE_URL}{Endpoints.GET_DELAYED_CHARGING}", payload=delayed_response)
            mocked.post(f"{API_BASE_URL}{Endpoints.GET_SCHEDULED_TASK}", payload=scheduled_response)
            mocked.post(f"{API_BASE_URL}{Endpoints.GET_OFF_PEAK_TIME}", payload=off_peak_response)
            mocked.post(f"{API_BASE_URL}{Endpoints.TRANSACTION_LIST}", payload=transactions_response)
            mocked.post(f"{API_BASE_URL}{Endpoints.GET_VALUES}", payload=meter_values_response)
            mocked.post(f"{API_BASE_URL}{Endpoints.TRANSACTION_MONTH}", payload=monthly_response)
            mocked.post(f"{API_BASE_URL}{Endpoints.TRANSACTION_YEAR}", payload=yearly_response)
            mocked.post(f"{API_BASE_URL}{Endpoints.GET_FIRMWARE_STATUS}", payload=firmware_response)
            mocked.post(f"{API_BASE_URL}{Endpoints.GET_WIFI_INFO}", payload=wifi_response)
            mocked.post(f"{API_BASE_URL}{Endpoints.GET_LOAD_BALANCING}", payload=load_balancing_response)

            await client.async_login(TEST_PASSWORD)
            data = await client.async_get_charger_data(TEST_CHARGER_ID)

            # Verify charging state
            assert data.status.is_charging is True
            assert data.transaction_id == "123"
            assert data.session_start_time is not None

            # Verify meter values
            assert data.meter_values is not None
            assert data.meter_values.voltage == 230.5
            assert data.meter_values.current == 16.0

            # Verify last session data
            assert data.last_session is not None
            assert data.last_session.energy == 15.0

            # Verify lifetime energy
            assert data.lifetime_energy == 25.5  # 10.5 + 15.0

            # Verify firmware update available
            assert data.firmware is not None
            assert data.firmware.update_available is True

            # Verify monthly/yearly statistics (parsed from energyTotal field)
            assert data.monthly_statistics is not None
            assert data.monthly_statistics.total_energy == 50.5
            assert data.yearly_statistics is not None
            assert data.yearly_statistics.total_energy == 500.0

            # Verify load balancing (enablePowerAllocationCharge='1' => enabled,
            # totalDomesticPower stored in the max_current field)
            assert data.load_balancing.enabled is True
            assert data.load_balancing.max_current == 25

        await client.close()

    @pytest.mark.unit
    async def test_async_get_charger_data_charger_not_found(
        self,
        client: WellborneApiClient,
        api_login_response: dict[str, Any],
    ) -> None:
        """Test getting charger data when charger is not found."""
        charger_list_response = {"result": 0, "msg": "success", "obj": []}

        with aioresponses() as mocked:
            mocked.post(f"{API_BASE_URL}{Endpoints.LOGIN}", payload=api_login_response)
            mocked.post(f"{API_BASE_URL}{Endpoints.CHARGER_LIST}", payload=charger_list_response)

            await client.async_login(TEST_PASSWORD)

            with pytest.raises(ApiResponseError, match="not found"):
                await client.async_get_charger_data("NONEXISTENT")

        await client.close()

    @pytest.mark.unit
    async def test_safe_float_helper(self) -> None:
        """Test the _safe_float helper method."""
        # Normal float conversion
        assert WellborneApiClient._safe_float(10.5) == 10.5
        assert WellborneApiClient._safe_float("10.5") == 10.5
        assert WellborneApiClient._safe_float(10) == 10.0

        # None returns default
        assert WellborneApiClient._safe_float(None) == 0.0
        assert WellborneApiClient._safe_float(None, default=5.0) == 5.0

        # Invalid values return default
        assert WellborneApiClient._safe_float("not a number") == 0.0
        assert WellborneApiClient._safe_float({}) == 0.0
        assert WellborneApiClient._safe_float([]) == 0.0


class TestRedactSensitive:
    """Tests for redaction of sensitive values in debug logging."""

    def test_redact_masks_password_token_and_wifi_password(self) -> None:
        """Sensitive keys are masked, including nested and in lists."""
        masked = "***"
        payload = {"email": "a@b.com", "password": "deadbeefhash", "phoneOs": "0"}
        response = {
            "result": 0,
            "obj": {"token": "JWT.value", "wifiPassword": "pw", "wifiSsid": "Net"},
            "dataList": [{"token": "x", "alias": "Demo"}],
        }

        rp = _redact_sensitive(payload)
        rr = _redact_sensitive(response)

        assert rp["password"] == masked
        assert rp["email"] == "a@b.com"
        assert rr["obj"]["token"] == masked
        assert rr["obj"]["wifiPassword"] == masked
        assert rr["obj"]["wifiSsid"] == "Net"
        assert rr["dataList"][0]["token"] == masked
        assert rr["dataList"][0]["alias"] == "Demo"

    def test_redact_does_not_mutate_original(self) -> None:
        """Redaction returns a copy; the original payload keeps its secrets."""
        secret_pw = "secret"  # noqa: S105
        secret_token = "JWT"  # noqa: S105
        payload = {"password": secret_pw, "obj": {"token": secret_token}}
        _redact_sensitive(payload)
        assert payload["password"] == secret_pw
        assert payload["obj"]["token"] == secret_token

    def test_redact_passes_through_non_mapping(self) -> None:
        """Non-dict values pass through unchanged."""
        assert _redact_sensitive(None) is None
        assert _redact_sensitive("plain") == "plain"
