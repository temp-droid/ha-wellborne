"""Tests for the Wellborne button platform."""

from __future__ import annotations

from unittest.mock import AsyncMock, MagicMock, PropertyMock

from homeassistant.core import HomeAssistant
import pytest
from pytest_homeassistant_custom_component.common import MockConfigEntry

from custom_components.wellborne.button import async_setup_entry
from custom_components.wellborne.const import DOMAIN

from .conftest import TEST_CHARGER_ID


# Note: button press_fn callables are zero-arg lambdas that invoke the coordinator
# methods with their defaults (e.g. connector_id="1"), so asserting the correct
# coordinator method was called once is sufficient at this layer. The argument
# contract (connector_id) is exercised in the coordinator/client tests.
@pytest.fixture
def mock_coordinator(mock_wellborne_data):
    """Create a mock coordinator."""
    coordinator = MagicMock()
    coordinator.data = mock_wellborne_data
    coordinator.charger_id = TEST_CHARGER_ID
    coordinator.last_update_success = True
    type(coordinator).available = PropertyMock(return_value=True)
    coordinator.async_start_charging = AsyncMock()
    coordinator.async_stop_charging = AsyncMock()
    coordinator.async_unlock_connector = AsyncMock()
    coordinator.async_prompt_charge = AsyncMock()
    return coordinator


async def test_start_charging_button(
    hass: HomeAssistant,
    mock_config_entry: MockConfigEntry,
    mock_coordinator,
) -> None:
    """Test start charging button calls API on press."""
    mock_config_entry.add_to_hass(hass)

    hass.data.setdefault(DOMAIN, {})
    hass.data[DOMAIN][mock_config_entry.entry_id] = mock_coordinator

    entities_added = []

    def capture_entities(entities):
        entities_added.extend(entities)

    await async_setup_entry(hass, mock_config_entry, capture_entities)
    await hass.async_block_till_done()

    # Find the start charging button
    start_button = next((e for e in entities_added if "start_charging" in e.unique_id), None)
    assert start_button is not None

    # Press the button
    await start_button.async_press()

    # Verify API was called
    mock_coordinator.async_start_charging.assert_called_once()


async def test_stop_charging_button(
    hass: HomeAssistant,
    mock_config_entry: MockConfigEntry,
    mock_coordinator,
) -> None:
    """Test stop charging button calls API on press."""
    mock_config_entry.add_to_hass(hass)

    hass.data.setdefault(DOMAIN, {})
    hass.data[DOMAIN][mock_config_entry.entry_id] = mock_coordinator

    entities_added = []

    def capture_entities(entities):
        entities_added.extend(entities)

    await async_setup_entry(hass, mock_config_entry, capture_entities)
    await hass.async_block_till_done()

    # Find the stop charging button
    stop_button = next((e for e in entities_added if "stop_charging" in e.unique_id), None)
    assert stop_button is not None

    # Press the button
    await stop_button.async_press()

    # Verify API was called
    mock_coordinator.async_stop_charging.assert_called_once()


async def test_unlock_connector_button(
    hass: HomeAssistant,
    mock_config_entry: MockConfigEntry,
    mock_coordinator,
) -> None:
    """Test unlock connector button calls API on press."""
    mock_config_entry.add_to_hass(hass)

    hass.data.setdefault(DOMAIN, {})
    hass.data[DOMAIN][mock_config_entry.entry_id] = mock_coordinator

    entities_added = []

    def capture_entities(entities):
        entities_added.extend(entities)

    await async_setup_entry(hass, mock_config_entry, capture_entities)
    await hass.async_block_till_done()

    # Find the unlock connector button
    unlock_button = next((e for e in entities_added if "unlock_connector" in e.unique_id), None)
    assert unlock_button is not None

    # Press the button
    await unlock_button.async_press()

    # Verify API was called
    mock_coordinator.async_unlock_connector.assert_called_once()


async def test_prompt_charge_button(
    hass: HomeAssistant,
    mock_config_entry: MockConfigEntry,
    mock_coordinator,
) -> None:
    """Test prompt charge button calls API on press (immediate charge bypassing delay)."""
    mock_config_entry.add_to_hass(hass)

    hass.data.setdefault(DOMAIN, {})
    hass.data[DOMAIN][mock_config_entry.entry_id] = mock_coordinator

    entities_added = []

    def capture_entities(entities):
        entities_added.extend(entities)

    await async_setup_entry(hass, mock_config_entry, capture_entities)
    await hass.async_block_till_done()

    # Find the prompt charge button
    prompt_button = next((e for e in entities_added if "prompt_charge" in e.unique_id), None)
    assert prompt_button is not None

    # Press the button
    await prompt_button.async_press()

    # Verify API was called
    mock_coordinator.async_prompt_charge.assert_called_once()


async def test_button_unique_ids(
    hass: HomeAssistant,
    mock_config_entry: MockConfigEntry,
    mock_coordinator,
) -> None:
    """Test buttons have correct unique IDs."""
    mock_config_entry.add_to_hass(hass)

    hass.data.setdefault(DOMAIN, {})
    hass.data[DOMAIN][mock_config_entry.entry_id] = mock_coordinator

    entities_added = []

    def capture_entities(entities):
        entities_added.extend(entities)

    await async_setup_entry(hass, mock_config_entry, capture_entities)
    await hass.async_block_till_done()

    # Check that all entities have unique IDs starting with the charger ID
    for entity in entities_added:
        assert entity.unique_id.startswith(TEST_CHARGER_ID)
