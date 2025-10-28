from typing import Callable, Optional

from BaseClasses import CollectionState, Location, Region
from .Items import StreetsOfRageItem
from .Utils import strip_description_from_region_name


class StreetsOfRageLocation(Location):
    game: str = "Streets of Rage"
    stage: Optional[int] = None

    def __init__(self,
                 name: str,
                 stage: Optional[int],
                 can_access: Callable[[CollectionState, int], bool],
                 parent: Region,
                 locked_item: Optional[StreetsOfRageItem]=None,
        ):
        loc_name = f"{strip_description_from_region_name(parent.name)} - {name}"
        if loc_name not in parent.multiworld.worlds[parent.player].location_name_to_id:
            idx = None
        else:
            idx = parent.multiworld.worlds[parent.player].location_name_to_id[loc_name]
        super().__init__(parent.player, loc_name, idx, parent)
        self.stage = stage
        self.can_access = lambda state: can_access(state, self.player)
        if locked_item is not None:
            locked_item.location = self
            self.place_locked_item(locked_item)
