from typing import Callable, Type

from .streets_of_rage.aboard_the_ferry import (
    AboardTheFerry,
    AboardTheFerry_StageClear,
)
from .streets_of_rage.beachside import (
    Beachside,
    Beachside_StageClear,
)
from .streets_of_rage.bridge_under_construction import (
    BridgeUnderConstruction,
    BridgeUnderConstruction_StageClear,
)
from .streets_of_rage.elevator import (
    Elevator,
    Elevator_StageClear,
)
from .streets_of_rage.factory import (
    Factory,
    Factory_StageClear,
)
from .streets_of_rage.inner_city_slums import (
    InnerCitySlums,
    InnerCitySlums_StageClear,
)
from .streets_of_rage.menu import (
    AboardTheFerryGate,
    BeachsideGate,
    BridgeUnderConstructionGate,
    ElevatorGate,
    FactoryGate,
    InnerCitySlumsGate,
    Menu,
    ShoppingMallGate,
    SyndicateMansionGate
)
from .streets_of_rage.shopping_mall import (
    ShoppingMall,
    ShoppingMall_StageClear,
)
from .streets_of_rage.syndicate_mansion import (
    SyndicateMansion,
    SyndicateMansion_Twins,
    SyndicateMansion_MrX,
)
from ..Regions import StreetsOfRageRegion

from BaseClasses import CollectionState, Entrance, MultiWorld
from ...generic.Rules import set_rule


def regions_(player:int, multiworld: MultiWorld) -> dict[str, StreetsOfRageRegion]:
    return {
        # Shopping Mall (Stage 1)
        'Shopping Mall': ShoppingMall(player, multiworld),
        'Shopping Mall (Stage Clear)': ShoppingMall_StageClear(player, multiworld),
        'Shopping Mall Gate': ShoppingMallGate(player, multiworld),

        # Inner City Slums (Stage 2)
        'Inner City Slums': InnerCitySlums(player, multiworld),
        'Inner City Slums (Stage Clear)': InnerCitySlums_StageClear(player, multiworld),
        'Inner City Slums Gate': InnerCitySlumsGate(player, multiworld),

        # Beachside (Stage 3)
        'Beachside': Beachside(player, multiworld),
        'Beachside (Stage Clear)': Beachside_StageClear(player, multiworld),
        'Beachside Gate': BeachsideGate(player, multiworld),

        # Bridge Under Construction (Stage 4)
        'Bridge Under Construction': BridgeUnderConstruction(player, multiworld),
        'Bridge Under Construction (Stage Clear)': BridgeUnderConstruction_StageClear(player, multiworld),
        'Bridge Under Construction Gate': BridgeUnderConstructionGate(player, multiworld),

        # Aboard The Ferry (Stage 5)
        'Aboard The Ferry': AboardTheFerry(player, multiworld),
        'Aboard The Ferry (Stage Clear)': AboardTheFerry_StageClear(player, multiworld),
        'Aboard The Ferry Gate': AboardTheFerryGate(player, multiworld),

        # Factory (Stage 6)
        'Factory': Factory(player, multiworld),
        'Factory (Stage Clear)': Factory_StageClear(player, multiworld),
        'Factory Gate': FactoryGate(player, multiworld),

        # Elevator (Stage 7)
        'Elevator': Elevator(player, multiworld),
        'Elevator (Stage Clear)': Elevator_StageClear(player, multiworld),
        'Elevator Gate': ElevatorGate(player, multiworld),

        # Syndicate Mansion (Stage 8)
        'Syndicate Mansion': SyndicateMansion(player, multiworld),
        'Syndicate Mansion (Twins)': SyndicateMansion_Twins(player, multiworld),
        'Syndicate Mansion Gate': SyndicateMansionGate(player, multiworld),

        # Mr. X (Stage 9 - Final Boss)
        'Syndicate Mansion (Mr. X)': SyndicateMansion_MrX(player, multiworld),

        # Stage Selection
        'Menu': Menu(player, multiworld),
    }


def locations_() -> dict[str, int]:
    return {
        'Shopping Mall - Rach Shop Phone Booth 1 (Apple)': 0,
        'Shopping Mall - Rach Shop Phone Booth 2 (Bottle)': 1,
        'Shopping Mall - Rach Shop Phone Booth 3 (Pipe)': 2,
        'Shopping Mall - ABC Shop Phone Booth 1 (Nothing)': 3,
        'Shopping Mall - ABC Shop Phone Booth 2 (Bottle)': 4,
        'Shopping Mall - ABC Shop Phone Booth 3 (Nothing)': 5,
        'Shopping Mall - Boss Phone Booth (Chicken)': 6,
        'Shopping Mall - Stage Clear (Inner City Slums Key)': 7,
        'Inner City Slums - Red Bricks Door Barrel 1 (1000 Points)': 8,
        'Inner City Slums - Red Bricks Door Barrel 2 (Sleeping Powder)': 9,
        'Inner City Slums - Broken Windows Door Barrel 1 (Bottle)': 10,
        'Inner City Slums - Broken Windows Door Barrel 2 (Apple)': 11,
        'Inner City Slums - Graffiti Wall Barrel 1 (Bottle)': 12,
        'Inner City Slums - Graffiti Wall Barrel 2 (Extra Life)': 13,
        'Inner City Slums - Fence Barrel (Pipe)': 14,
        'Inner City Slums - Blue Brick Poster Barrel (Apple)': 15,
        'Inner City Slums - Blue Brick Before Boss Barrel (Knife)': 16,
        'Inner City Slums - Red Brick Boss Barrel (Chicken)': 17,
        'Inner City Slums - Stage Clear (Beachside Key)': 18,
        'Beachside - Before First Projector Tires (Baseball Bat)': 19,
        'Beachside - Third Fence Tires 1 (Apple)': 20,
        'Beachside - Third Fence Tires 2 (1000 Points)': 21,
        'Beachside - Third Fence Tires 3 (Chicken)': 22,
        'Beachside - Stage Clear (Bridge Under Construction Key)': 23,
        'Bridge Under Construction - First Hole Signalisation Block (Sleeping Powder)': 24,
        'Bridge Under Construction - First Hole Safety Barrier (1000 Points)': 25,
        'Bridge Under Construction - Second Hole Signalisation Pole (Apple)': 26,
        'Bridge Under Construction - Second Hole Signalisation Block (Extra Life)': 27,
        'Bridge Under Construction - Third Hole Signalisation Pole (Nothing)': 28,
        'Bridge Under Construction - Third Hole Safety Barrier 1 (1000 Points)': 29,
        'Bridge Under Construction - Third Hole Safety Barrier 2 (Apple)': 30,
        'Bridge Under Construction - Big Hole Signalisation Block 1 (Bottle)': 31,
        'Bridge Under Construction - Big Hole Signalisation Block 2 (Chicken)': 32,
        'Bridge Under Construction - Stage Clear (Aboard The Ferry Key)': 33,
        'Aboard The Ferry - Double Wooden Wall Container 1 (1000 Points)': 34,
        'Aboard The Ferry - Double Wooden Wall Container 2 (Sleeping Powder)': 35,
        'Aboard The Ferry - Double Wooden Wall Container 3 (1000 Points)': 36,
        'Aboard The Ferry - Double Wooden Wall Container 4 (Apple)': 37,
        'Aboard The Ferry - First Ladder Container (Chicken)': 38,
        'Aboard The Ferry - Before Second Ladder Container (Chicken)': 39,
        'Aboard The Ferry - Before Boss Container (Police)': 40,
        'Aboard The Ferry - Boss Container (Chicken)': 41,
        'Aboard The Ferry - Stage Clear (Factory Key)': 42,
        'Factory - First Treadmill Crate 1 (5000 Points)': 43,
        'Factory - First Treadmill Crate 2 (1000 Points)': 44,
        'Factory - Miniboss Crate 1 (Apple)': 45,
        'Factory - Miniboss Crate 2 (Chicken)': 46,
        'Factory - After Double Treadmill Crate 1 (Sleeping Powder)': 47,
        'Factory - After Double Treadmill Crate 2 (Nothing)': 48,
        'Factory - Before Big Single Treadmill Crate 1 (Police)': 49,
        'Factory - Before Big Single Treadmill Crate 2 (Extra Life)': 50,
        'Factory - Before Big Single Treadmill Crate 3 (Pipe)': 51,
        'Factory - Boss Crate (Chicken)': 52,
        'Factory - Stage Clear (Elevator Key)': 53,
        'Elevator - Stage Clear (Syndicate Mansion Key)': 54,
        'Syndicate Mansion - Before Stage 1 Boss Table 1 (Nothing)': 55,
        'Syndicate Mansion - Before Stage 1 Boss Table 2 (Nothing)': 56,
        'Syndicate Mansion - Stage 1 Boss Table (Apple)': 57,
        'Syndicate Mansion - Stage 2 Boss Table (Chicken)': 58,
        'Syndicate Mansion - Stage 3 Boss Table 1 (Sleeping Powder)': 59,
        'Syndicate Mansion - Stage 3 Boss Table 2 (Chicken)': 60,
        'Syndicate Mansion - Before Stage 4 Boss Table (Chicken)': 61,
        'Syndicate Mansion - Stage 4 Boss Table 1 (Knife)': 62,
        'Syndicate Mansion - Stage 4 Boss Table 2 (Sleeping Powder)': 63,
        'Syndicate Mansion - Stage 4 Boss Table 3 (Apple)': 64,
        'Syndicate Mansion - Before Stage 5 Boss Table (Nothing)': 65,
        'Syndicate Mansion - Stage 5 Boss Table (Chicken)': 66,
        'Syndicate Mansion - Twins (Nothing)': 67,
    }


def _set_rule(exit_: Entrance, exit_rule: Callable[[CollectionState, int], bool], player: int):
    set_rule(exit_, lambda state: exit_rule(state, player))


def set_rules(multiworld: MultiWorld, player: int):
    regions = [region for region in multiworld.get_regions() if region.player == player and region.__class__.__base__ is StreetsOfRageRegion]

    region: Type[StreetsOfRageRegion]
    for region in regions:
        for exit_, exit_access_rule in region.exits_.items():
            _set_rule(multiworld.get_entrance(f'{region.name} -> {exit_}', player), exit_access_rule, player)

    multiworld.completion_condition[player] = lambda state: state.has('Mr. X Defeated', player)