from . import has_final_boss_access
from ...Items import StreetsOfRageItem
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

        self.add_location(
            'Before Stage 1 Boss Table 1 (Nothing)',
            lambda state, player: True,
        )
        self.add_location(
            'Before Stage 1 Boss Table 2 (Nothing)',
            lambda state, player: True,
        )
        self.add_location(
            'Stage 1 Boss Table (Apple)',
            lambda state, player: True,
        )
        self.add_location(
            'Stage 2 Boss Table (Chicken)',
            lambda state, player: True,
        )
        self.add_location(
            'Stage 3 Boss Table 1 (Sleeping Powder)',
            lambda state, player: True,
        )
        self.add_location(
            'Stage 3 Boss Table 2 (Chicken)',
            lambda state, player: True,
        )
        self.add_location(
            'Before Stage 4 Boss Table (Chicken)',
            lambda state, player: True,
        )
        self.add_location(
            'Stage 4 Boss Table 1 (Knife)',
            lambda state, player: True,
        )
        self.add_location(
            'Stage 4 Boss Table 2 (Sleeping Powder)',
            lambda state, player: True,
        )
        self.add_location(
            'Stage 4 Boss Table 3 (Apple)',
            lambda state, player: True,
        )
        self.add_location(
            'Before Stage 5 Boss Table (Nothing)',
            lambda state, player: True,
        )
        self.add_location(
            'Stage 5 Boss Table (Chicken)',
            lambda state, player: True,
        )


# noinspection PyShadowingNames
class SyndicateMansion_Twins(StreetsOfRageRegion):
    name = 'Syndicate Mansion (Twins)'

    def __init__(self, player: int, multiworld: MultiWorld):
        super().__init__(player, multiworld, stage=7, exits_= {
            'Syndicate Mansion (Mr. X)': lambda state, player: has_final_boss_access(state, player),
        })

        self.add_location(
            'Twins (Nothing)',
            lambda state, player: True,
        )
        self.add_location(
            'Syndicate Mansion Twins Beaten',
            lambda state, player: True,
            StreetsOfRageItem(
                name='Stage Clear',
                classification=ItemClassification.progression,
                code=None,
                player=player,
            ),
        )


# noinspection PyShadowingNames
class SyndicateMansion_MrX(StreetsOfRageRegion):
    name = 'Syndicate Mansion (Mr. X)'

    def __init__(self, player: int, multiworld: MultiWorld):
        super().__init__(player, multiworld, stage=8, exits_={
            'Menu': lambda state, player: True,
        })

        self.add_location(
            'Mr. X Defeated',
            lambda state, player: True,
            StreetsOfRageItem(
                name='Mr. X Defeated',
                classification=ItemClassification.progression,
                code=None,
                player=player,
            ),
        )
