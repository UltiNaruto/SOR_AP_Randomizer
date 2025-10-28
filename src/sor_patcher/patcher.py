import json


def patch(json_data: str) -> None:
    from .patches.game_patches import apply_patches

    apply_patches(json.loads(json_data))
