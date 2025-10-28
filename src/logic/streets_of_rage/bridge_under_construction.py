from ...Items import StreetsOfRageItem
from ...Locations import StreetsOfRageLocation
from ...Regions import StreetsOfRageRegion

from BaseClasses import MultiWorld, ItemClassification


# noinspection PyShadowingNames
class BridgeUnderConstruction(StreetsOfRageRegion):
    name = 'Bridge Under Construction'

    def __init__(self, player: int, multiworld: MultiWorld):
        super().__init__(player, multiworld, stage=3, exits_={
            'Menu': lambda state, player: True,
            'Bridge Under Construction (Stage Clear)': lambda state, player: True,
        })

        self.locations = [
            StreetsOfRageLocation(
                name='First Hole Signalisation Block (Sleeping Powder)',
                stage=self.stage,
                can_access=lambda state, player: True,
                parent=self,
            ),
            StreetsOfRageLocation(
                name='First Hole Safety Barrier (1000 Points)',
                stage=self.stage,
                can_access=lambda state, player: True,
                parent=self,
            ),
            StreetsOfRageLocation(
                name='Second Hole Signalisation Pole (Apple)',
                stage=self.stage,
                can_access=lambda state, player: True,
                parent=self,
            ),
            StreetsOfRageLocation(
                name='Second Hole Signalisation Block (Extra Life)',
                stage=self.stage,
                can_access=lambda state, player: True,
                parent=self,
            ),
            StreetsOfRageLocation(
                name='Third Hole Signalisation Pole (Nothing)',
                stage=self.stage,
                can_access=lambda state, player: True,
                parent=self,
            ),
            StreetsOfRageLocation(
                name='Third Hole Safety Barrier 1 (1000 Points)',
                stage=self.stage,
                can_access=lambda state, player: True,
                parent=self,
            ),
            StreetsOfRageLocation(
                name='Third Hole Safety Barrier 2 (Apple)',
                stage=self.stage,
                can_access=lambda state, player: True,
                parent=self,
            ),
            StreetsOfRageLocation(
                name='Big Hole Signalisation Block 1 (Bottle)',
                stage=self.stage,
                can_access=lambda state, player: True,
                parent=self,
            ),
            StreetsOfRageLocation(
                name='Big Hole Signalisation Block 2 (Chicken)',
                stage=self.stage,
                can_access=lambda state, player: True,
                parent=self,
            ),
        ]


# noinspection PyShadowingNames
class BridgeUnderConstruction_StageClear(StreetsOfRageRegion):
    name = 'Bridge Under Construction (Stage Clear)'

    def __init__(self, player: int, multiworld: MultiWorld):
        super().__init__(player, multiworld, stage=3, exits_={
            'Menu': lambda state, player: True,
        })

        self.locations = [
            StreetsOfRageLocation(
                name='Stage Clear (Aboard The Ferry Key)',
                stage=self.stage,
                can_access=lambda state, player: True,
                parent=self,
            ),
            StreetsOfRageLocation(
                name='Bridge Under Construction Boss Beaten',
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
