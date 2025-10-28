from ...Items import StreetsOfRageItem
from ...Locations import StreetsOfRageLocation
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

        self.locations = [
            StreetsOfRageLocation(
                name='Double Wooden Wall Container 1 (1000 Points)',
                stage=self.stage,
                can_access=lambda state, player: True,
                parent=self,
            ),
            StreetsOfRageLocation(
                name='Double Wooden Wall Container 2 (Sleeping Powder)',
                stage=self.stage,
                can_access=lambda state, player: True,
                parent=self,
            ),
            StreetsOfRageLocation(
                name='Double Wooden Wall Container 3 (1000 Points)',
                stage=self.stage,
                can_access=lambda state, player: True,
                parent=self,
            ),
            StreetsOfRageLocation(
                name='Double Wooden Wall Container 4 (Apple)',
                stage=self.stage,
                can_access=lambda state, player: True,
                parent=self,
            ),
            StreetsOfRageLocation(
                name='First Ladder Container (Chicken)',
                stage=self.stage,
                can_access=lambda state, player: True,
                parent=self,
            ),
            StreetsOfRageLocation(
                name='Before Second Ladder Container (Chicken)',
                stage=self.stage,
                can_access=lambda state, player: True,
                parent=self,
            ),
            StreetsOfRageLocation(
                name='Before Boss Container (Police)',
                stage=self.stage,
                can_access=lambda state, player: True,
                parent=self,
            ),
            StreetsOfRageLocation(
                name='Boss Container (Chicken)',
                stage=self.stage,
                can_access=lambda state, player: True,
                parent=self,
            ),
        ]


# noinspection PyShadowingNames
class AboardTheFerry_StageClear(StreetsOfRageRegion):
    name = 'Aboard The Ferry (Stage Clear)'

    def __init__(self, player: int, multiworld: MultiWorld):
        super().__init__(player, multiworld, stage=4, exits_={
            'Menu': lambda state, player: True,
        })

        self.locations = [
            StreetsOfRageLocation(
                name='Stage Clear (Factory Key)',
                stage=self.stage,
                can_access=lambda state, player: True,
                parent=self,
            ),
            StreetsOfRageLocation(
                name='Aboard The Ferry Boss Beaten',
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
