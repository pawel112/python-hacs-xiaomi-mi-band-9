"""Config flow for Xiaomi Mi Band 9."""
import voluptuous as vol
from homeassistant import config_entries
from . import DOMAIN


class MiBand9ConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle config flow."""

    VERSION = 1

    async def async_step_user(self, user_input=None):
        if self._async_current_entries():
            return self.async_abort(reason="single_instance_allowed")
        if user_input is not None:
            return self.async_create_entry(title="Xiaomi Mi Band 9", data={})
        return self.async_show_form(step_id="user", data_schema=vol.Schema({}))
