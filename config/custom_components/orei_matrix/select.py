from homeassistant.components.select import (
    SelectEntity
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN
from .coordinator import OreiCoordinator
from .models import MatrixOutput

import logging

_LOGGER = logging.getLogger(__name__)

async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:

    coordinator: OreiCoordinator = hass.data[DOMAIN][entry.entry_id][
        "coordinator"
    ]

    entities = [
        OreiOutputSelect(
            coordinator,
            entry,
            output.id,
        )
        for output in coordinator.data.outputs
    ]

    async_add_entities(entities)

class OreiOutputSelect(CoordinatorEntity, SelectEntity):
    """Representation of an Orei output."""

    _attr_should_poll = False

    def __init__(
        self,
        coordinator: OreiCoordinator,
        entry: ConfigEntry,
        output_id: int,
    ) -> None:

        super().__init__(coordinator)

        self._output_id = output_id

        self._attr_unique_id = (
            f"{entry.entry_id}_output_{output_id}"
        )

    @property
    def current_option(self) -> str:
        return self.coordinator

    @property
    def options(self) -> list[str]:
        return [
            input_.name
            for input_ in self.coordinator.data.inputs
        ]

    async def async_select_option(
        self,
        option: str,
    ) -> None:
        """Select Input Source"""
        
        _LOGGER.debug("Selecting Media Source for Orei Select")

        selected_input = next(
            (
                input_
                for input_ in self.coordinator.data.inputs
                if input_.name == option
            ),
            None,
        )

        if selected_input is None:
            _LOGGER.debug("Media player has None selected input")
            return

        await self.coordinator.api.set_output_source(
            output_id=self._output_id,
            input_id=selected_input.id,
        )

        await self.coordinator.async_request_refresh()