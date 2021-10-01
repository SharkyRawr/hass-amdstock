"""Sensor platform for AMD GPU Stock."""
from homeassistant.components.sensor import SensorEntity
from homeassistant.const import ATTR_ATTRIBUTION
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from . import get_coordinator
from .const import DOMAIN
from .stock import check_stock


async def async_setup_entry(hass, config_entry, async_add_entities):
    coordinator = await get_coordinator(hass)
        
    # keys: title, price, stock
    
    async_add_entities(
        StockSensor(coordinator, card)
        for card in coordinator.data
    )
    
    
class StockSensor(CoordinatorEntity, SensorEntity):
    def __init__(self, coordinator, card):
        super().__init__(coordinator)
        self._attr_extra_state_attributes = {ATTR_ATTRIBUTION: "AMD.com"}
        self._attr_unique_id = f"amd-gpu-stock-{card}"
        self.info_type = card
        self._attr_name = card
        self._attr_icon = 'mdi:expansion-card'
        
    @property
    def available(self):
        """Return if sensor is available."""
        return self.coordinator.last_update_success
    
    
    @property
    def native_value(self):
        """State of the sensor."""
        if self.coordinator.data[self._attr_name]['stock'] == 'Out of Stock':
            return  self.coordinator.data[self._attr_name]['stock']
        else:
            return "In Stock"

    @property
    def state_attributes(self):
        return dict(stock=self.coordinator.data[self._attr_name]['stock'])
    
    @property
    def device_info(self):
        """Device info."""
        return {
            "identifiers": {(DOMAIN,)},
            "manufacturer": "AMD.com",
            "model": "GPU Stock",
            "default_name": "AMD GPU Stock",
            "entry_type": "service",
        }

    
