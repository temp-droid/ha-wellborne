"""Tests for the Wellborne integration setup and unload."""

from __future__ import annotations

from unittest.mock import AsyncMock, patch

from homeassistant.core import HomeAssistant
from homeassistant.exceptions import ConfigEntryAuthFailed, ConfigEntryNotReady
import pytest
from pytest_homeassistant_custom_component.common import MockConfigEntry

from custom_components.wellborne import async_setup_entry, async_unload_entry
from custom_components.wellborne.api import ApiConnectionError, AuthenticationError
from custom_components.wellborne.const import DOMAIN

from .conftest import TEST_CHARGER_ID


@pytest.fixture
def mock_api_client_for_init(mock_wellborne_data):
    """Create a mock API client for init tests."""
    with patch("custom_components.wellborne.WellborneApiClient") as mock_class:
        client = AsyncMock()
        client.async_login.return_value = {"token": "test_token"}
        client.async_get_chargers.return_value = [mock_wellborne_data.charger]
        client.async_logout.return_value = None
        client.async_get_charger_data.return_value = mock_wellborne_data
        mock_class.return_value = client
        yield client


@pytest.fixture
def mock_coordinator_for_init(mock_wellborne_data, mock_api_client_for_init):
    """Create a mock coordinator for init tests."""
    with patch("custom_components.wellborne.WellborneDataUpdateCoordinator") as mock_class:
        coordinator = AsyncMock()
        coordinator.async_config_entry_first_refresh.return_value = None
        coordinator.data = mock_wellborne_data
        coordinator.charger_id = TEST_CHARGER_ID
        coordinator.client = mock_api_client_for_init  # Link client to coordinator
        mock_class.return_value = coordinator
        yield coordinator


@pytest.fixture
def mock_forward_entry_setups():
    """Mock the platform forward setup."""
    with patch(
        "homeassistant.config_entries.ConfigEntries.async_forward_entry_setups",
        return_value=None,
    ) as mock:
        yield mock


@pytest.fixture
def mock_unload_platforms():
    """Mock the platform unload."""
    with patch(
        "homeassistant.config_entries.ConfigEntries.async_unload_platforms",
        return_value=True,
    ) as mock:
        yield mock


async def test_setup_entry_success(
    hass: HomeAssistant,
    mock_config_entry: MockConfigEntry,
    mock_api_client_for_init,
    mock_coordinator_for_init,
    mock_forward_entry_setups,
) -> None:
    """Test successful setup of config entry."""
    mock_config_entry.add_to_hass(hass)

    result = await async_setup_entry(hass, mock_config_entry)

    assert result is True
    assert mock_config_entry.entry_id in hass.data[DOMAIN]
    mock_api_client_for_init.async_login.assert_called_once()
    mock_forward_entry_setups.assert_called_once()


async def test_setup_entry_auth_failure(
    hass: HomeAssistant,
    mock_config_entry: MockConfigEntry,
) -> None:
    """Test setup fails with invalid credentials."""
    mock_config_entry.add_to_hass(hass)

    with patch("custom_components.wellborne.WellborneApiClient") as mock_class:
        client = AsyncMock()
        client.async_login.side_effect = AuthenticationError("Invalid credentials")
        mock_class.return_value = client

        with pytest.raises(ConfigEntryAuthFailed):
            await async_setup_entry(hass, mock_config_entry)


async def test_setup_entry_connection_failure(
    hass: HomeAssistant,
    mock_config_entry: MockConfigEntry,
) -> None:
    """Test setup fails when API is unreachable."""
    mock_config_entry.add_to_hass(hass)

    with patch("custom_components.wellborne.WellborneApiClient") as mock_class:
        client = AsyncMock()
        client.async_login.side_effect = ApiConnectionError("Cannot connect")
        mock_class.return_value = client

        with pytest.raises(ConfigEntryNotReady):
            await async_setup_entry(hass, mock_config_entry)


async def test_setup_entry_no_chargers(
    hass: HomeAssistant,
    mock_config_entry: MockConfigEntry,
) -> None:
    """Test setup fails when no chargers are found."""
    mock_config_entry.add_to_hass(hass)

    with patch("custom_components.wellborne.WellborneApiClient") as mock_class:
        client = AsyncMock()
        client.async_login.return_value = {"token": "test_token"}
        client.async_get_chargers.return_value = []  # No chargers
        mock_class.return_value = client

        with pytest.raises(ConfigEntryNotReady, match="No chargers found"):
            await async_setup_entry(hass, mock_config_entry)


async def test_unload_entry(
    hass: HomeAssistant,
    mock_config_entry: MockConfigEntry,
    mock_api_client_for_init,
    mock_coordinator_for_init,
    mock_forward_entry_setups,
    mock_unload_platforms,
) -> None:
    """Test unloading a config entry."""
    mock_config_entry.add_to_hass(hass)

    # Set up first
    await async_setup_entry(hass, mock_config_entry)
    assert mock_config_entry.entry_id in hass.data[DOMAIN]

    # Now unload
    result = await async_unload_entry(hass, mock_config_entry)

    assert result is True
    assert mock_config_entry.entry_id not in hass.data[DOMAIN]
    mock_api_client_for_init.async_logout.assert_called_once()
    mock_unload_platforms.assert_called_once()


async def test_unload_entry_succeeds_when_logout_raises(
    hass: HomeAssistant,
    mock_config_entry: MockConfigEntry,
    mock_api_client_for_init,
    mock_coordinator_for_init,
    mock_forward_entry_setups,
    mock_unload_platforms,
) -> None:
    """Test that unload returns True and cleans up even when logout raises an unexpected error."""
    mock_config_entry.add_to_hass(hass)

    # Set up first
    await async_setup_entry(hass, mock_config_entry)
    assert mock_config_entry.entry_id in hass.data[DOMAIN]

    # Simulate an unexpected non-WellborneError from logout
    mock_api_client_for_init.async_logout.side_effect = RuntimeError("boom")

    # Unload must still succeed
    result = await async_unload_entry(hass, mock_config_entry)

    assert result is True
    # Entry must be removed — no orphan coordinator
    assert mock_config_entry.entry_id not in hass.data[DOMAIN]
