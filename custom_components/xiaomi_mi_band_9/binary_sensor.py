"""Binary sensor platform for Xiaomi Mi Band 9."""
from __future__ import annotations

from homeassistant.components.binary_sensor import (
    BinarySensorDeviceClass,
    BinarySensorEntity,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant, callback
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.event import async_track_state_change_event

from .device import DEVICE_INFO


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    async_add_entities([MiBand9Connected(hass)], update_before_add=True)


class MiBand9Connected(BinarySensorEntity):
    _attr_has_entity_name = True
    _attr_name = "Połączony"
    _attr_unique_id = "miband9_connected"
    _attr_device_class = BinarySensorDeviceClass.CONNECTIVITY
    _attr_icon = "mdi:watch"
    _attr_should_poll = False
    _attr_device_info = DEVICE_INFO

    SOURCE = "sensor.miband_trigger_6"

    def __init__(self, hass: HomeAssistant) -> None:
        self.hass = hass

    async def async_added_to_hass(self) -> None:
        self.async_on_remove(
            async_track_state_change_event(
                self.hass, [self.SOURCE], self._handle_state_change,
            )
        )
        self._update_state()

    @callback
    def _handle_state_change(self, event) -> None:
        self._update_state()
        self.async_write_ha_state()

    def _update_state(self) -> None:
        from datetime import datetime, timezone, timedelta
        state = self.hass.states.get(self.SOURCE)
        if state is None or state.state in ("unknown", "unavailable", ""):
            self._attr_is_on = None
            return
        try:
            last_conn = datetime.fromisoformat(state.state)
            now = datetime.now(tz=timezone.utc)
            self._attr_is_on = (now - last_conn.astimezone(timezone.utc)) < timedelta(minutes=5)
        except (ValueError, TypeError):
            self._attr_is_on = None

    @property
    def available(self) -> bool:
        state = self.hass.states.get(self.SOURCE)
        return state is not None and state.state not in ("unknown", "unavailable")