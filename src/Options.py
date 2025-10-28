from dataclasses import dataclass

from Options import Choice, DeathLink, OptionGroup, PerGameCommonOptions, Toggle, Range


class DeathTraps(Toggle):
    """Can you receive death traps?"""
    display_name = "Death Traps"


class EasyMode(Toggle):
    """Easy Mode gives unlimited lives"""
    display_name = "Easy Mode"


class GameOverTraps(Toggle):
    """Can you receive game over traps?"""
    display_name = "Game Over Traps"


class StartLocation(Choice):
    """Choose where you want to start the game."""
    display_name = "Starting Location"
    option_shopping_mall = 0
    option_inner_city_slums = 1
    option_beachside = 2
    option_bridge_under_construction = 3
    option_aboard_the_ferry = 4
    option_factory = 5
    option_elevator = 6
    option_syndicate_mansion = 7
    default = 0


class StagesToClear(Range):
    """Amount of stages required to reach goal."""
    display_name = "Stages To Clear"
    range_start = 4
    range_end = 8
    default = 8


@dataclass
class StreetsOfRageOptions(PerGameCommonOptions):
    death_link: DeathLink
    death_traps: DeathTraps
    easy_mode: EasyMode
    game_over_traps: GameOverTraps
    stages_to_clear: StagesToClear
    start_location: StartLocation


streets_of_rage_option_groups = [
    OptionGroup('Main Options', [
        StagesToClear,
        StartLocation,
    ]),
    OptionGroup("QoL Options", [
        EasyMode,
    ]),
    OptionGroup("Trap Options", [
        DeathTraps,
        GameOverTraps,
    ]),
]
