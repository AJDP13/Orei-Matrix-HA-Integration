"""Platform for sensor integration."""
from __future__ import annotations

from homeassistant.components.select import (
    SelectDeviceClass,
    SelectEntity
)
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.typing import ConfigType, DiscoveryInfoType


def setup_platform(
    hass: HomeAssistant,
    config: ConfigType,
    add_entities: AddEntitiesCallback,
    discovery_info: DiscoveryInfoType | None = None
) -> None:
    add_entities(
        [
            ExampleSelect()
        ]
    )
    
class ExampleSelect(SelectEntity):
    __atr_name = "Output 1"

    _selected = "Sky"


    @property
    def options(self) -> list[str]:
        return ["AppleTV", "Sky", "Input3", "Input4"]
    
    @property
    def current_option(self) -> str:
        return self._selected
    
    def select_option(self, option:str) -> None:
        if(option not in self.options()):
            return
        self._selected = option