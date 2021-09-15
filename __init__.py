import logging
from datetime import timedelta
import async_timeout

from .const import DOMAIN
from .config_flow import AMDStockConfigFlow
from .stock import check_stock

from homeassistant.core import HomeAssistant
from homeassistant.config_entries import ConfigEntry
from homeassistant.helpers.typing import ConfigType
from homeassistant.helpers import aiohttp_client, update_coordinator


PLATFORMS = ["sensor"]


async def async_setup(hass, config):
    """Register the API with the HTTP interface."""
    return True


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    hass.config_entries.async_setup_platforms(entry, PLATFORMS)
    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    return await hass.config_entries.async_unload_platforms(entry, PLATFORMS)


async def get_coordinator(
    hass: HomeAssistant,
) -> update_coordinator.DataUpdateCoordinator:
    """Get the data update coordinator."""
    if DOMAIN in hass.data:
        return hass.data[DOMAIN]
    
    
    async def async_get_stock():
        with async_timeout.timeout(30):
            return await check_stock()
    
    hass.data[DOMAIN] = update_coordinator.DataUpdateCoordinator(
        hass,
        logging.getLogger(__name__),
        name=DOMAIN,
        update_method=async_get_stock,
        update_interval=timedelta(minutes=1),
    )
    
    await hass.data[DOMAIN].async_refresh()
    return hass.data[DOMAIN]
    