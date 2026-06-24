"""Orei HDMI Matrix integration."""

# __init__.py

from __future__ import annotations

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.aiohttp_client import (
    async_get_clientsession,
)

from .api import OreiApi
from .const import DOMAIN, PLATFORMS
from .coordinator import OreiCoordinator
from .orei_client import OreiHttpClient


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
    """Set up Orei Matrix from a config entry."""

    hass.data.setdefault(DOMAIN, {})

    host = entry.data["Matrix Host"]

    session = async_get_clientsession(hass)

    client = OreiHttpClient(
        host=host,
        session=session,
    )

    api = OreiApi(client)

    coordinator = OreiCoordinator(
        hass=hass,
        api=api,
    )

    await coordinator.async_config_entry_first_refresh()

    hass.data[DOMAIN][entry.entry_id] = {
        "client": client,
        "api": api,
        "coordinator": coordinator,
    }

    await hass.config_entries.async_forward_entry_setups(
        entry,
        PLATFORMS,
    )

    return True


async def async_unload_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
) -> bool:
    """Unload an Orei config entry."""

    unload_ok = await hass.config_entries.async_unload_platforms(
        entry,
        PLATFORMS,
    )

    if unload_ok:
        hass.data[DOMAIN].pop(
            entry.entry_id,
            None,
        )

    return unload_ok