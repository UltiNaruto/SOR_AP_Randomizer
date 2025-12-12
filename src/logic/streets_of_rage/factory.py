from ...Items import StreetsOfRageItem
from ...Regions import StreetsOfRageRegion

from BaseClasses import MultiWorld, ItemClassification


# noinspection PyShadowingNames
class Factory(StreetsOfRageRegion):
    name = 'Factory'

    def __init__(self, player: int, multiworld: MultiWorld):
        super().__init__(player, multiworld, stage=5, exits_={
            'Menu': lambda state, player: True,
            'Factory (Stage Clear)': lambda state, player: True,
        })

        self.add_location(
            'First Treadmill Crate 1 (5000 Points)',
            lambda state, player: True,
        )
        self.add_location(
            'First Treadmill Crate 2 (1000 Points)',
            lambda state, player: True,
        )
        self.add_location(
            'Miniboss Crate 1 (Apple)',
            lambda state, player: True,
        )
        self.add_location(
            'Miniboss Crate 2 (Chicken)',
            lambda state, player: True,
        )
        self.add_location(
            'After Double Treadmill Crate 1 (Sleeping Powder)',
            lambda state, player: True,
        )
        self.add_location(
            'After Double Treadmill Crate 2 (Nothing)',
            lambda state, player: True,
        )
        self.add_location(
            'Before Big Single Treadmill Crate 1 (Police)',
            lambda state, player: True,
        )
        self.add_location(
            'Before Big Single Treadmill Crate 2 (Extra Life)',
            lambda state, player: True,
        )
        self.add_location(
            'Before Big Single Treadmill Crate 3 (Pipe)',
            lambda state, player: True,
        )
        self.add_location(
            'Boss Crate (Chicken)',
            lambda state, player: True,
        )


# noinspection PyShadowingNames
class Factory_StageClear(StreetsOfRageRegion):
    name = 'Factory (Stage Clear)'

    def __init__(self, player: int, multiworld: MultiWorld):
        super().__init__(player, multiworld, stage=5, exits_={
            'Menu': lambda state, player: True,
        })

        self.add_location(
            'Stage Clear (Elevator Key)',
            lambda state, player: True,
        )
        self.add_location(
            'Factory Boss Beaten',
            lambda state, player: True,
            StreetsOfRageItem(
                name='Stage Clear',
                classification=ItemClassification.progression,
                code=None,
                player=player,
            ),
        )
