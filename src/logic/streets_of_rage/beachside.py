from ...Items import StreetsOfRageItem
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

        self.add_location(
            'Before First Projector Tires (Baseball Bat)',
            lambda state, player: True,
        )
        self.add_location(
            'Third Fence Tires 1 (Apple)',
            lambda state, player: True,
        )
        self.add_location(
            'Third Fence Tires 2 (1000 Points)',
            lambda state, player: True,
        )
        self.add_location(
            'Third Fence Tires 3 (Chicken)',
            lambda state, player: True,
        )


# noinspection PyShadowingNames
class Beachside_StageClear(StreetsOfRageRegion):
    name = 'Beachside (Stage Clear)'

    def __init__(self, player: int, multiworld: MultiWorld):
        super().__init__(player, multiworld, stage=2, exits_={
            'Menu': lambda state, player: True,
        })

        self.add_location(
            'Stage Clear (Bridge Under Construction Key)',
            lambda state, player: True,
        )
        self.add_location(
            'Beachside Boss Beaten',
            lambda state, player: True,
            StreetsOfRageItem(
                name='Stage Clear',
                classification=ItemClassification.progression,
                code=None,
                player=player,
            ),
        )
