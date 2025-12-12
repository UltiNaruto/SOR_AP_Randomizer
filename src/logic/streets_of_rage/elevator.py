from ...Items import StreetsOfRageItem
from ...Regions import StreetsOfRageRegion

from BaseClasses import MultiWorld, ItemClassification


# noinspection PyShadowingNames
class Elevator(StreetsOfRageRegion):
    name = 'Elevator'

    def __init__(self, player: int, multiworld: MultiWorld):
        super().__init__(player, multiworld, stage=6, exits_={
            'Menu': lambda state, player: True,
            'Elevator (Stage Clear)': lambda state, player: True,
        })


# noinspection PyShadowingNames
class Elevator_StageClear(StreetsOfRageRegion):
    name = 'Elevator (Stage Clear)'

    def __init__(self, player: int, multiworld: MultiWorld):
        super().__init__(player, multiworld, stage=6, exits_={
            'Menu': lambda state, player: True,
        })

        self.add_location(
            'Stage Clear (Syndicate Mansion Key)',
            lambda state, player: True,
        )
        self.add_location(
            'Elevator Stage Clear',
            lambda state, player: True,
            StreetsOfRageItem(
                name='Stage Clear',
                classification=ItemClassification.progression,
                code=None,
                player=player,
            ),
        )
