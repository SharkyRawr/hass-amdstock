from homeassistant import config_entries, data_entry_flow
from homeassistant.data_entry_flow import FlowResult
from typing import Any
import voluptuous as vol


@config_entries.HANDLERS.register("amdstock")
class AMDStockConfigFlow(config_entries.ConfigFlow):
    VERSION = 1

    async def async_step_user(
            self, user_input: dict[str, Any] = None
        ) -> FlowResult:
        errors: dict[str, str] = {}
        
        if user_input is not None:
            await self.async_set_unique_id("AMD GPU Stock")
            self._abort_if_unique_id_configured()
            return self.async_create_entry(
                title="AMD GPU Stock", data=user_input
            )
        
        return self.async_show_form(
            step_id="user",
            errors=errors,
        )