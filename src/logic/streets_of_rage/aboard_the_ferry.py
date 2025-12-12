from ...Items import StreetsOfRageItem
from ...Regions import StreetsOfRageRegion

from BaseClasses import MultiWorld, ItemClassification


# noinspection PyShadowingNames
class AboardTheFerry(StreetsOfRageRegion):
    name = 'Aboard The Ferry'

    def __init__(self, player: int, multiworld: MultiWorld):
        super().__init__(player, multiworld, stage=4, exits_={
            'Menu': lambda state, player: True,
            'Aboard The Ferry (Stage Clear)': lambda state, player: True,
        })

        self.add_location(
            'Double Wooden Wall Container 1 (1000 Points)',
            lambda state, player: True,
        )
        self.add_location(
            'Double Wooden Wall Container 2 (Sleeping Powder)',
            lambda state, player: True,
        )
        self.add_location(
            'Double Wooden Wall Container 3 (1000 Points)',
            lambda state, player: True,
        )
        self.add_location(
            'Double Wooden Wall Container 4 (Apple)',
            lambda state, player: True,
        )
        self.add_location(
            'First Ladder Container (Chicken)',
            lambda state, player: True,
        )
        self.add_location(
            'Before Second Ladder Container (Chicken)',
            lambda state, player: True,
        )
        self.add_location(
            'Before Boss Container (Police)',
            lambda state, player: True,
        )
        self.add_location(
            'Boss Container (Chicken)',
            lambda state, player: True,
        )


# noinspection PyShadowingNames
class AboardTheFerry_StageClear(StreetsOfRageRegion):
    name = 'Aboard The Ferry (Stage Clear)'

    def __init__(self, player: int, multiworld: MultiWorld):
        super().__init__(player, multiworld, stage=4, exits_={
            'Menu': lambda state, player: True,
        })

        self.add_location(
            'Stage Clear (Factory Key)',
            lambda state, player: True,
        )
        self.add_location(
            'Aboard The Ferry Boss Beaten',
            lambda state, player: True,
            locked_item=StreetsOfRageItem(
                name='Stage Clear',
                classification=ItemClassification.progression,
                code=None,
                player=player,
            ),
        )
