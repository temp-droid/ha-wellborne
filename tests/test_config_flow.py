"""Tests for the Wellborne config flow."""

from __future__ import annotations

from unittest.mock import AsyncMock, patch

from homeassistant.config_entries import SOURCE_REAUTH, SOURCE_RECONFIGURE, SOURCE_USER
from homeassistant.const import CONF_EMAIL, CONF_PASSWORD
from homeassistant.core import HomeAssistant
from homeassistant.data_entry_flow import FlowResultType
import pytest
from pytest_homeassistant_custom_component.common import MockConfigEntry

from custom_components.wellborne.api import (
    ApiConnectionError,
    ApiResponseError,
    AuthenticationError,
    ChargerInfo,
    SessionExpiredError,
)
from custom_components.wellborne.const import DOMAIN

from .conftest import TEST_CHARGER_ID, TEST_EMAIL, TEST_PASSWORD


@pytest.fixture
def mock_setup_entry() -> AsyncMock:
    """Mock async_setup_entry."""
    with patch(
        "custom_components.wellborne.async_setup_entry",
        return_value=True,
    ) as mock_setup:
        yield mock_setup


async def test_user_flow_success(
    hass: HomeAssistant,
    mock_setup_entry: AsyncMock,
) -> None:
    """Test successful user flow creates config entry."""
    # Start the config flow
    result = await hass.config_entries.flow.async_init(
        DOMAIN,
        context={"source": SOURCE_USER},
    )

    assert result["type"] is FlowResultType.FORM
    assert result["step_id"] == "user"
    assert result["errors"] == {}

    # Mock the API client
    with patch("custom_components.wellborne.config_flow.WellborneApiClient") as mock_client_class:
        mock_client = AsyncMock()
        mock_client.async_login.return_value = {"token": "test_token"}
        mock_client.async_get_chargers.return_value = [
            ChargerInfo(
                charger_id=TEST_CHARGER_ID,
                alias="Test Charger",
                model="EVA-22S",
                owner=1,
                connector_num=1,
                max_power=22.0,
            )
        ]
        mock_client.close.return_value = None
        mock_client_class.return_value = mock_client

        # Submit the form
        result = await hass.config_entries.flow.async_configure(
            result["flow_id"],
            user_input={
                CONF_EMAIL: TEST_EMAIL,
                CONF_PASSWORD: TEST_PASSWORD,
            },
        )

    assert result["type"] is FlowResultType.CREATE_ENTRY
    assert result["title"] == TEST_EMAIL
    assert result["data"] == {
        CONF_EMAIL: TEST_EMAIL,
        CONF_PASSWORD: TEST_PASSWORD,
    }
    assert result["result"].unique_id == TEST_EMAIL

    # Verify setup was called
    assert mock_setup_entry.called


async def test_user_flow_invalid_auth(
    hass: HomeAssistant,
) -> None:
    """Test user flow with invalid credentials shows error."""
    result = await hass.config_entries.flow.async_init(
        DOMAIN,
        context={"source": SOURCE_USER},
    )

    assert result["type"] is FlowResultType.FORM
    assert result["step_id"] == "user"

    # Mock the API client to raise AuthenticationError
    with patch("custom_components.wellborne.config_flow.WellborneApiClient") as mock_client_class:
        mock_client = AsyncMock()
        mock_client.async_login.side_effect = AuthenticationError("Invalid credentials")
        mock_client.close.return_value = None
        mock_client_class.return_value = mock_client

        # Submit the form with wrong credentials
        result = await hass.config_entries.flow.async_configure(
            result["flow_id"],
            user_input={
                CONF_EMAIL: TEST_EMAIL,
                CONF_PASSWORD: "wrong_password",
            },
        )

    # Should show form again with error
    assert result["type"] is FlowResultType.FORM
    assert result["step_id"] == "user"
    assert result["errors"] == {"base": "invalid_auth"}


async def test_user_flow_cannot_connect(
    hass: HomeAssistant,
) -> None:
    """Test user flow when API is unreachable shows error."""
    result = await hass.config_entries.flow.async_init(
        DOMAIN,
        context={"source": SOURCE_USER},
    )

    assert result["type"] is FlowResultType.FORM
    assert result["step_id"] == "user"

    # Mock the API client to raise ApiConnectionError
    with patch("custom_components.wellborne.config_flow.WellborneApiClient") as mock_client_class:
        mock_client = AsyncMock()
        mock_client.async_login.side_effect = ApiConnectionError("Connection failed")
        mock_client.close.return_value = None
        mock_client_class.return_value = mock_client

        # Submit the form
        result = await hass.config_entries.flow.async_configure(
            result["flow_id"],
            user_input={
                CONF_EMAIL: TEST_EMAIL,
                CONF_PASSWORD: TEST_PASSWORD,
            },
        )

    # Should show form again with connection error
    assert result["type"] is FlowResultType.FORM
    assert result["step_id"] == "user"
    assert result["errors"] == {"base": "cannot_connect"}


async def test_user_flow_already_configured(
    hass: HomeAssistant,
    mock_config_entry: MockConfigEntry,
) -> None:
    """Test user flow aborts when account is already configured."""
    # Add existing config entry
    mock_config_entry.add_to_hass(hass)

    result = await hass.config_entries.flow.async_init(
        DOMAIN,
        context={"source": SOURCE_USER},
    )

    assert result["type"] is FlowResultType.FORM
    assert result["step_id"] == "user"

    # Mock the API client for successful login
    with patch("custom_components.wellborne.config_flow.WellborneApiClient") as mock_client_class:
        mock_client = AsyncMock()
        mock_client.async_login.return_value = {"token": "test_token"}
        mock_client.async_get_chargers.return_value = [
            ChargerInfo(
                charger_id=TEST_CHARGER_ID,
                alias="Test Charger",
                model="EVA-22S",
                owner=1,
                connector_num=1,
                max_power=22.0,
            )
        ]
        mock_client.close.return_value = None
        mock_client_class.return_value = mock_client

        # Submit the form with same email
        result = await hass.config_entries.flow.async_configure(
            result["flow_id"],
            user_input={
                CONF_EMAIL: TEST_EMAIL,
                CONF_PASSWORD: TEST_PASSWORD,
            },
        )

    # Should abort because already configured
    assert result["type"] is FlowResultType.ABORT
    assert result["reason"] == "already_configured"


async def test_reauth_flow_success(
    hass: HomeAssistant,
    mock_config_entry: MockConfigEntry,
    mock_setup_entry: AsyncMock,
) -> None:
    """Test reauth flow updates credentials successfully."""
    # Add existing config entry
    mock_config_entry.add_to_hass(hass)

    # Start reauth flow
    result = await hass.config_entries.flow.async_init(
        DOMAIN,
        context={
            "source": SOURCE_REAUTH,
            "entry_id": mock_config_entry.entry_id,
        },
        data=mock_config_entry.data,
    )

    assert result["type"] is FlowResultType.FORM
    assert result["step_id"] == "reauth_confirm"

    # Mock the API client for successful login
    with patch("custom_components.wellborne.config_flow.WellborneApiClient") as mock_client_class:
        mock_client = AsyncMock()
        mock_client.async_login.return_value = {"token": "new_token"}
        mock_client.close.return_value = None
        mock_client_class.return_value = mock_client

        # Submit new password
        result = await hass.config_entries.flow.async_configure(
            result["flow_id"],
            user_input={
                CONF_PASSWORD: "new_password",
            },
        )

    assert result["type"] is FlowResultType.ABORT
    assert result["reason"] == "reauth_successful"

    # Verify credentials were updated
    assert mock_config_entry.data[CONF_PASSWORD] == "new_password"


async def test_reauth_flow_invalid_auth(
    hass: HomeAssistant,
    mock_config_entry: MockConfigEntry,
) -> None:
    """Test reauth flow with wrong password shows error."""
    # Add existing config entry
    mock_config_entry.add_to_hass(hass)

    # Start reauth flow
    result = await hass.config_entries.flow.async_init(
        DOMAIN,
        context={
            "source": SOURCE_REAUTH,
            "entry_id": mock_config_entry.entry_id,
        },
        data=mock_config_entry.data,
    )

    assert result["type"] is FlowResultType.FORM
    assert result["step_id"] == "reauth_confirm"

    # Mock the API client to raise AuthenticationError
    with patch("custom_components.wellborne.config_flow.WellborneApiClient") as mock_client_class:
        mock_client = AsyncMock()
        mock_client.async_login.side_effect = AuthenticationError("Invalid credentials")
        mock_client.close.return_value = None
        mock_client_class.return_value = mock_client

        # Submit wrong password
        result = await hass.config_entries.flow.async_configure(
            result["flow_id"],
            user_input={
                CONF_PASSWORD: "wrong_password",
            },
        )

    # Should show form again with error
    assert result["type"] is FlowResultType.FORM
    assert result["step_id"] == "reauth_confirm"
    assert result["errors"] == {"base": "invalid_auth"}


async def test_user_flow_unknown_error(
    hass: HomeAssistant,
) -> None:
    """Test user flow handles unexpected errors gracefully."""
    result = await hass.config_entries.flow.async_init(
        DOMAIN,
        context={"source": SOURCE_USER},
    )

    assert result["type"] is FlowResultType.FORM
    assert result["step_id"] == "user"

    # Mock the API client to raise unexpected exception
    with patch("custom_components.wellborne.config_flow.WellborneApiClient") as mock_client_class:
        mock_client = AsyncMock()
        mock_client.async_login.side_effect = RuntimeError("Unexpected error")
        mock_client.close.return_value = None
        mock_client_class.return_value = mock_client

        # Submit the form
        result = await hass.config_entries.flow.async_configure(
            result["flow_id"],
            user_input={
                CONF_EMAIL: TEST_EMAIL,
                CONF_PASSWORD: TEST_PASSWORD,
            },
        )

    # Should show form again with unknown error
    assert result["type"] is FlowResultType.FORM
    assert result["step_id"] == "user"
    assert result["errors"] == {"base": "unknown"}


# =============================================================================
# Options Flow Tests
# =============================================================================


async def test_options_flow_shows_entity_selector(
    hass: HomeAssistant,
    mock_config_entry: MockConfigEntry,
) -> None:
    """Test options flow shows entity selector for EV integration."""
    mock_config_entry.add_to_hass(hass)

    # Start options flow directly without setting up the entry
    result = await hass.config_entries.options.async_init(mock_config_entry.entry_id)

    assert result["type"] is FlowResultType.FORM
    assert result["step_id"] == "init"

    # Check that the schema contains the end_of_charge_entity selector
    schema_keys = [str(k) for k in result["data_schema"].schema]
    assert "end_of_charge_entity" in schema_keys


async def test_options_flow_saves_entity_selection(
    hass: HomeAssistant,
    mock_config_entry: MockConfigEntry,
) -> None:
    """Test options flow saves selected entity."""
    mock_config_entry.add_to_hass(hass)

    # Start options flow
    result = await hass.config_entries.options.async_init(mock_config_entry.entry_id)

    assert result["type"] is FlowResultType.FORM
    assert result["step_id"] == "init"

    # Submit the form with an entity ID
    result = await hass.config_entries.options.async_configure(
        result["flow_id"],
        user_input={"end_of_charge_entity": "sensor.car_end_of_charge"},
    )

    assert result["type"] is FlowResultType.CREATE_ENTRY
    assert result["data"]["end_of_charge_entity"] == "sensor.car_end_of_charge"


async def test_options_flow_shows_current_value(
    hass: HomeAssistant,
) -> None:
    """Test options flow shows current entity selection."""
    # Create a config entry with existing options
    entry = MockConfigEntry(
        domain=DOMAIN,
        title=TEST_EMAIL,
        data={
            CONF_EMAIL: TEST_EMAIL,
            CONF_PASSWORD: TEST_PASSWORD,
        },
        options={"end_of_charge_entity": "sensor.car_end_of_charge"},
        unique_id=TEST_EMAIL,
        version=1,
    )
    entry.add_to_hass(hass)

    # Start options flow
    result = await hass.config_entries.options.async_init(entry.entry_id)

    assert result["type"] is FlowResultType.FORM
    assert result["step_id"] == "init"

    # Check the schema has the default value from options
    schema = result["data_schema"].schema
    for key in schema:
        if str(key) == "end_of_charge_entity":
            assert key.default() == "sensor.car_end_of_charge"
            break
    else:
        pytest.fail("end_of_charge_entity not found in schema")


# =============================================================================
# User Flow Error Branches (ApiResponseError / SessionExpiredError / TimeoutError)
# =============================================================================


async def test_user_flow_api_response_error(
    hass: HomeAssistant,
) -> None:
    """Test user flow shows cannot_connect when ApiResponseError is raised."""
    result = await hass.config_entries.flow.async_init(
        DOMAIN,
        context={"source": SOURCE_USER},
    )

    assert result["type"] is FlowResultType.FORM
    assert result["step_id"] == "user"

    with patch("custom_components.wellborne.config_flow.WellborneApiClient") as mock_client_class:
        mock_client = AsyncMock()
        mock_client.async_login.side_effect = ApiResponseError("Server error", result_code=500)
        mock_client.close.return_value = None
        mock_client_class.return_value = mock_client

        result = await hass.config_entries.flow.async_configure(
            result["flow_id"],
            user_input={
                CONF_EMAIL: TEST_EMAIL,
                CONF_PASSWORD: TEST_PASSWORD,
            },
        )

    assert result["type"] is FlowResultType.FORM
    assert result["step_id"] == "user"
    assert result["errors"] == {"base": "cannot_connect"}


async def test_user_flow_session_expired_error(
    hass: HomeAssistant,
) -> None:
    """Test user flow shows invalid_auth when SessionExpiredError is raised.

    SessionExpiredError is a subclass of AuthenticationError, so it is caught
    by the AuthenticationError handler and maps to 'invalid_auth'.
    """
    result = await hass.config_entries.flow.async_init(
        DOMAIN,
        context={"source": SOURCE_USER},
    )

    assert result["type"] is FlowResultType.FORM
    assert result["step_id"] == "user"

    with patch("custom_components.wellborne.config_flow.WellborneApiClient") as mock_client_class:
        mock_client = AsyncMock()
        mock_client.async_login.side_effect = SessionExpiredError("Session expired")
        mock_client.close.return_value = None
        mock_client_class.return_value = mock_client

        result = await hass.config_entries.flow.async_configure(
            result["flow_id"],
            user_input={
                CONF_EMAIL: TEST_EMAIL,
                CONF_PASSWORD: TEST_PASSWORD,
            },
        )

    # SessionExpiredError subclasses AuthenticationError → caught first → invalid_auth
    assert result["type"] is FlowResultType.FORM
    assert result["step_id"] == "user"
    assert result["errors"] == {"base": "invalid_auth"}


async def test_user_flow_timeout_error(
    hass: HomeAssistant,
) -> None:
    """Test user flow shows cannot_connect when TimeoutError is raised."""
    result = await hass.config_entries.flow.async_init(
        DOMAIN,
        context={"source": SOURCE_USER},
    )

    assert result["type"] is FlowResultType.FORM
    assert result["step_id"] == "user"

    with patch("custom_components.wellborne.config_flow.WellborneApiClient") as mock_client_class:
        mock_client = AsyncMock()
        mock_client.async_login.side_effect = TimeoutError("Request timed out")
        mock_client.close.return_value = None
        mock_client_class.return_value = mock_client

        result = await hass.config_entries.flow.async_configure(
            result["flow_id"],
            user_input={
                CONF_EMAIL: TEST_EMAIL,
                CONF_PASSWORD: TEST_PASSWORD,
            },
        )

    assert result["type"] is FlowResultType.FORM
    assert result["step_id"] == "user"
    assert result["errors"] == {"base": "cannot_connect"}


# =============================================================================
# Reauth Flow Error Branches (ApiConnectionError / ApiResponseError / TimeoutError)
# =============================================================================


async def test_reauth_flow_cannot_connect(
    hass: HomeAssistant,
    mock_config_entry: MockConfigEntry,
) -> None:
    """Test reauth flow shows cannot_connect when API is unreachable."""
    mock_config_entry.add_to_hass(hass)

    result = await hass.config_entries.flow.async_init(
        DOMAIN,
        context={
            "source": SOURCE_REAUTH,
            "entry_id": mock_config_entry.entry_id,
        },
        data=mock_config_entry.data,
    )

    assert result["type"] is FlowResultType.FORM
    assert result["step_id"] == "reauth_confirm"

    with patch("custom_components.wellborne.config_flow.WellborneApiClient") as mock_client_class:
        mock_client = AsyncMock()
        mock_client.async_login.side_effect = ApiConnectionError("Connection refused")
        mock_client.close.return_value = None
        mock_client_class.return_value = mock_client

        result = await hass.config_entries.flow.async_configure(
            result["flow_id"],
            user_input={CONF_PASSWORD: TEST_PASSWORD},
        )

    assert result["type"] is FlowResultType.FORM
    assert result["step_id"] == "reauth_confirm"
    assert result["errors"] == {"base": "cannot_connect"}


async def test_reauth_flow_api_response_error(
    hass: HomeAssistant,
    mock_config_entry: MockConfigEntry,
) -> None:
    """Test reauth flow shows cannot_connect when ApiResponseError is raised."""
    mock_config_entry.add_to_hass(hass)

    result = await hass.config_entries.flow.async_init(
        DOMAIN,
        context={
            "source": SOURCE_REAUTH,
            "entry_id": mock_config_entry.entry_id,
        },
        data=mock_config_entry.data,
    )

    assert result["type"] is FlowResultType.FORM
    assert result["step_id"] == "reauth_confirm"

    with patch("custom_components.wellborne.config_flow.WellborneApiClient") as mock_client_class:
        mock_client = AsyncMock()
        mock_client.async_login.side_effect = ApiResponseError("Server error", result_code=500)
        mock_client.close.return_value = None
        mock_client_class.return_value = mock_client

        result = await hass.config_entries.flow.async_configure(
            result["flow_id"],
            user_input={CONF_PASSWORD: TEST_PASSWORD},
        )

    assert result["type"] is FlowResultType.FORM
    assert result["step_id"] == "reauth_confirm"
    assert result["errors"] == {"base": "cannot_connect"}


async def test_reauth_flow_unknown_error(
    hass: HomeAssistant,
    mock_config_entry: MockConfigEntry,
) -> None:
    """Test reauth flow shows unknown error when unexpected exception occurs."""
    mock_config_entry.add_to_hass(hass)

    result = await hass.config_entries.flow.async_init(
        DOMAIN,
        context={
            "source": SOURCE_REAUTH,
            "entry_id": mock_config_entry.entry_id,
        },
        data=mock_config_entry.data,
    )

    assert result["type"] is FlowResultType.FORM
    assert result["step_id"] == "reauth_confirm"

    with patch("custom_components.wellborne.config_flow.WellborneApiClient") as mock_client_class:
        mock_client = AsyncMock()
        mock_client.async_login.side_effect = RuntimeError("Unexpected error")
        mock_client.close.return_value = None
        mock_client_class.return_value = mock_client

        result = await hass.config_entries.flow.async_configure(
            result["flow_id"],
            user_input={CONF_PASSWORD: TEST_PASSWORD},
        )

    assert result["type"] is FlowResultType.FORM
    assert result["step_id"] == "reauth_confirm"
    assert result["errors"] == {"base": "unknown"}


# =============================================================================
# Reconfigure Flow Tests
# =============================================================================


async def test_reconfigure_flow_shows_form_prefilled_with_current_email(
    hass: HomeAssistant,
    mock_config_entry: MockConfigEntry,
) -> None:
    """Test reconfigure flow shows form pre-filled with the current email."""
    mock_config_entry.add_to_hass(hass)

    result = await hass.config_entries.flow.async_init(
        DOMAIN,
        context={
            "source": SOURCE_RECONFIGURE,
            "entry_id": mock_config_entry.entry_id,
        },
    )

    assert result["type"] is FlowResultType.FORM
    assert result["step_id"] == "reconfigure"

    # Verify schema is pre-filled with current email
    schema = result["data_schema"].schema
    for key in schema:
        if str(key) == CONF_EMAIL:
            assert key.default() == TEST_EMAIL
            break
    else:
        pytest.fail("email not found in reconfigure schema")


async def test_reconfigure_flow_success(
    hass: HomeAssistant,
    mock_config_entry: MockConfigEntry,
) -> None:
    """Test reconfigure flow updates entry and reloads on valid credentials."""
    mock_config_entry.add_to_hass(hass)

    result = await hass.config_entries.flow.async_init(
        DOMAIN,
        context={
            "source": SOURCE_RECONFIGURE,
            "entry_id": mock_config_entry.entry_id,
        },
    )

    assert result["type"] is FlowResultType.FORM
    assert result["step_id"] == "reconfigure"

    new_email = "new@example.com"
    new_password = "new_password"  # noqa: S105

    with patch("custom_components.wellborne.config_flow.WellborneApiClient") as mock_client_class:
        mock_client = AsyncMock()
        mock_client.async_login.return_value = {"token": "new_token"}
        mock_client.close.return_value = None
        mock_client_class.return_value = mock_client

        result = await hass.config_entries.flow.async_configure(
            result["flow_id"],
            user_input={
                CONF_EMAIL: new_email,
                CONF_PASSWORD: new_password,
            },
        )

    # async_update_reload_and_abort returns ABORT with "reconfigure_successful"
    assert result["type"] is FlowResultType.ABORT
    assert result["reason"] == "reconfigure_successful"

    # Verify entry was updated
    assert mock_config_entry.data[CONF_EMAIL] == new_email
    assert mock_config_entry.data[CONF_PASSWORD] == new_password


async def test_reconfigure_flow_invalid_auth(
    hass: HomeAssistant,
    mock_config_entry: MockConfigEntry,
) -> None:
    """Test reconfigure flow shows invalid_auth error on bad credentials."""
    mock_config_entry.add_to_hass(hass)

    result = await hass.config_entries.flow.async_init(
        DOMAIN,
        context={
            "source": SOURCE_RECONFIGURE,
            "entry_id": mock_config_entry.entry_id,
        },
    )

    assert result["type"] is FlowResultType.FORM
    assert result["step_id"] == "reconfigure"

    with patch("custom_components.wellborne.config_flow.WellborneApiClient") as mock_client_class:
        mock_client = AsyncMock()
        mock_client.async_login.side_effect = AuthenticationError("Bad credentials")
        mock_client.close.return_value = None
        mock_client_class.return_value = mock_client

        result = await hass.config_entries.flow.async_configure(
            result["flow_id"],
            user_input={
                CONF_EMAIL: TEST_EMAIL,
                CONF_PASSWORD: "wrong_password",
            },
        )

    assert result["type"] is FlowResultType.FORM
    assert result["step_id"] == "reconfigure"
    assert result["errors"] == {"base": "invalid_auth"}


async def test_reconfigure_flow_cannot_connect(
    hass: HomeAssistant,
    mock_config_entry: MockConfigEntry,
) -> None:
    """Test reconfigure flow shows cannot_connect when API is unreachable."""
    mock_config_entry.add_to_hass(hass)

    result = await hass.config_entries.flow.async_init(
        DOMAIN,
        context={
            "source": SOURCE_RECONFIGURE,
            "entry_id": mock_config_entry.entry_id,
        },
    )

    assert result["type"] is FlowResultType.FORM
    assert result["step_id"] == "reconfigure"

    with patch("custom_components.wellborne.config_flow.WellborneApiClient") as mock_client_class:
        mock_client = AsyncMock()
        mock_client.async_login.side_effect = ApiConnectionError("Connection refused")
        mock_client.close.return_value = None
        mock_client_class.return_value = mock_client

        result = await hass.config_entries.flow.async_configure(
            result["flow_id"],
            user_input={
                CONF_EMAIL: TEST_EMAIL,
                CONF_PASSWORD: TEST_PASSWORD,
            },
        )

    assert result["type"] is FlowResultType.FORM
    assert result["step_id"] == "reconfigure"
    assert result["errors"] == {"base": "cannot_connect"}


async def test_reconfigure_flow_api_response_error(
    hass: HomeAssistant,
    mock_config_entry: MockConfigEntry,
) -> None:
    """Test reconfigure flow shows cannot_connect when ApiResponseError is raised."""
    mock_config_entry.add_to_hass(hass)

    result = await hass.config_entries.flow.async_init(
        DOMAIN,
        context={
            "source": SOURCE_RECONFIGURE,
            "entry_id": mock_config_entry.entry_id,
        },
    )

    assert result["type"] is FlowResultType.FORM
    assert result["step_id"] == "reconfigure"

    with patch("custom_components.wellborne.config_flow.WellborneApiClient") as mock_client_class:
        mock_client = AsyncMock()
        mock_client.async_login.side_effect = ApiResponseError("Server error", result_code=500)
        mock_client.close.return_value = None
        mock_client_class.return_value = mock_client

        result = await hass.config_entries.flow.async_configure(
            result["flow_id"],
            user_input={
                CONF_EMAIL: TEST_EMAIL,
                CONF_PASSWORD: TEST_PASSWORD,
            },
        )

    assert result["type"] is FlowResultType.FORM
    assert result["step_id"] == "reconfigure"
    assert result["errors"] == {"base": "cannot_connect"}


async def test_reconfigure_flow_unknown_error(
    hass: HomeAssistant,
    mock_config_entry: MockConfigEntry,
) -> None:
    """Test reconfigure flow shows unknown error on unexpected exception."""
    mock_config_entry.add_to_hass(hass)

    result = await hass.config_entries.flow.async_init(
        DOMAIN,
        context={
            "source": SOURCE_RECONFIGURE,
            "entry_id": mock_config_entry.entry_id,
        },
    )

    assert result["type"] is FlowResultType.FORM
    assert result["step_id"] == "reconfigure"

    with patch("custom_components.wellborne.config_flow.WellborneApiClient") as mock_client_class:
        mock_client = AsyncMock()
        mock_client.async_login.side_effect = RuntimeError("Unexpected error")
        mock_client.close.return_value = None
        mock_client_class.return_value = mock_client

        result = await hass.config_entries.flow.async_configure(
            result["flow_id"],
            user_input={
                CONF_EMAIL: TEST_EMAIL,
                CONF_PASSWORD: TEST_PASSWORD,
            },
        )

    assert result["type"] is FlowResultType.FORM
    assert result["step_id"] == "reconfigure"
    assert result["errors"] == {"base": "unknown"}
