from ...Items import StreetsOfRageItem
from ...Locations import StreetsOfRageLocation
from ...Regions import StreetsOfRageRegion

from BaseClasses import MultiWorld, ItemClassification


# noinspection PyShadowingNames
class Beachside(StreetsOfRageRegion):
    name = 'Beachside'

    def __init__(self, player: int, multiworld: MultiWorld):
        super().__init__(player, multiworld, stage=2, exits_={
            'Menu': lambda state, player: True,
            'Beachside (Stage Clear)': lambda state, player: True,
        })

        self.locations = [
            StreetsOfRageLocation(
                name='Before First Projector Tires (Baseball Bat)',
                stage=self.stage,
                can_access=lambda state, player: True,
                parent=self,
            ),
            StreetsOfRageLocation(
                name='Third Fence Tires 1 (Apple)',
                stage=self.stage,
                can_access=lambda state, player: True,
                parent=self,
            ),
            StreetsOfRageLocation(
                name='Third Fence Tires 2 (1000 Points)',
                stage=self.stage,
                can_access=lambda state, player: True,
                parent=self,
            ),
            StreetsOfRageLocation(
                name='Third Fence Tires 3 (Chicken)',
                stage=self.stage,
                can_access=lambda state, player: True,
                parent=self,
            ),
        ]


# noinspection PyShadowingNames
class Beachside_StageClear(StreetsOfRageRegion):
    name = 'Beachside (Stage Clear)'

    def __init__(self, player: int, multiworld: MultiWorld):
        super().__init__(player, multiworld, stage=2, exits_={
            'Menu': lambda state, player: True,
        })

        self.locations = [
            StreetsOfRageLocation(
                name='Stage Clear (Bridge Under Construction Key)',
                stage=self.stage,
                can_access=lambda state, player: True,
                parent=self,
            ),
            StreetsOfRageLocation(
                name='Beachside Boss Beaten',
                stage=self.stage,
                can_access=lambda state, player: True,
                parent=self,
                locked_item=StreetsOfRageItem(
                    name='Stage Clear',
                    classification=ItemClassification.progression,
                    code=None,
                    player=player,
                ),
            ),
        ]
