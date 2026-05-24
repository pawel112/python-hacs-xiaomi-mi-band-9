"""Sensor platform for Xiaomi Mi Band 9."""
from __future__ import annotations

from homeassistant.components.sensor import (
    SensorDeviceClass,
    SensorEntity,
    SensorStateClass,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant, callback
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.event import async_track_state_change_event
from homeassistant.util.dt import as_local
from datetime import datetime

from .device import DEVICE_INFO
from . import DOMAIN


SENSORS = [
    {
        "unique_id": "miband9_battery",
        "name": "Bateria",
        "source": "sensor.miband_battery",
        "unit": "%",
        "device_class": SensorDeviceClass.BATTERY,
        "state_class": SensorStateClass.MEASUREMENT,
        "icon": "mdi:battery-heart",
    },
    {
        "unique_id": "miband9_steps",
        "name": "Kroki",
        "source": "sensor.miband_steps",
        "unit": "kroki",
        "device_class": None,
        "state_class": SensorStateClass.TOTAL_INCREASING,
        "icon": "mdi:walk",
    },
    {
        "unique_id": "miband9_heartrate",
        "name": "Tętno",
        "source": "sensor.miband_heartrate",
        "unit": "bpm",
        "device_class": None,
        "state_class": SensorStateClass.MEASUREMENT,
        "icon": "mdi:heart-pulse",
    },
    {
        "unique_id": "miband9_sleep",
        "name": "Sen",
        "source": "sensor.miband_sleep",
        "unit": "min",
        "device_class": None,
        "state_class": SensorStateClass.MEASUREMENT,
        "icon": "mdi:sleep",
    },
    {
        "unique_id": "miband9_spo2",
        "name": "SpO2",
        "source": "sensor.miband_spo2",
        "unit": "%",
        "device_class": None,
        "state_class": SensorStateClass.MEASUREMENT,
        "icon": "mdi:blood-bag",
    },
    {
        "unique_id": "miband9_stress",
        "name": "Stres",
        "source": "sensor.miband_stress",
        "unit": None,
        "device_class": None,
        "state_class": SensorStateClass.MEASUREMENT,
        "icon": "mdi:emoticon-frown-outline",
    },
    {
        "unique_id": "miband9_activity_score",
        "name": "Aktywność",
        "source": "sensor.miband_as",
        "unit": None,
        "device_class": None,
        "state_class": SensorStateClass.MEASUREMENT,
        "icon": "mdi:lightning-bolt",
    },
    {
        "unique_id": "miband9_trigger_connected",
        "name": "Ostatnie połączenie",
        "source": "sensor.miband_trigger_6",
        "unit": None,
        "device_class": SensorDeviceClass.TIMESTAMP,
        "state_class": None,
        "icon": "mdi:bluetooth-connect",
        "is_timestamp": True,
    },
    {
        "unique_id": "miband9_trigger_disconnected",
        "name": "Ostatnie rozłączenie",
        "source": "sensor.miband_trigger_7",
        "unit": None,
        "device_class": SensorDeviceClass.TIMESTAMP,
        "state_class": None,
        "icon": "mdi:bluetooth-off",
        "is_timestamp": True,
    },
]


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    async_add_entities(
        [MiBand9Sensor(hass, cfg) for cfg in SENSORS],
        update_before_add=True,
    )


class MiBand9Sensor(SensorEntity):
    """Sensor mirroring a source entity, grouped under Mi Band 9 device."""

    _attr_has_entity_name = True
    _attr_should_poll = False

    def __init__(self, hass: HomeAssistant, cfg: dict) -> None:
        self.hass = hass
        self._source = cfg["source"]
        self._is_timestamp = cfg.get("is_timestamp", False)
        self._attr_unique_id = cfg["unique_id"]
        self._attr_name = cfg["name"]
        self._attr_native_unit_of_measurement = cfg["unit"]
        self._attr_device_class = cfg["device_class"]
        self._attr_state_class = cfg["state_class"]
        self._attr_icon = cfg["icon"]
        self._attr_device_info = DEVICE_INFO

    async def async_added_to_hass(self) -> None:
        self.async_on_remove(
            async_track_state_change_event(
                self.hass, [self._source], self._handle_state_change
            )
        )
        self._update_state()

    @callback
    def _handle_state_change(self, event) -> None:
        self._update_state()
        self.async_write_ha_state()

    def _update_state(self) -> None:
        state = self.hass.states.get(self._source)
        if state is None or state.state in ("unknown", "unavailable"):
            self._attr_native_value = None
            return

        if self._is_timestamp:
            try:
                ts = int(state.state)
                if ts > 0:
                    self._attr_native_value = as_local(
                        datetime.utcfromtimestamp(ts).replace(
                            tzinfo=__import__("datetime").timezone.utc
                        )
                    )
                else:
                    self._attr_native_value = None
            except (ValueError, TypeError):
                self._attr_native_value = None
        else:
            try:
                self._attr_native_value = float(state.state)
            except (ValueError, TypeError):
                self._attr_native_value = state.state

    @property
    def available(self) -> bool:
        state = self.hass.states.get(self._source)
        return state is not None and state.state not in ("unknown", "unavailable")
