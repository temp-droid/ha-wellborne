"""Pytest fixtures for Wellborne tests."""

from __future__ import annotations

from collections.abc import Generator
from datetime import UTC, datetime, timedelta
from typing import Any
from unittest.mock import AsyncMock, MagicMock, PropertyMock, patch

from homeassistant.const import CONF_EMAIL, CONF_PASSWORD
import pytest
from pytest_homeassistant_custom_component.common import MockConfigEntry

from custom_components.wellborne.api import (
    ChargerInfo,
    ChargerStatus,
    DelayedChargingSettings,
    MeterValues,
    OffPeakSettings,
    ScheduledChargingTask,
    WellborneApiClient,
    WellborneData,
)
from custom_components.wellborne.const import DOMAIN

# Test constants
TEST_EMAIL = "test@example.com"
TEST_PASSWORD = "test_password"  # noqa: S105
TEST_CHARGER_ID = "TEST12345"
TEST_CHARGER_ALIAS = "Test Charger"


@pytest.fixture(autouse=True)
def auto_enable_custom_integrations(enable_custom_integrations: None) -> None:
    """Enable custom integrations in Home Assistant."""


@pytest.fixture
def mock_charger_info() -> ChargerInfo:
    """Return mock charger info."""
    return ChargerInfo(
        charger_id=TEST_CHARGER_ID,
        alias=TEST_CHARGER_ALIAS,
        model="EVA-22S",
        owner=1,
        connector_num=1,
        max_power=22.0,
        bluetooth_enabled=False,
        create_time="2024-01-01 00:00:00",
    )


@pytest.fixture
def mock_charger_status() -> ChargerStatus:
    """Return mock charger status."""
    return ChargerStatus(
        is_charging=False,
        solar_mode="0",
        max_current=16.0,
        connector_lock=False,
        lcd_enabled=True,
        low_power_reserve=False,
    )


@pytest.fixture
def mock_meter_values() -> MeterValues:
    """Return mock meter values."""
    return MeterValues(
        voltage=230.0,
        voltage_l2=230.0,
        voltage_l3=230.0,
        current=16.0,
        current_l2=16.0,
        current_l3=16.0,
        energy=10.5,
        power=3680.0,
        phase="3-phase",
        timestamp="2024-01-01 12:00:00",
    )


@pytest.fixture
def mock_delayed_charging() -> DelayedChargingSettings:
    """Return mock delayed charging settings."""
    return DelayedChargingSettings(
        enabled=False,
        delay_time=0,
        select_status=0,
    )


@pytest.fixture
def mock_scheduled_charging() -> ScheduledChargingTask:
    """Return mock scheduled charging task."""
    return ScheduledChargingTask(
        enabled=False,
        cycle="",
        cycle_time="",
        expiry_date=None,
        connection_type="1",
    )


@pytest.fixture
def mock_off_peak() -> OffPeakSettings:
    """Return mock off-peak charging settings."""
    return OffPeakSettings(
        enabled=False,
        weekday_start="22:00",
        weekday_end="06:00",
        weekend_start="00:00",
        weekend_end="00:00",
    )


@pytest.fixture
def mock_wellborne_data(
    mock_charger_info: ChargerInfo,
    mock_charger_status: ChargerStatus,
    mock_delayed_charging: DelayedChargingSettings,
    mock_scheduled_charging: ScheduledChargingTask,
    mock_off_peak: OffPeakSettings,
) -> WellborneData:
    """Return mock Wellborne data."""
    return WellborneData(
        charger=mock_charger_info,
        status=mock_charger_status,
        meter_values=None,
        delayed_charging=mock_delayed_charging,
        scheduled_charging=mock_scheduled_charging,
        off_peak=mock_off_peak,
        transaction_id=None,
    )


@pytest.fixture
def mock_wellborne_data_charging(
    mock_wellborne_data: WellborneData,
    mock_meter_values: MeterValues,
) -> WellborneData:
    """Return mock Wellborne data with active charging."""
    mock_wellborne_data.status.is_charging = True
    mock_wellborne_data.meter_values = mock_meter_values
    mock_wellborne_data.transaction_id = "12345"
    return mock_wellborne_data


@pytest.fixture
def mock_api_client(mock_wellborne_data: WellborneData) -> Generator[AsyncMock]:
    """Create a mock API client."""
    with patch(
        "custom_components.wellborne.api.client.WellborneApiClient",
        autospec=True,
    ) as mock_class:
        client = AsyncMock(spec=WellborneApiClient)

        # Authentication
        client.async_login.return_value = {
            "token": "test_token",
            "email": TEST_EMAIL,
        }
        client.async_logout.return_value = None
        client.is_authenticated = True

        # Charger management
        client.async_get_chargers.return_value = [mock_wellborne_data.charger]
        client.async_is_charging.return_value = False
        client.async_unlock_connector.return_value = None

        # Charging control
        client.async_start_charging.return_value = None
        client.async_stop_charging.return_value = None
        client.async_prompt_charge.return_value = None

        # Configuration
        client.async_get_charger_config.return_value = {
            "maximumOutputCurrent": "16.00",
            "connectorLock": "true",
            "lcd": "Enable",
            "lowPowerReserve": "Disable",
        }
        client.async_get_home_config.return_value = {
            "solarChargingMode": "0",
            "delayedCharging": {
                "delayTime": 0,
                "status": 2,
            },
        }
        client.async_set_max_current.return_value = None
        client.async_set_solar_mode.return_value = None
        client.async_set_connector_lock.return_value = None

        # Scheduled/Delayed charging
        client.async_get_scheduled_charging.return_value = mock_wellborne_data.scheduled_charging
        client.async_get_delayed_charging.return_value = mock_wellborne_data.delayed_charging

        # Combined data
        client.async_get_charger_data.return_value = mock_wellborne_data

        # Transactions
        client.async_get_transactions.return_value = []

        # Close
        client.close.return_value = None

        mock_class.return_value = client
        yield client


@pytest.fixture
def mock_config_entry() -> MockConfigEntry:
    """Create a mock config entry with default options."""
    return MockConfigEntry(
        domain=DOMAIN,
        title=TEST_EMAIL,
        data={
            CONF_EMAIL: TEST_EMAIL,
            CONF_PASSWORD: TEST_PASSWORD,
        },
        options={
            "vehicle_efficiency": 6.0,
            "charging_poll_interval": 30,
            "idle_poll_interval": 120,
        },
        unique_id=TEST_EMAIL,
        version=1,
    )


@pytest.fixture
def mock_setup_entry() -> Generator[AsyncMock]:
    """Mock async_setup_entry."""
    with patch(
        "custom_components.wellborne.async_setup_entry",
        return_value=True,
    ) as mock_setup:
        yield mock_setup


# API Response fixtures for raw API testing
@pytest.fixture
def api_login_response() -> dict[str, Any]:
    """Return mock login response."""
    return {
        "result": 0,
        "msg": "Login successful",
        "obj": {
            "id": 123,
            "email": TEST_EMAIL,
            "country": "Example Country",
            "timezone": "Region/City(UTC+00:00)",
            "token": "Bearer eyJhbGciOiJIUzUxMiJ9.test_token",
        },
    }


@pytest.fixture
def api_charger_list_response() -> dict[str, Any]:
    """Return mock charger list response."""
    return {
        "result": 0,
        "msg": "operate successfully",
        "obj": [
            {
                "owner": 1,
                "isVa1NovoNano": False,
                "createTime": "2024-01-01 00:00:00",
                "bluetoothEnable": 0,
                "chargerId": TEST_CHARGER_ID,
                "connectorStandard": {"country": "", "connector": ""},
                "connectorModel": ["AC"],
                "alias": TEST_CHARGER_ALIAS,
                "model": "AC",
                "connectorNum": 1,
                "chargePointModelPower": 22,
            }
        ],
    }


@pytest.fixture
def api_is_charging_response() -> dict[str, Any]:
    """Return mock is_charging response."""
    return {
        "result": 0,
        "msg": "operate successfully",
        "obj": False,
    }


@pytest.fixture
def api_charger_config_response() -> dict[str, Any]:
    """Return mock charger config response."""
    return {
        "result": 0,
        "msg": "operate successfully",
        "obj": {
            "solarChargingMode": "0",
            "solarLimitChargingPower": "3.96",
            "connectorLock": "true",
            "lcd": "Enable",
            "chargingMode": "1",
            "allowChargingTime": "00:00-00:00",
            "maximumOutputCurrent": "16.00",
            "maxPower": None,
            "lowPowerReserve": "Disable",
            "fullContinueCharge": "Disable",
            "language": {"describe": "English", "value": "English"},
        },
    }


@pytest.fixture
def api_home_config_response() -> dict[str, Any]:
    """Return mock home config response."""
    return {
        "result": 0,
        "msg": "operate successfully",
        "obj": {
            "delayedCharging": {
                "delayTime": 0,
                "status": 2,
                "chargerId": TEST_CHARGER_ID,
                "selectStatus": 0,
            },
            "solarChargingMode": "0",
        },
    }


@pytest.fixture
def api_error_response() -> dict[str, Any]:
    """Return mock error response."""
    return {
        "result": 500,
        "msg": "Operation failed",
        "obj": None,
    }


@pytest.fixture
def api_auth_error_response() -> dict[str, Any]:
    """Return mock authentication error response."""
    return {
        "result": 500,
        "msg": "Invalid credentials",
        "obj": None,
    }


@pytest.fixture
def api_session_expired_response() -> dict[str, Any]:
    """Return mock session expired response."""
    return {
        "result": 10000,
        "msg": "Session expired",
        "obj": None,
    }


# =============================================================================
# Transaction fixtures for Lifetime Energy sensor tests
# =============================================================================


@pytest.fixture
def mock_transactions() -> list[dict[str, Any]]:
    """Return mock transaction history."""
    return [
        {
            "id": 1,
            "chargerId": TEST_CHARGER_ID,
            "energy": 15.5,
            "startTime": "2024-01-01 08:00:00",
            "endTime": "2024-01-01 10:00:00",
            "status": "completed",
        },
        {
            "id": 2,
            "chargerId": TEST_CHARGER_ID,
            "energy": 22.3,
            "startTime": "2024-01-02 18:00:00",
            "endTime": "2024-01-02 22:00:00",
            "status": "completed",
        },
        {
            "id": 3,
            "chargerId": TEST_CHARGER_ID,
            "energy": 8.7,
            "startTime": "2024-01-03 12:00:00",
            "endTime": "2024-01-03 13:30:00",
            "status": "completed",
        },
    ]


# =============================================================================
# Session Duration fixtures
# =============================================================================


@pytest.fixture
def mock_wellborne_data_with_session_start(
    mock_wellborne_data_charging: WellborneData,
) -> WellborneData:
    """Return mock Wellborne data with a session start ~90 minutes ago.

    The wall-clock value is only a sane default. Tests asserting an exact session
    duration must override ``session_start_time`` under ``freeze_time`` (see
    ``test_session_duration_sensor_shows_minutes_when_charging``) to stay deterministic.
    """
    session_start = datetime.now(tz=UTC) - timedelta(minutes=90)
    mock_wellborne_data_charging.session_start_time = session_start
    return mock_wellborne_data_charging


@pytest.fixture
def mock_coordinator_with_session_start(mock_wellborne_data_with_session_start):
    """Create a mock coordinator with session start time."""
    coordinator = MagicMock()
    coordinator.data = mock_wellborne_data_with_session_start
    coordinator.charger_id = TEST_CHARGER_ID
    coordinator.last_update_success = True
    type(coordinator).available = PropertyMock(return_value=True)
    return coordinator


# =============================================================================
# Charger Status fixtures
# =============================================================================


@pytest.fixture
def mock_wellborne_data_with_delayed_charging(
    mock_wellborne_data: WellborneData,
) -> WellborneData:
    """Return mock Wellborne data with delayed charging enabled."""
    mock_wellborne_data.delayed_charging.enabled = True
    mock_wellborne_data.delayed_charging.delay_time = 3600  # 1 hour delay
    return mock_wellborne_data


@pytest.fixture
def mock_coordinator_with_delayed_charging(mock_wellborne_data_with_delayed_charging):
    """Create a mock coordinator with delayed charging enabled."""
    coordinator = MagicMock()
    coordinator.data = mock_wellborne_data_with_delayed_charging
    coordinator.charger_id = TEST_CHARGER_ID
    coordinator.last_update_success = True
    type(coordinator).available = PropertyMock(return_value=True)
    return coordinator
