from . import has_final_boss_access
from ...Items import StreetsOfRageItem
from ...Locations import StreetsOfRageLocation
from ...Regions import StreetsOfRageRegion

from BaseClasses import MultiWorld, ItemClassification


# noinspection PyShadowingNames
class SyndicateMansion(StreetsOfRageRegion):
    name = 'Syndicate Mansion'

    def __init__(self, player: int, multiworld: MultiWorld):
        super().__init__(player, multiworld, stage=7, exits_={
            'Menu': lambda state, player: True,
            'Syndicate Mansion (Twins)': lambda state, player: True,
        })

        self.locations = [
            StreetsOfRageLocation(
                name='Before Stage 1 Boss Table 1 (Nothing)',
                stage=self.stage,
                can_access=lambda state, player: True,
                parent=self,
            ),
            StreetsOfRageLocation(
                name='Before Stage 1 Boss Table 2 (Nothing)',
                stage=self.stage,
                can_access=lambda state, player: True,
                parent=self,
            ),
            StreetsOfRageLocation(
                name='Stage 1 Boss Table (Apple)',
                stage=self.stage,
                can_access=lambda state, player: True,
                parent=self,
            ),
            StreetsOfRageLocation(
                name='Stage 2 Boss Table (Chicken)',
                stage=self.stage,
                can_access=lambda state, player: True,
                parent=self,
            ),
            StreetsOfRageLocation(
                name='Stage 3 Boss Table 1 (Sleeping Powder)',
                stage=self.stage,
                can_access=lambda state, player: True,
                parent=self,
            ),
            StreetsOfRageLocation(
                name='Stage 3 Boss Table 2 (Chicken)',
                stage=self.stage,
                can_access=lambda state, player: True,
                parent=self,
            ),
            StreetsOfRageLocation(
                name='Before Stage 4 Boss Table (Chicken)',
                stage=self.stage,
                can_access=lambda state, player: True,
                parent=self,
            ),
            StreetsOfRageLocation(
                name='Stage 4 Boss Table 1 (Knife)',
                stage=self.stage,
                can_access=lambda state, player: True,
                parent=self,
            ),
            StreetsOfRageLocation(
                name='Stage 4 Boss Table 2 (Sleeping Powder)',
                stage=self.stage,
                can_access=lambda state, player: True,
                parent=self,
            ),
            StreetsOfRageLocation(
                name='Stage 4 Boss Table 3 (Apple)',
                stage=self.stage,
                can_access=lambda state, player: True,
                parent=self,
            ),
            StreetsOfRageLocation(
                name='Before Stage 5 Boss Table (Nothing)',
                stage=self.stage,
                can_access=lambda state, player: True,
                parent=self,
            ),
            StreetsOfRageLocation(
                name='Stage 5 Boss Table (Chicken)',
                stage=self.stage,
                can_access=lambda state, player: True,
                parent=self,
            ),
        ]


# noinspection PyShadowingNames
class SyndicateMansion_Twins(StreetsOfRageRegion):
    name = 'Syndicate Mansion (Twins)'

    def __init__(self, player: int, multiworld: MultiWorld):
        super().__init__(player, multiworld, stage=7, exits_= {
            'Syndicate Mansion (Mr. X)': lambda state, player: has_final_boss_access(state, player),
        })

        self.locations = [
            StreetsOfRageLocation(
                name='Twins (Nothing)',
                stage=self.stage,
                can_access=lambda state, player: True,
                parent=self,
            ),
            StreetsOfRageLocation(
                name='Syndicate Mansion Twins Beaten',
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


# noinspection PyShadowingNames
class SyndicateMansion_MrX(StreetsOfRageRegion):
    name = 'Syndicate Mansion (Mr. X)'

    def __init__(self, player: int, multiworld: MultiWorld):
        super().__init__(player, multiworld, stage=8, exits_={
            'Menu': lambda state, player: True,
        })

        self.locations = [
            StreetsOfRageLocation(
                name='Mr. X Defeated',
                stage=self.stage,
                can_access=lambda state, player: True,
                parent=self,
                locked_item=StreetsOfRageItem(
                    name='Mr. X Defeated',
                    classification=ItemClassification.progression,
                    code=None,
                    player=player,
                ),
            ),
        ]
