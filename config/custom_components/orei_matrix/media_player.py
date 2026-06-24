from __future__ import annotations

from homeassistant.components.media_player import (
    MediaPlayerEntity,
    MediaPlayerEntityFeature,
    MediaType,
    MediaPlayerState
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

    coordinator: OreiCoordinator =  hass.data[DOMAIN][entry.entry_id][
        "coordinator"
    ]

    entities = [
        OreiOutputMediaPlayer(
            coordinator,
            entry,
            output.id,
        )
        for output in coordinator.data.outputs
    ]

    async_add_entities(entities)


class OreiOutputMediaPlayer(
    CoordinatorEntity,
    MediaPlayerEntity,
):
    """Representation of an Orei output."""

    _attr_should_poll = False

    _attr_supported_features = (
        MediaPlayerEntityFeature.SELECT_SOURCE
    )

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
    def output(self) -> MatrixOutput:
        return next(
            output
            for output in self.coordinator.data.outputs
            if output.id == self._output_id
        )

    @property
    def name(self) -> str:
        return self.output.name

    @property
    def available(self) -> bool:
        return self.coordinator.last_update_success

    @property
    def state(self) -> str:
        return MediaPlayerState.ON

    @property
    def source_list(self) -> list[str]:
        return [
            input_.name
            for input_ in self.coordinator.data.inputs
        ]

    @property
    def source(self) -> str | None:
        current_input_id = self.output.current_input

        return next(
            (
                input_.name
                for input_ in self.coordinator.data.inputs
                if input_.id == current_input_id
            ),
            None,
        )

    async def async_select_source(
        self,
        source: str,
    ) -> None:
        """Select Input Source"""
        
        _LOGGER.debug("Selecting Media Source for Orei")

        selected_input = next(
            (
                input_
                for input_ in self.coordinator.data.inputs
                if input_.name == source
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