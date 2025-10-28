from ...Items import StreetsOfRageItem
from ...Locations import StreetsOfRageLocation
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

        self.locations = [
            StreetsOfRageLocation(
                name='First Treadmill Crate 1 (5000 Points)',
                stage=self.stage,
                can_access=lambda state, player: True,
                parent=self,
            ),
            StreetsOfRageLocation(
                name='First Treadmill Crate 2 (1000 Points)',
                stage=self.stage,
                can_access=lambda state, player: True,
                parent=self,
            ),
            StreetsOfRageLocation(
                name='Miniboss Crate 1 (Apple)',
                stage=self.stage,
                can_access=lambda state, player: True,
                parent=self,
            ),
            StreetsOfRageLocation(
                name='Miniboss Crate 2 (Chicken)',
                stage=self.stage,
                can_access=lambda state, player: True,
                parent=self,
            ),
            StreetsOfRageLocation(
                name='After Double Treadmill Crate 1 (Sleeping Powder)',
                stage=self.stage,
                can_access=lambda state, player: True,
                parent=self,
            ),
            StreetsOfRageLocation(
                name='After Double Treadmill Crate 2 (Nothing)',
                stage=self.stage,
                can_access=lambda state, player: True,
                parent=self,
            ),
            StreetsOfRageLocation(
                name='Before Big Single Treadmill Crate 1 (Police)',
                stage=self.stage,
                can_access=lambda state, player: True,
                parent=self,
            ),
            StreetsOfRageLocation(
                name='Before Big Single Treadmill Crate 2 (Extra Life)',
                stage=self.stage,
                can_access=lambda state, player: True,
                parent=self,
            ),
            StreetsOfRageLocation(
                name='Before Big Single Treadmill Crate 3 (Pipe)',
                stage=self.stage,
                can_access=lambda state, player: True,
                parent=self,
            ),
            StreetsOfRageLocation(
                name='Boss Crate (Chicken)',
                stage=self.stage,
                can_access=lambda state, player: True,
                parent=self,
            ),
        ]


# noinspection PyShadowingNames
class Factory_StageClear(StreetsOfRageRegion):
    name = 'Factory (Stage Clear)'

    def __init__(self, player: int, multiworld: MultiWorld):
        super().__init__(player, multiworld, stage=5, exits_={
            'Menu': lambda state, player: True,
        })

        self.locations = [
            StreetsOfRageLocation(
                name='Stage Clear (Elevator Key)',
                stage=self.stage,
                can_access=lambda state, player: True,
                parent=self,
            ),
            StreetsOfRageLocation(
                name='Factory Boss Beaten',
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
