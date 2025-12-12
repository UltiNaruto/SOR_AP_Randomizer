from ...Items import StreetsOfRageItem
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

        self.add_location(
            'First Hole Signalisation Block (Sleeping Powder)',
            lambda state, player: True,
        )
        self.add_location(
            'First Hole Safety Barrier (1000 Points)',
            lambda state, player: True,
        )
        self.add_location(
            'Second Hole Signalisation Pole (Apple)',
            lambda state, player: True,
        )
        self.add_location(
            'Second Hole Signalisation Block (Extra Life)',
            lambda state, player: True,
        )
        self.add_location(
            'Third Hole Signalisation Pole (Nothing)',
            lambda state, player: True,
        )
        self.add_location(
            'Third Hole Safety Barrier 1 (1000 Points)',
            lambda state, player: True,
        )
        self.add_location(
            'Third Hole Safety Barrier 2 (Apple)',
            lambda state, player: True,
        )
        self.add_location(
            'Big Hole Signalisation Block 1 (Bottle)',
            lambda state, player: True,
        )
        self.add_location(
            'Big Hole Signalisation Block 2 (Chicken)',
            lambda state, player: True,
        )


# noinspection PyShadowingNames
class BridgeUnderConstruction_StageClear(StreetsOfRageRegion):
    name = 'Bridge Under Construction (Stage Clear)'

    def __init__(self, player: int, multiworld: MultiWorld):
        super().__init__(player, multiworld, stage=3, exits_={
            'Menu': lambda state, player: True,
        })

        self.add_location(
            'Stage Clear (Aboard The Ferry Key)',
            lambda state, player: True,
        )
        self.add_location(
            'Bridge Under Construction Boss Beaten',
            lambda state, player: True,
            StreetsOfRageItem(
                name='Stage Clear',
                classification=ItemClassification.progression,
                code=None,
                player=player,
            ),
        )
