from typing import Callable, Optional

from BaseClasses import CollectionState, Region, MultiWorld


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
