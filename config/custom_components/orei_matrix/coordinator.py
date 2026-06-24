# coordinator.py

from __future__ import annotations

from datetime import timedelta
from logging import getLogger

from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import (
    DataUpdateCoordinator,
    UpdateFailed,
)

from .api import OreiApi
from .const import DOMAIN, SCAN_INTERVAL
from .models import MatrixState

_LOGGER = getLogger(__name__)


class OreiCoordinator(DataUpdateCoordinator[MatrixState]):
    """Coordinator for Orei matrix state."""

    def __init__(
        self,
        hass: HomeAssistant,
        api: OreiApi,
    ) -> None:
        """Initialize coordinator."""
        self.api = api

        super().__init__(
            hass,
            _LOGGER,
            name=DOMAIN,
            update_interval=timedelta(seconds=SCAN_INTERVAL),
        )

    async def _async_update_data(self) -> MatrixState:
        """Fetch latest data from the matrix."""

        try:
            inputs = await self.api.get_inputs()
            outputs = await self.api.get_outputs()

            return MatrixState(
                inputs=inputs,
                outputs=outputs,
            )

        except Exception as err:
            print("Failed to update Orei Matrix Data")
            raise UpdateFailed(
                f"Failed to update Orei matrix data: {err}"
            ) from err