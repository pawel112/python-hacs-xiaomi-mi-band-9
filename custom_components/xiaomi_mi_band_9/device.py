"""Device info for Xiaomi Mi Band 9."""
from homeassistant.helpers.entity import DeviceInfo
from . import DOMAIN

DEVICE_INFO = DeviceInfo(
    identifiers={(DOMAIN, "xiaomi_mi_band_9")},
    name="Xiaomi Mi Band 9",
    manufacturer="Xiaomi",
    model="Smart Band 9",
)
