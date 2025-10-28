from typing import cast

from ...Options import StreetsOfRageOptions

from BaseClasses import CollectionState


def has_final_boss_access(state: CollectionState, player: int) -> bool:
    options = cast(StreetsOfRageOptions, state.multiworld.worlds[player].options)

    stages_cleared_count = state.count('Stage Clear', player)
    stages_to_clear = options.stages_to_clear.value

    return stages_cleared_count >= stages_to_clear