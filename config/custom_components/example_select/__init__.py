"""The example sensor integration."""

from __future__ import annotations

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.aiohttp_client import (
    async_get_clientsession,
)
from homeassistant.const import Platform

async def async_setup(
    hass: HomeAssistant,
    config: dict,
) -> bool:
    """Set up integration from YAML."""
    return True


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
) -> bool:

    hass.data.setdefault("example_select", {})

    await hass.config_entries.async_forward_entry_setups(
        entry,
        [Platform.SELECT],
    )

    return True

async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    # This is called when an entry/configured device is to be removed. The class
    # needs to unload itself, and remove callbacks. See the classes for further
    # details
    unload_ok = await hass.config_entries.async_unload_platforms(entry, [Platform.SELECT])

    return unload_ok