import json


def patch(json_data: str, bizhawk_version: str) -> None:
    from .patches.game_patches import apply_patches

    apply_patches(json.loads(json_data), bizhawk_version)
