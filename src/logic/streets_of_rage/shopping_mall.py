from ...Items import StreetsOfRageItem
from ...Regions import StreetsOfRageRegion

from BaseClasses import MultiWorld, ItemClassification


# noinspection PyShadowingNames
class ShoppingMall(StreetsOfRageRegion):
    name = 'Shopping Mall'

    def __init__(self, player: int, multiworld: MultiWorld):
        super().__init__(player, multiworld, stage=0, exits_={
            'Menu': lambda state, player: True,
            'Shopping Mall (Stage Clear)': lambda state, player: True,
        })

        self.add_location(
            'Rach Shop Phone Booth 1 (Apple)',
            lambda state, player: True,
        )
        self.add_location(
            'Rach Shop Phone Booth 2 (Bottle)',
            lambda state, player: True,
        )
        self.add_location(
            'Rach Shop Phone Booth 3 (Pipe)',
            lambda state, player: True,
        )
        self.add_location(
            'ABC Shop Phone Booth 1 (Nothing)',
            lambda state, player: True,
        )
        self.add_location(
            'ABC Shop Phone Booth 2 (Bottle)',
            lambda state, player: True,
        )
        self.add_location(
            'ABC Shop Phone Booth 3 (Nothing)',
            lambda state, player: True,
        )
        self.add_location(
            'Boss Phone Booth (Chicken)',
            lambda state, player: True,
        )


# noinspection PyShadowingNames
class ShoppingMall_StageClear(StreetsOfRageRegion):
    name = 'Shopping Mall (Stage Clear)'

    def __init__(self, player: int, multiworld: MultiWorld):
        super().__init__(player, multiworld, stage=0, exits_={
            'Menu': lambda state, player: True,
        })

        self.add_location(
            'Stage Clear (Inner City Slums Key)',
            lambda state, player: True,
        )
        self.add_location(
            'Shopping Mall Boss Beaten',
            lambda state, player: True,
            locked_item=StreetsOfRageItem(
                name='Stage Clear',
                classification=ItemClassification.progression,
                code=None,
                player=player,
            ),
        )
