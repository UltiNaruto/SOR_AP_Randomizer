from ...Items import StreetsOfRageItem
from ...Regions import StreetsOfRageRegion

from BaseClasses import MultiWorld, ItemClassification


# noinspection PyShadowingNames
class InnerCitySlums(StreetsOfRageRegion):
    name = 'Inner City Slums'

    def __init__(self, player: int, multiworld: MultiWorld):
        super().__init__(player, multiworld, stage=1, exits_={
            'Menu': lambda state, player: True,
            'Inner City Slums (Stage Clear)': lambda state, player: True,
        })

        self.add_location(
            'Red Bricks Door Barrel 1 (1000 Points)',
            lambda state, player: True,
        )
        self.add_location(
            'Red Bricks Door Barrel 2 (Sleeping Powder)',
            lambda state, player: True,
        )
        self.add_location(
            'Broken Windows Door Barrel 1 (Bottle)',
            lambda state, player: True,
        )
        self.add_location(
            'Broken Windows Door Barrel 2 (Apple)',
            lambda state, player: True,
        )
        self.add_location(
            'Graffiti Wall Barrel 1 (Bottle)',
            lambda state, player: True,
        )
        self.add_location(
            'Graffiti Wall Barrel 2 (Extra Life)',
            lambda state, player: True,
        )
        self.add_location(
            'Fence Barrel (Pipe)',
            lambda state, player: True,
        )
        self.add_location(
            'Blue Brick Poster Barrel (Apple)',
            lambda state, player: True,
        )
        self.add_location(
            'Blue Brick Before Boss Barrel (Knife)',
            lambda state, player: True,
        )
        self.add_location(
            'Red Brick Boss Barrel (Chicken)',
            lambda state, player: True,
        )


# noinspection PyShadowingNames
class InnerCitySlums_StageClear(StreetsOfRageRegion):
    name = 'Inner City Slums (Stage Clear)'

    def __init__(self, player: int, multiworld: MultiWorld):
        super().__init__(player, multiworld, stage=1, exits_={
            'Menu': lambda state, player: True,
        })

        self.add_location(
            'Stage Clear (Beachside Key)',
            lambda state, player: True,
        )
        self.add_location(
            'Inner City Slums Boss Beaten',
            lambda state, player: True,
            locked_item=StreetsOfRageItem(
                name='Stage Clear',
                classification=ItemClassification.progression,
                code=None,
                player=player,
            ),
        )
