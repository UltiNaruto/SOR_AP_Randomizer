from ...Items import StreetsOfRageItem
from ...Locations import StreetsOfRageLocation
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

        self.locations = [
            StreetsOfRageLocation(
                name='Rach Shop Phone Booth 1 (Apple)',
                stage=self.stage,
                can_access=lambda state, player: True,
                parent=self,
            ),
            StreetsOfRageLocation(
                name='Rach Shop Phone Booth 2 (Bottle)',
                stage=self.stage,
                can_access=lambda state, player: True,
                parent=self,
            ),
            StreetsOfRageLocation(
                name='Rach Shop Phone Booth 3 (Pipe)',
                stage=self.stage,
                can_access=lambda state, player: True,
                parent=self,
            ),
            StreetsOfRageLocation(
                name='ABC Shop Phone Booth 1 (Nothing)',
                stage=self.stage,
                can_access=lambda state, player: True,
                parent=self,
            ),
            StreetsOfRageLocation(
                name='ABC Shop Phone Booth 2 (Bottle)',
                stage=self.stage,
                can_access=lambda state, player: True,
                parent=self,
            ),
            StreetsOfRageLocation(
                name='ABC Shop Phone Booth 3 (Nothing)',
                stage=self.stage,
                can_access=lambda state, player: True,
                parent=self,
            ),
            StreetsOfRageLocation(
                name='Boss Phone Booth (Chicken)',
                stage=self.stage,
                can_access=lambda state, player: True,
                parent=self,
            ),
        ]


# noinspection PyShadowingNames
class ShoppingMall_StageClear(StreetsOfRageRegion):
    name = 'Shopping Mall (Stage Clear)'

    def __init__(self, player: int, multiworld: MultiWorld):
        super().__init__(player, multiworld, stage=0, exits_={
            'Menu': lambda state, player: True,
        })

        self.locations = [
            StreetsOfRageLocation(
                name='Stage Clear (Inner City Slums Key)',
                stage=self.stage,
                can_access=lambda state, player: True,
                parent=self,
            ),
            StreetsOfRageLocation(
                name='Shopping Mall Boss Beaten',
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
