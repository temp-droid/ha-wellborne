"""Tests for the Wellborne DataUpdateCoordinator."""

from __future__ import annotations

from datetime import timedelta
from unittest.mock import AsyncMock, MagicMock, patch

from homeassistant.core import HomeAssistant
from homeassistant.exceptions import ConfigEntryAuthFailed, HomeAssistantError
from homeassistant.helpers.update_coordinator import UpdateFailed
import pytest
from pytest_homeassistant_custom_component.common import MockConfigEntry

from custom_components.wellborne.api import (
    ApiConnectionError,
    AuthenticationError,
    ChargerOfflineError,
    SessionExpiredError,
    WellborneData,
    WellborneError,
)
from custom_components.wellborne.const import (
    CHARGING_POLL_INTERVAL,
    DOMAIN,
    IDLE_POLL_INTERVAL,
    OFFLINE_POLL_INTERVAL,
    OFFLINE_TIMEOUT_COUNT,
)
from custom_components.wellborne.coordinator import WellborneDataUpdateCoordinator

from .conftest import TEST_CHARGER_ID


@pytest.fixture
def mock_api_client_local():
    """Create a mock API client (local to this test module)."""
    client = MagicMock()
    client.async_get_charger_data = AsyncMock()
    client.async_start_charging = AsyncMock()
    client.async_stop_charging = AsyncMock()
    client.async_set_max_current = AsyncMock()
    client.async_set_solar_mode = AsyncMock()
    client.async_unlock_connector = AsyncMock()
    client.async_prompt_charge = AsyncMock()
    client.async_set_connector_lock = AsyncMock()
    client.async_set_delayed_charging = AsyncMock()
    client.async_set_scheduled_by_time = AsyncMock()
    client.async_set_off_peak_enabled = AsyncMock()
    client.async_set_off_peak_time = AsyncMock()
    client.async_set_lcd_enabled = AsyncMock()
    client.async_set_low_power_reserve = AsyncMock()
    client.async_set_load_balancing = AsyncMock()
    client.async_set_max_power = AsyncMock()
    return client


@pytest.fixture
def mock_config_entry_local() -> MockConfigEntry:
    """Create a mock config entry for coordinator tests."""
    return MockConfigEntry(
        domain=DOMAIN,
        title="test@example.com",
        data={"email": "test@example.com", "password": "test"},
        options={
            "vehicle_efficiency": 6.0,
            "charging_poll_interval": 30,
            "idle_poll_interval": 120,
        },
        unique_id="test@example.com",
        version=1,
    )


@pytest.fixture
def coordinator(hass: HomeAssistant, mock_api_client_local, mock_config_entry_local) -> WellborneDataUpdateCoordinator:
    """Create a coordinator for testing."""
    return WellborneDataUpdateCoordinator(
        hass,
        mock_api_client_local,
        TEST_CHARGER_ID,
        config_entry=mock_config_entry_local,
        update_interval=30,
    )


# =============================================================================
# Coordinator Properties Tests
# =============================================================================


async def test_coordinator_properties(
    hass: HomeAssistant,
    mock_api_client_local,
    coordinator: WellborneDataUpdateCoordinator,
) -> None:
    """Test coordinator properties return correct values."""
    assert coordinator.client is mock_api_client_local
    assert coordinator.charger_id == TEST_CHARGER_ID


# =============================================================================
# _async_update_data Tests
# =============================================================================


async def test_async_update_data_success(
    hass: HomeAssistant,
    mock_api_client_local,
    coordinator: WellborneDataUpdateCoordinator,
    mock_wellborne_data: WellborneData,
) -> None:
    """Test successful data fetch."""
    mock_api_client_local.async_get_charger_data.return_value = mock_wellborne_data

    result = await coordinator._async_update_data()

    assert result is mock_wellborne_data
    mock_api_client_local.async_get_charger_data.assert_called_once_with(TEST_CHARGER_ID)


async def test_async_update_data_auth_error(
    hass: HomeAssistant,
    mock_api_client_local,
    coordinator: WellborneDataUpdateCoordinator,
) -> None:
    """Test authentication error raises ConfigEntryAuthFailed."""
    mock_api_client_local.async_get_charger_data.side_effect = AuthenticationError("Invalid credentials")

    with pytest.raises(ConfigEntryAuthFailed):
        await coordinator._async_update_data()


async def test_async_update_data_session_expired(
    hass: HomeAssistant,
    mock_api_client_local,
    coordinator: WellborneDataUpdateCoordinator,
) -> None:
    """Test session expired error raises ConfigEntryAuthFailed."""
    mock_api_client_local.async_get_charger_data.side_effect = SessionExpiredError("Session expired")

    with pytest.raises(ConfigEntryAuthFailed):
        await coordinator._async_update_data()


async def test_async_update_data_connection_error(
    hass: HomeAssistant,
    mock_api_client_local,
    coordinator: WellborneDataUpdateCoordinator,
) -> None:
    """Test connection error raises UpdateFailed."""
    mock_api_client_local.async_get_charger_data.side_effect = ApiConnectionError("Connection failed")

    with pytest.raises(UpdateFailed, match="Error communicating with API"):
        await coordinator._async_update_data()


async def test_async_update_data_wellborne_error(
    hass: HomeAssistant,
    mock_api_client_local,
    coordinator: WellborneDataUpdateCoordinator,
) -> None:
    """Test generic Wellborne error raises UpdateFailed."""
    mock_api_client_local.async_get_charger_data.side_effect = WellborneError("Something went wrong")

    with pytest.raises(UpdateFailed, match="Error fetching data"):
        await coordinator._async_update_data()


# =============================================================================
# Charging Control Tests
# =============================================================================


async def test_async_start_charging(
    hass: HomeAssistant,
    mock_api_client_local,
    coordinator: WellborneDataUpdateCoordinator,
) -> None:
    """Test starting a charging session."""
    with patch.object(coordinator, "async_request_refresh", new_callable=AsyncMock) as mock_refresh:
        await coordinator.async_start_charging()

        mock_api_client_local.async_start_charging.assert_called_once_with(TEST_CHARGER_ID, "1")
        mock_refresh.assert_called_once()


async def test_async_start_charging_custom_connector(
    hass: HomeAssistant,
    mock_api_client_local,
    coordinator: WellborneDataUpdateCoordinator,
) -> None:
    """Test starting a charging session on specific connector."""
    with patch.object(coordinator, "async_request_refresh", new_callable=AsyncMock):
        await coordinator.async_start_charging(connector_id="2")

        mock_api_client_local.async_start_charging.assert_called_once_with(TEST_CHARGER_ID, "2")


async def test_async_stop_charging(
    hass: HomeAssistant,
    mock_api_client_local,
    coordinator: WellborneDataUpdateCoordinator,
) -> None:
    """Test stopping a charging session."""
    with patch.object(coordinator, "async_request_refresh", new_callable=AsyncMock) as mock_refresh:
        await coordinator.async_stop_charging()

        mock_api_client_local.async_stop_charging.assert_called_once_with(TEST_CHARGER_ID, "1")
        mock_refresh.assert_called_once()


async def test_async_prompt_charge(
    hass: HomeAssistant,
    mock_api_client_local,
    coordinator: WellborneDataUpdateCoordinator,
) -> None:
    """Test immediate charge (bypass delay)."""
    with patch.object(coordinator, "async_request_refresh", new_callable=AsyncMock) as mock_refresh:
        await coordinator.async_prompt_charge()

        mock_api_client_local.async_prompt_charge.assert_called_once_with(TEST_CHARGER_ID, "1")
        mock_refresh.assert_called_once()


async def test_async_unlock_connector(
    hass: HomeAssistant,
    mock_api_client_local,
    coordinator: WellborneDataUpdateCoordinator,
) -> None:
    """Test unlocking the connector."""
    await coordinator.async_unlock_connector()

    mock_api_client_local.async_unlock_connector.assert_called_once_with(TEST_CHARGER_ID)


# =============================================================================
# Current and Power Settings Tests
# =============================================================================


async def test_async_set_max_current(
    hass: HomeAssistant,
    mock_api_client_local,
    coordinator: WellborneDataUpdateCoordinator,
) -> None:
    """Test setting maximum charging current."""
    with patch.object(coordinator, "async_request_refresh", new_callable=AsyncMock) as mock_refresh:
        await coordinator.async_set_max_current(16)

        mock_api_client_local.async_set_max_current.assert_called_once_with(TEST_CHARGER_ID, 16)
        mock_refresh.assert_called_once()


async def test_async_set_max_power(
    hass: HomeAssistant,
    mock_api_client_local,
    coordinator: WellborneDataUpdateCoordinator,
) -> None:
    """Test setting maximum charging power."""
    with patch.object(coordinator, "async_request_refresh", new_callable=AsyncMock) as mock_refresh:
        await coordinator.async_set_max_power(11000)

        mock_api_client_local.async_set_max_power.assert_called_once_with(TEST_CHARGER_ID, 11000)
        mock_refresh.assert_called_once()


async def test_async_set_solar_mode(
    hass: HomeAssistant,
    mock_api_client_local,
    coordinator: WellborneDataUpdateCoordinator,
) -> None:
    """Test setting solar charging mode."""
    with patch.object(coordinator, "async_request_refresh", new_callable=AsyncMock) as mock_refresh:
        await coordinator.async_set_solar_mode("1")

        mock_api_client_local.async_set_solar_mode.assert_called_once_with(TEST_CHARGER_ID, "1")
        mock_refresh.assert_called_once()


# =============================================================================
# Connector Lock Tests
# =============================================================================


async def test_async_set_connector_lock_enabled(
    hass: HomeAssistant,
    mock_api_client_local,
    coordinator: WellborneDataUpdateCoordinator,
) -> None:
    """Test enabling connector lock."""
    with patch.object(coordinator, "async_request_refresh", new_callable=AsyncMock) as mock_refresh:
        await coordinator.async_set_connector_lock(enabled=True)

        mock_api_client_local.async_set_connector_lock.assert_called_once_with(TEST_CHARGER_ID, enabled=True)
        mock_refresh.assert_called_once()


async def test_async_set_connector_lock_disabled(
    hass: HomeAssistant,
    mock_api_client_local,
    coordinator: WellborneDataUpdateCoordinator,
) -> None:
    """Test disabling connector lock."""
    with patch.object(coordinator, "async_request_refresh", new_callable=AsyncMock):
        await coordinator.async_set_connector_lock(enabled=False)

        mock_api_client_local.async_set_connector_lock.assert_called_once_with(TEST_CHARGER_ID, enabled=False)


# =============================================================================
# Delayed Charging Tests
# =============================================================================


async def test_async_set_delayed_charging_enabled(
    hass: HomeAssistant,
    mock_api_client_local,
    coordinator: WellborneDataUpdateCoordinator,
    mock_wellborne_data: WellborneData,
) -> None:
    """Test enabling delayed charging preserves delay time."""
    coordinator.data = mock_wellborne_data
    coordinator.data.delayed_charging.delay_time = 1800  # 30 minutes

    with patch.object(coordinator, "async_request_refresh", new_callable=AsyncMock) as mock_refresh:
        await coordinator.async_set_delayed_charging_enabled(enabled=True)

        mock_api_client_local.async_set_delayed_charging.assert_called_once_with(
            TEST_CHARGER_ID, enabled=True, delay_seconds=1800
        )
        mock_refresh.assert_called_once()


async def test_async_set_delayed_charging_disabled_no_data(
    hass: HomeAssistant,
    mock_api_client_local,
    coordinator: WellborneDataUpdateCoordinator,
) -> None:
    """Test disabling delayed charging with no existing data uses 0 delay."""
    coordinator.data = None

    with patch.object(coordinator, "async_request_refresh", new_callable=AsyncMock):
        await coordinator.async_set_delayed_charging_enabled(enabled=False)

        mock_api_client_local.async_set_delayed_charging.assert_called_once_with(
            TEST_CHARGER_ID, enabled=False, delay_seconds=0
        )


async def test_async_set_delay_time(
    hass: HomeAssistant,
    mock_api_client_local,
    coordinator: WellborneDataUpdateCoordinator,
    mock_wellborne_data: WellborneData,
) -> None:
    """Test setting delay time preserves enabled state."""
    coordinator.data = mock_wellborne_data
    coordinator.data.delayed_charging.enabled = True

    with patch.object(coordinator, "async_request_refresh", new_callable=AsyncMock) as mock_refresh:
        await coordinator.async_set_delay_time(45)  # 45 minutes

        mock_api_client_local.async_set_delayed_charging.assert_called_once_with(
            TEST_CHARGER_ID,
            enabled=True,
            delay_seconds=2700,  # 45 * 60
        )
        mock_refresh.assert_called_once()


async def test_async_set_delay_time_no_data(
    hass: HomeAssistant,
    mock_api_client_local,
    coordinator: WellborneDataUpdateCoordinator,
) -> None:
    """Test setting delay time with no data uses enabled=False."""
    coordinator.data = None

    with patch.object(coordinator, "async_request_refresh", new_callable=AsyncMock):
        await coordinator.async_set_delay_time(30)

        mock_api_client_local.async_set_delayed_charging.assert_called_once_with(
            TEST_CHARGER_ID, enabled=False, delay_seconds=1800
        )


# =============================================================================
# Scheduled Charging Tests
# =============================================================================


async def test_async_set_scheduled_charging_enabled(
    hass: HomeAssistant,
    mock_api_client_local,
    coordinator: WellborneDataUpdateCoordinator,
    mock_wellborne_data: WellborneData,
) -> None:
    """Test enabling scheduled charging uses current settings."""
    coordinator.data = mock_wellborne_data
    coordinator.data.scheduled_charging.cycle = "1,2,3,4,5"
    coordinator.data.scheduled_charging.cycle_time = "23:00"

    with patch.object(coordinator, "async_request_refresh", new_callable=AsyncMock) as mock_refresh:
        await coordinator.async_set_scheduled_charging_enabled(enabled=True)

        mock_api_client_local.async_set_scheduled_by_time.assert_called_once_with(
            TEST_CHARGER_ID,
            connector_id="1",
            minutes=60,
            cycle="1,2,3,4,5",
            cycle_time="23:00",
            enabled=True,
        )
        mock_refresh.assert_called_once()


async def test_async_set_scheduled_charging_disabled_uses_defaults(
    hass: HomeAssistant,
    mock_api_client_local,
    coordinator: WellborneDataUpdateCoordinator,
    mock_wellborne_data: WellborneData,
) -> None:
    """Test disabling scheduled charging uses defaults if no cycle/time."""
    coordinator.data = mock_wellborne_data
    coordinator.data.scheduled_charging.cycle = None
    coordinator.data.scheduled_charging.cycle_time = None

    with patch.object(coordinator, "async_request_refresh", new_callable=AsyncMock):
        await coordinator.async_set_scheduled_charging_enabled(enabled=False)

        mock_api_client_local.async_set_scheduled_by_time.assert_called_once_with(
            TEST_CHARGER_ID,
            connector_id="1",
            minutes=60,
            cycle="1,2,3,4,5,6,7",
            cycle_time="22:00",
            enabled=False,
        )


async def test_async_set_scheduled_charging_no_data(
    hass: HomeAssistant,
    mock_api_client_local,
    coordinator: WellborneDataUpdateCoordinator,
) -> None:
    """Test scheduled charging with no data raises HomeAssistantError."""
    coordinator.data = None

    with patch.object(coordinator, "async_request_refresh", new_callable=AsyncMock) as mock_refresh:
        with pytest.raises(HomeAssistantError):
            await coordinator.async_set_scheduled_charging_enabled(enabled=True)

        mock_api_client_local.async_set_scheduled_by_time.assert_not_called()
        mock_refresh.assert_not_called()


async def test_async_set_scheduled_time(
    hass: HomeAssistant,
    mock_api_client_local,
    coordinator: WellborneDataUpdateCoordinator,
    mock_wellborne_data: WellborneData,
) -> None:
    """Test setting scheduled start time."""
    coordinator.data = mock_wellborne_data
    coordinator.data.scheduled_charging.cycle = "1,2,3,4,5"
    coordinator.data.scheduled_charging.enabled = True

    with patch.object(coordinator, "async_request_refresh", new_callable=AsyncMock) as mock_refresh:
        await coordinator.async_set_scheduled_time(cycle_time="21:30")

        mock_api_client_local.async_set_scheduled_by_time.assert_called_once_with(
            TEST_CHARGER_ID,
            connector_id="1",
            minutes=60,
            cycle="1,2,3,4,5",
            cycle_time="21:30",
            enabled=True,
        )
        mock_refresh.assert_called_once()


async def test_async_set_scheduled_time_no_data(
    hass: HomeAssistant,
    mock_api_client_local,
    coordinator: WellborneDataUpdateCoordinator,
) -> None:
    """Test setting scheduled time with no data raises HomeAssistantError."""
    coordinator.data = None

    with patch.object(coordinator, "async_request_refresh", new_callable=AsyncMock) as mock_refresh:
        with pytest.raises(HomeAssistantError):
            await coordinator.async_set_scheduled_time(cycle_time="21:30")

        mock_api_client_local.async_set_scheduled_by_time.assert_not_called()
        mock_refresh.assert_not_called()


async def test_set_scheduled_enabled_raises_when_no_schedule_data(
    hass: HomeAssistant,
    mock_api_client_local,
    coordinator: WellborneDataUpdateCoordinator,
) -> None:
    """Test that enabling scheduled charging raises when scheduled_charging is None."""
    coordinator.data = MagicMock(scheduled_charging=None)

    with patch.object(coordinator, "async_request_refresh", new_callable=AsyncMock) as mock_refresh:
        with pytest.raises(HomeAssistantError):
            await coordinator.async_set_scheduled_charging_enabled(enabled=True)

        mock_api_client_local.async_set_scheduled_by_time.assert_not_called()
        mock_refresh.assert_not_called()


async def test_set_scheduled_time_raises_when_no_schedule_data(
    hass: HomeAssistant,
    mock_api_client_local,
    coordinator: WellborneDataUpdateCoordinator,
) -> None:
    """Test that setting scheduled time raises when scheduled_charging is None."""
    coordinator.data = MagicMock(scheduled_charging=None)

    with patch.object(coordinator, "async_request_refresh", new_callable=AsyncMock) as mock_refresh:
        with pytest.raises(HomeAssistantError):
            await coordinator.async_set_scheduled_time(cycle_time="07:00")

        mock_api_client_local.async_set_scheduled_by_time.assert_not_called()
        mock_refresh.assert_not_called()


# =============================================================================
# Off-Peak Charging Tests
# =============================================================================


async def test_async_set_off_peak_enabled(
    hass: HomeAssistant,
    mock_api_client_local,
    coordinator: WellborneDataUpdateCoordinator,
) -> None:
    """Test enabling off-peak charging."""
    with patch.object(coordinator, "async_request_refresh", new_callable=AsyncMock) as mock_refresh:
        await coordinator.async_set_off_peak_enabled(enabled=True)

        mock_api_client_local.async_set_off_peak_enabled.assert_called_once_with(TEST_CHARGER_ID, enabled=True)
        mock_refresh.assert_called_once()


async def test_async_set_off_peak_time_with_current_values(
    hass: HomeAssistant,
    mock_api_client_local,
    coordinator: WellborneDataUpdateCoordinator,
    mock_wellborne_data: WellborneData,
) -> None:
    """Test setting off-peak time preserves unspecified values."""
    coordinator.data = mock_wellborne_data
    coordinator.data.off_peak.weekday_start = "22:00"
    coordinator.data.off_peak.weekday_end = "06:00"
    coordinator.data.off_peak.weekend_start = "00:00"
    coordinator.data.off_peak.weekend_end = "00:00"

    with patch.object(coordinator, "async_request_refresh", new_callable=AsyncMock) as mock_refresh:
        await coordinator.async_set_off_peak_time(weekday_start="23:00")

        mock_api_client_local.async_set_off_peak_time.assert_called_once_with(
            TEST_CHARGER_ID,
            weekday_start="23:00",
            weekday_end="06:00",
            weekend_start="00:00",
            weekend_end="00:00",
        )
        mock_refresh.assert_called_once()


async def test_async_set_off_peak_time_no_data(
    hass: HomeAssistant,
    mock_api_client_local,
    coordinator: WellborneDataUpdateCoordinator,
) -> None:
    """Test setting off-peak time with no data uses defaults."""
    coordinator.data = None

    with patch.object(coordinator, "async_request_refresh", new_callable=AsyncMock):
        await coordinator.async_set_off_peak_time(weekday_start="22:00", weekday_end="07:00")

        mock_api_client_local.async_set_off_peak_time.assert_called_once_with(
            TEST_CHARGER_ID,
            weekday_start="22:00",
            weekday_end="07:00",
            weekend_start="00:00",
            weekend_end="00:00",
        )


# =============================================================================
# LCD and Low Power Reserve Tests
# =============================================================================


async def test_async_set_lcd_enabled(
    hass: HomeAssistant,
    mock_api_client_local,
    coordinator: WellborneDataUpdateCoordinator,
) -> None:
    """Test enabling LCD display."""
    with patch.object(coordinator, "async_request_refresh", new_callable=AsyncMock) as mock_refresh:
        await coordinator.async_set_lcd_enabled(enabled=True)

        mock_api_client_local.async_set_lcd_enabled.assert_called_once_with(TEST_CHARGER_ID, enabled=True)
        mock_refresh.assert_called_once()


async def test_async_set_lcd_disabled(
    hass: HomeAssistant,
    mock_api_client_local,
    coordinator: WellborneDataUpdateCoordinator,
) -> None:
    """Test disabling LCD display."""
    with patch.object(coordinator, "async_request_refresh", new_callable=AsyncMock):
        await coordinator.async_set_lcd_enabled(enabled=False)

        mock_api_client_local.async_set_lcd_enabled.assert_called_once_with(TEST_CHARGER_ID, enabled=False)


async def test_async_set_low_power_reserve_enabled(
    hass: HomeAssistant,
    mock_api_client_local,
    coordinator: WellborneDataUpdateCoordinator,
) -> None:
    """Test enabling low power reserve."""
    with patch.object(coordinator, "async_request_refresh", new_callable=AsyncMock) as mock_refresh:
        await coordinator.async_set_low_power_reserve_enabled(enabled=True)

        mock_api_client_local.async_set_low_power_reserve.assert_called_once_with(TEST_CHARGER_ID, enabled=True)
        mock_refresh.assert_called_once()


async def test_async_set_low_power_reserve_disabled(
    hass: HomeAssistant,
    mock_api_client_local,
    coordinator: WellborneDataUpdateCoordinator,
) -> None:
    """Test disabling low power reserve."""
    with patch.object(coordinator, "async_request_refresh", new_callable=AsyncMock):
        await coordinator.async_set_low_power_reserve_enabled(enabled=False)

        mock_api_client_local.async_set_low_power_reserve.assert_called_once_with(TEST_CHARGER_ID, enabled=False)


# =============================================================================
# Load Balancing Tests
# =============================================================================


async def test_async_set_load_balancing_enabled(
    hass: HomeAssistant,
    mock_api_client_local,
    coordinator: WellborneDataUpdateCoordinator,
    mock_wellborne_data: WellborneData,
) -> None:
    """Test enabling load balancing preserves max current."""
    coordinator.data = mock_wellborne_data
    coordinator.data.load_balancing.max_current = 25

    with patch.object(coordinator, "async_request_refresh", new_callable=AsyncMock) as mock_refresh:
        await coordinator.async_set_load_balancing_enabled(enabled=True)

        mock_api_client_local.async_set_load_balancing.assert_called_once_with(
            TEST_CHARGER_ID, enabled=True, max_current=25
        )
        mock_refresh.assert_called_once()


async def test_async_set_load_balancing_disabled(
    hass: HomeAssistant,
    mock_api_client_local,
    coordinator: WellborneDataUpdateCoordinator,
    mock_wellborne_data: WellborneData,
) -> None:
    """Test disabling load balancing."""
    coordinator.data = mock_wellborne_data
    coordinator.data.load_balancing.max_current = 20

    with patch.object(coordinator, "async_request_refresh", new_callable=AsyncMock):
        await coordinator.async_set_load_balancing_enabled(enabled=False)

        mock_api_client_local.async_set_load_balancing.assert_called_once_with(
            TEST_CHARGER_ID, enabled=False, max_current=20
        )


async def test_async_set_load_balancing_enabled_no_data(
    hass: HomeAssistant,
    mock_api_client_local,
    coordinator: WellborneDataUpdateCoordinator,
) -> None:
    """Test enabling load balancing with no data uses default max current."""
    coordinator.data = None

    with patch.object(coordinator, "async_request_refresh", new_callable=AsyncMock):
        await coordinator.async_set_load_balancing_enabled(enabled=True)

        mock_api_client_local.async_set_load_balancing.assert_called_once_with(
            TEST_CHARGER_ID, enabled=True, max_current=32
        )


async def test_async_set_load_balancing_current(
    hass: HomeAssistant,
    mock_api_client_local,
    coordinator: WellborneDataUpdateCoordinator,
    mock_wellborne_data: WellborneData,
) -> None:
    """Test setting load balancing current preserves enabled state."""
    coordinator.data = mock_wellborne_data
    coordinator.data.load_balancing.enabled = True

    with patch.object(coordinator, "async_request_refresh", new_callable=AsyncMock) as mock_refresh:
        await coordinator.async_set_load_balancing_current(20)

        mock_api_client_local.async_set_load_balancing.assert_called_once_with(
            TEST_CHARGER_ID, enabled=True, max_current=20
        )
        mock_refresh.assert_called_once()


async def test_async_set_load_balancing_current_no_data(
    hass: HomeAssistant,
    mock_api_client_local,
    coordinator: WellborneDataUpdateCoordinator,
) -> None:
    """Test setting load balancing current with no data uses enabled=False."""
    coordinator.data = None

    with patch.object(coordinator, "async_request_refresh", new_callable=AsyncMock):
        await coordinator.async_set_load_balancing_current(16)

        mock_api_client_local.async_set_load_balancing.assert_called_once_with(
            TEST_CHARGER_ID, enabled=False, max_current=16
        )


# =============================================================================
# Offline Detection Tests
# =============================================================================


async def test_offline_detection_marks_offline_after_threshold(
    hass: HomeAssistant,
    mock_api_client_local,
    coordinator: WellborneDataUpdateCoordinator,
) -> None:
    """Test coordinator marks charger offline after OFFLINE_TIMEOUT_COUNT consecutive connection errors."""
    mock_api_client_local.async_get_charger_data.side_effect = ApiConnectionError("Connection refused")

    # Before threshold: still considered online
    assert coordinator.is_online is True

    for _ in range(OFFLINE_TIMEOUT_COUNT - 1):
        with pytest.raises(UpdateFailed):
            await coordinator._async_update_data()
        assert coordinator.is_online is True, "Should still be online before threshold"

    # The OFFLINE_TIMEOUT_COUNT-th failure crosses the threshold
    with pytest.raises(UpdateFailed):
        await coordinator._async_update_data()

    assert coordinator.is_online is False


async def test_offline_detection_restores_online_after_success(
    hass: HomeAssistant,
    mock_api_client_local,
    coordinator: WellborneDataUpdateCoordinator,
    mock_wellborne_data: WellborneData,
) -> None:
    """Test coordinator restores online state and resets counter after a successful update."""
    mock_api_client_local.async_get_charger_data.side_effect = ApiConnectionError("timeout")

    # Drive coordinator offline
    for _ in range(OFFLINE_TIMEOUT_COUNT):
        with pytest.raises(UpdateFailed):
            await coordinator._async_update_data()

    assert coordinator.is_online is False
    assert coordinator._consecutive_timeouts == OFFLINE_TIMEOUT_COUNT

    # A successful call restores online status
    mock_api_client_local.async_get_charger_data.side_effect = None
    mock_api_client_local.async_get_charger_data.return_value = mock_wellborne_data

    result = await coordinator._async_update_data()

    assert result is mock_wellborne_data
    assert coordinator.is_online is True
    assert coordinator._consecutive_timeouts == 0


# =============================================================================
# Adaptive Polling Tests
# =============================================================================


async def test_adaptive_polling_uses_charging_interval_when_charging(
    hass: HomeAssistant,
    mock_api_client_local,
    coordinator: WellborneDataUpdateCoordinator,
    mock_wellborne_data_charging: WellborneData,
) -> None:
    """Test coordinator switches to charging poll interval when charger is actively charging."""
    mock_api_client_local.async_get_charger_data.return_value = mock_wellborne_data_charging
    assert mock_wellborne_data_charging.status.is_charging is True

    await coordinator._async_update_data()

    assert coordinator.update_interval == timedelta(seconds=CHARGING_POLL_INTERVAL)


async def test_adaptive_polling_uses_idle_interval_when_not_charging(
    hass: HomeAssistant,
    mock_api_client_local,
    coordinator: WellborneDataUpdateCoordinator,
    mock_wellborne_data: WellborneData,
) -> None:
    """Test coordinator switches to idle poll interval when charger is not charging."""
    mock_api_client_local.async_get_charger_data.return_value = mock_wellborne_data
    assert mock_wellborne_data.status.is_charging is False

    await coordinator._async_update_data()

    assert coordinator.update_interval == timedelta(seconds=IDLE_POLL_INTERVAL)


# =============================================================================
# Timeout Handling Tests
# =============================================================================


async def test_async_update_data_timeout_raises_update_failed(
    hass: HomeAssistant,
    mock_api_client_local,
    coordinator: WellborneDataUpdateCoordinator,
) -> None:
    """Test that a bare TimeoutError from the coordinator timeout raises UpdateFailed, not a bare exception."""
    mock_api_client_local.async_get_charger_data.side_effect = TimeoutError()

    with pytest.raises(UpdateFailed, match="timed out"):
        await coordinator._async_update_data()


async def test_async_update_data_timeout_increments_consecutive_timeouts(
    hass: HomeAssistant,
    mock_api_client_local,
    coordinator: WellborneDataUpdateCoordinator,
) -> None:
    """Test that a TimeoutError increments _consecutive_timeouts like ApiConnectionError does."""
    mock_api_client_local.async_get_charger_data.side_effect = TimeoutError()

    with pytest.raises(UpdateFailed):
        await coordinator._async_update_data()

    assert coordinator._consecutive_timeouts == 1


async def test_async_update_data_timeout_marks_offline_after_threshold(
    hass: HomeAssistant,
    mock_api_client_local,
    coordinator: WellborneDataUpdateCoordinator,
) -> None:
    """Test that repeated TimeoutErrors trigger offline detection the same way ApiConnectionError does."""
    mock_api_client_local.async_get_charger_data.side_effect = TimeoutError()

    assert coordinator.is_online is True

    for _ in range(OFFLINE_TIMEOUT_COUNT - 1):
        with pytest.raises(UpdateFailed):
            await coordinator._async_update_data()
        assert coordinator.is_online is True

    with pytest.raises(UpdateFailed):
        await coordinator._async_update_data()


# =============================================================================
# Charger Offline (upstream message) Tests
# =============================================================================


async def test_charger_offline_marks_offline_after_threshold(
    hass: HomeAssistant,
    mock_api_client_local,
    coordinator: WellborneDataUpdateCoordinator,
) -> None:
    """Test a ChargerOfflineError marks the charger offline after OFFLINE_TIMEOUT_COUNT failures.

    With no cached data, each failure raises UpdateFailed; the charger stays online before
    the threshold and flips offline once it is crossed.
    """
    mock_api_client_local.async_get_charger_data.side_effect = ChargerOfflineError("Charger is not online")

    assert coordinator.data is None
    assert coordinator.is_online is True

    for _ in range(OFFLINE_TIMEOUT_COUNT - 1):
        with pytest.raises(UpdateFailed, match="Charger offline"):
            await coordinator._async_update_data()
        assert coordinator.is_online is True, "Should still be online before threshold"

    with pytest.raises(UpdateFailed, match="Charger offline"):
        await coordinator._async_update_data()

    assert coordinator.is_online is False


async def test_charger_offline_keeps_entities_alive_with_cached_data(
    hass: HomeAssistant,
    mock_api_client_local,
    coordinator: WellborneDataUpdateCoordinator,
    mock_wellborne_data: WellborneData,
) -> None:
    """Test that with prior data, ChargerOfflineError returns cached data and backs off polling."""
    coordinator.data = mock_wellborne_data
    mock_api_client_local.async_get_charger_data.side_effect = ChargerOfflineError("Charger offline")

    # Each cycle returns the cached data instead of raising.
    for _ in range(OFFLINE_TIMEOUT_COUNT):
        result = await coordinator._async_update_data()
        assert result is mock_wellborne_data

    # Past the threshold: marked offline and backed off to the offline poll cadence.
    assert coordinator.is_online is False
    assert coordinator.update_interval == timedelta(seconds=OFFLINE_POLL_INTERVAL)


async def test_charger_offline_restores_online_after_success(
    hass: HomeAssistant,
    mock_api_client_local,
    coordinator: WellborneDataUpdateCoordinator,
    mock_wellborne_data: WellborneData,
) -> None:
    """Test that a success after a ChargerOfflineError restores online state and resets the counter."""
    mock_api_client_local.async_get_charger_data.side_effect = ChargerOfflineError("offline")

    for _ in range(OFFLINE_TIMEOUT_COUNT):
        with pytest.raises(UpdateFailed):
            await coordinator._async_update_data()

    assert coordinator.is_online is False
    assert coordinator._consecutive_timeouts == OFFLINE_TIMEOUT_COUNT

    mock_api_client_local.async_get_charger_data.side_effect = None
    mock_api_client_local.async_get_charger_data.return_value = mock_wellborne_data

    result = await coordinator._async_update_data()

    assert result is mock_wellborne_data
    assert coordinator.is_online is True
    assert coordinator._consecutive_timeouts == 0
