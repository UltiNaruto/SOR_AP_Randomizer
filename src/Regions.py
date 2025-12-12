from .Locations import StreetsOfRageLocation

from typing import Callable, Optional, TYPE_CHECKING

from BaseClasses import CollectionState, Region, MultiWorld


if TYPE_CHECKING:
    from .Items import StreetsOfRageItem


class StreetsOfRageRegion(Region):
    desc: Optional[str]
    stage: Optional[int]
    exits_: dict[str, Callable[[CollectionState, int], bool]]

    def __init__(self, player: int, multiworld: MultiWorld, desc: Optional[str]=None, stage: Optional[int]=None, exits_: dict[str, Callable[[CollectionState, int], bool]]=None):
        self.desc = desc
        self.stage = stage
        self.exits_ = {} if exits_ is None else exits_
        if desc is not None:
            super().__init__(f"{self.name} ({self.desc})", player, multiworld)
        else:
            super().__init__(f"{self.name}", player, multiworld)

    def add_location(self, name: str, can_access: Callable[[CollectionState, int], bool], locked_item: Optional["StreetsOfRageItem"]=None) -> None:
        self.locations += [StreetsOfRageLocation(
            name,
            self.stage,
            can_access,
            self,
            locked_item,
        )]
