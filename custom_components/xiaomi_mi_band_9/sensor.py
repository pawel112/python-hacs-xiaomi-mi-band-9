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
from datetime import datetime, timezone

from .device import DEVICE_INFO
from . import DOMAIN


SENSORS = [
    {
        "unique_id": "miband9_heartrate",
        "name": "Tętno",
        "source": "sensor.miband_heartrate",
        "unit": "bpm",
        "device_class": None,
        "state_class": SensorStateClass.MEASUREMENT,
        "icon": "mdi:heart-pulse",
        "attr_key": None,
    },
    {
        "unique_id": "miband9_steps",
        "name": "Kroki",
        "source": "sensor.miband_steps",
        "unit": "steps",
        "device_class": None,
        "state_class": SensorStateClass.TOTAL_INCREASING,
        "icon": "mdi:walk",
        "attr_key": None,
    },
    {
        "unique_id": "miband9_calories",
        "name": "Kalorie",
        "source": "sensor.miband_calories",
        "unit": "cal",
        "device_class": None,
        "state_class": SensorStateClass.TOTAL_INCREASING,
        "icon": "mdi:food",
        "attr_key": None,
    },
    {
        "unique_id": "miband9_distance",
        "name": "Dystans",
        "source": "sensor.miband_distance",
        "unit": "m",
        "device_class": None,
        "state_class": SensorStateClass.TOTAL_INCREASING,
        "icon": "mdi:map-marker-distance",
        "attr_key": None,
    },
    {
        "unique_id": "miband9_sleep",
        "name": "Sen",
        "source": "sensor.miband_sleep",
        "unit": None,
        "device_class": None,
        "state_class": None,
        "icon": "mdi:sleep",
        "attr_key": None,
    },
    {
        "unique_id": "miband9_sleep_duration",
        "name": "Czas snu",
        "source": "sensor.miband_sleepduration",
        "unit": "min",
        "device_class": None,
        "state_class": SensorStateClass.MEASUREMENT,
        "icon": "mdi:clock-outline",
        "attr_key": None,
    },
    {
        "unique_id": "miband9_connected_ts",
        "name": "Ostatnie połączenie",
        "source": "sensor.miband_trigger_6",
        "unit": None,
        "device_class": SensorDeviceClass.TIMESTAMP,
        "state_class": None,
        "icon": "mdi:bluetooth-connect",
        "attr_key": None,
        "is_timestamp": True,
    },
    {
        "unique_id": "miband9_connected_raw",
        "name": "Status połączenia",
        "source": "sensor.miband_connected",
        "unit": None,
        "device_class": SensorDeviceClass.TIMESTAMP,
        "state_class": None,
        "icon": "mdi:timeline-clock",
        "attr_key": None,
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
    """Sensor mirroring a source entity under Mi Band 9 device."""

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
        if state is None or state.state in ("unknown", "unavailable", ""):
            self._attr_native_value = None
            return

        if self._is_timestamp:
            # Obsługa zarówno ISO string jak i unix timestamp
            raw = state.state
            try:
                # Próbuj jako ISO datetime (np. "2026-05-24T15:38:01+0200")
                self._attr_native_value = datetime.fromisoformat(raw)
            except ValueError:
                try:
                    # Próbuj jako unix timestamp (ms lub s)
                    ts = int(raw)
                    if ts > 1_000_000_000_000:
                        ts = ts // 1000
                    if ts > 0:
                        self._attr_native_value = datetime.fromtimestamp(ts, tz=timezone.utc)
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
    def extra_state_attributes(self):
        """Przekaż atrybuty z encji źródłowej."""
        state = self.hass.states.get(self._source)
        if state:
            return dict(state.attributes)
        return {}

    @property
    def available(self) -> bool:
        state = self.hass.states.get(self._source)
        return state is not None and state.state not in ("unknown", "unavailable")
