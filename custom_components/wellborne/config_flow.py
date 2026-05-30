"""Config flow for Wellborne EV Charger integration."""

from __future__ import annotations

import logging
from typing import TYPE_CHECKING, Any

from homeassistant.config_entries import ConfigFlow, ConfigFlowResult, OptionsFlow
from homeassistant.const import CONF_EMAIL, CONF_PASSWORD
from homeassistant.helpers.selector import EntitySelector, EntitySelectorConfig
import voluptuous as vol

from .api import ApiConnectionError, ApiResponseError, AuthenticationError, WellborneApiClient
from .const import (
    CHARGING_POLL_INTERVAL,
    CONF_CHARGING_POLL_INTERVAL,
    CONF_END_OF_CHARGE_ENTITY,
    CONF_IDLE_POLL_INTERVAL,
    CONF_VEHICLE_EFFICIENCY,
    DEFAULT_VEHICLE_EFFICIENCY,
    DOMAIN,
    IDLE_POLL_INTERVAL,
)

if TYPE_CHECKING:
    from homeassistant.config_entries import ConfigEntry

_LOGGER = logging.getLogger(__name__)

USER_SCHEMA = vol.Schema(
    {
        vol.Required(CONF_EMAIL): str,
        vol.Required(CONF_PASSWORD): str,
    }
)

REAUTH_SCHEMA = vol.Schema(
    {
        vol.Required(CONF_PASSWORD): str,
    }
)

RECONFIGURE_SCHEMA = vol.Schema(
    {
        vol.Required(CONF_EMAIL): str,
        vol.Required(CONF_PASSWORD): str,
    }
)


class WellborneConfigFlow(ConfigFlow, domain=DOMAIN):
    """Handle a config flow for Wellborne."""

    VERSION = 1

    def __init__(self) -> None:
        """Initialize the config flow."""
        self._reauth_entry: ConfigEntry | None = None

    @staticmethod
    def async_get_options_flow(_config_entry: ConfigEntry) -> WellborneOptionsFlow:
        """Get the options flow handler."""
        return WellborneOptionsFlow()

    async def async_step_user(
        self,
        user_input: dict[str, Any] | None = None,
    ) -> ConfigFlowResult:
        """Handle the initial step."""
        errors: dict[str, str] = {}

        if user_input is not None:
            email = user_input[CONF_EMAIL]
            password = user_input[CONF_PASSWORD]

            client = WellborneApiClient(email=email)

            try:
                await client.async_login(password)
            except AuthenticationError:
                errors["base"] = "invalid_auth"
            except (ApiConnectionError, TimeoutError):
                errors["base"] = "cannot_connect"
            except ApiResponseError as err:
                _LOGGER.warning("API error during login: %s", err)
                errors["base"] = "cannot_connect"
            except Exception:
                _LOGGER.exception("Unexpected error during login")
                errors["base"] = "unknown"
            else:
                # Set unique ID and abort if already configured
                await self.async_set_unique_id(email)
                self._abort_if_unique_id_configured()

                return self.async_create_entry(
                    title=email,
                    data={
                        CONF_EMAIL: email,
                        CONF_PASSWORD: password,
                    },
                )
            finally:
                await client.close()

        return self.async_show_form(
            step_id="user",
            data_schema=USER_SCHEMA,
            errors=errors,
        )

    async def async_step_reauth(
        self,
        _entry_data: dict[str, Any],
    ) -> ConfigFlowResult:
        """Handle reauth when credentials expire."""
        entry_id = self.context.get("entry_id")
        if entry_id:
            self._reauth_entry = self.hass.config_entries.async_get_entry(entry_id)
        return await self.async_step_reauth_confirm()

    async def async_step_reauth_confirm(
        self,
        user_input: dict[str, Any] | None = None,
    ) -> ConfigFlowResult:
        """Handle reauth confirmation."""
        errors: dict[str, str] = {}

        if user_input is not None and self._reauth_entry is not None:
            email = self._reauth_entry.data[CONF_EMAIL]
            password = user_input[CONF_PASSWORD]

            client = WellborneApiClient(email=email)

            try:
                await client.async_login(password)
            except AuthenticationError:
                errors["base"] = "invalid_auth"
            except (ApiConnectionError, TimeoutError):
                errors["base"] = "cannot_connect"
            except ApiResponseError as err:
                _LOGGER.warning("API error during reauth: %s", err)
                errors["base"] = "cannot_connect"
            except Exception:
                _LOGGER.exception("Unexpected error during reauth")
                errors["base"] = "unknown"
            else:
                # Update entry with new credentials
                self.hass.config_entries.async_update_entry(
                    self._reauth_entry,
                    data={
                        **self._reauth_entry.data,
                        CONF_PASSWORD: password,
                    },
                )
                await self.hass.config_entries.async_reload(self._reauth_entry.entry_id)
                return self.async_abort(reason="reauth_successful")
            finally:
                await client.close()

        return self.async_show_form(
            step_id="reauth_confirm",
            data_schema=REAUTH_SCHEMA,
            errors=errors,
        )

    async def async_step_reconfigure(
        self,
        user_input: dict[str, Any] | None = None,
    ) -> ConfigFlowResult:
        """Handle reconfiguration of credentials."""
        errors: dict[str, str] = {}
        reconfigure_entry = self._get_reconfigure_entry()

        if user_input is not None:
            email = user_input[CONF_EMAIL]
            password = user_input[CONF_PASSWORD]

            client = WellborneApiClient(email=email)

            try:
                await client.async_login(password)
            except AuthenticationError:
                errors["base"] = "invalid_auth"
            except (ApiConnectionError, TimeoutError):
                errors["base"] = "cannot_connect"
            except ApiResponseError as err:
                _LOGGER.warning("API error during reconfigure: %s", err)
                errors["base"] = "cannot_connect"
            except Exception:
                _LOGGER.exception("Unexpected error during reconfigure")
                errors["base"] = "unknown"
            else:
                # Update entry with new credentials
                return self.async_update_reload_and_abort(
                    reconfigure_entry,
                    title=email,
                    data={
                        **reconfigure_entry.data,
                        CONF_EMAIL: email,
                        CONF_PASSWORD: password,
                    },
                )
            finally:
                await client.close()

        # Pre-fill with current email
        current_email = reconfigure_entry.data.get(CONF_EMAIL, "")
        schema = vol.Schema(
            {
                vol.Required(CONF_EMAIL, default=current_email): str,
                vol.Required(CONF_PASSWORD): str,
            }
        )

        return self.async_show_form(
            step_id="reconfigure",
            data_schema=schema,
            errors=errors,
        )


class WellborneOptionsFlow(OptionsFlow):
    """Handle Wellborne options flow."""

    async def async_step_init(
        self,
        user_input: dict[str, Any] | None = None,
    ) -> ConfigFlowResult:
        """Handle options flow."""
        if user_input is not None:
            return self.async_create_entry(title="", data=user_input)

        # Get current option values with defaults
        current_entity = self.config_entry.options.get(CONF_END_OF_CHARGE_ENTITY, "")
        current_efficiency = self.config_entry.options.get(CONF_VEHICLE_EFFICIENCY, DEFAULT_VEHICLE_EFFICIENCY)
        current_charging_poll = self.config_entry.options.get(CONF_CHARGING_POLL_INTERVAL, CHARGING_POLL_INTERVAL)
        current_idle_poll = self.config_entry.options.get(CONF_IDLE_POLL_INTERVAL, IDLE_POLL_INTERVAL)

        schema = vol.Schema(
            {
                vol.Optional(
                    CONF_END_OF_CHARGE_ENTITY,
                    default=current_entity,
                ): EntitySelector(
                    EntitySelectorConfig(
                        domain=["sensor"],
                    )
                ),
                vol.Optional(
                    CONF_VEHICLE_EFFICIENCY,
                    default=current_efficiency,
                ): vol.All(vol.Coerce(float), vol.Range(min=3.0, max=10.0)),
                vol.Optional(
                    CONF_CHARGING_POLL_INTERVAL,
                    default=current_charging_poll,
                ): vol.All(vol.Coerce(int), vol.Range(min=10, max=300)),
                vol.Optional(
                    CONF_IDLE_POLL_INTERVAL,
                    default=current_idle_poll,
                ): vol.All(vol.Coerce(int), vol.Range(min=30, max=600)),
            }
        )

        return self.async_show_form(step_id="init", data_schema=schema)
