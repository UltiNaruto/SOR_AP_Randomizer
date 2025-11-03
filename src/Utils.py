import re
from typing import Optional

MAGIC_EMPTY_SEED = ' ' * 20
VERSION = "0.0.4"

STAGES: list[str] = [
    'Shopping Mall',
    'Inner City Slums',
    'Beachside',
    'Bridge Under Construction',
    'Aboard The Ferry',
    'Factory',
    'Elevator',
    'Syndicate Mansion',
    'Mr. X',
]


def condition_or(conditions: list[bool]) -> bool:
    result = False
    for condition in conditions:
        result = result or condition
    return result


def condition_and(conditions: list[bool]) -> bool:
    result = True
    for condition in conditions:
        if not (result and condition):
            return False
    return result


def items_start_id() -> int:
    return 0xDEAFF00D


def locations_start_id() -> int:
    return items_start_id() + 50


def strip_description_from_region_name(region_name: str):
    tmp = region_name.split(" - ")
    if len(tmp) != 1:
        raise Exception(f"Are you stripping description from a region name? (region_name: {region_name})")

    # Strip description if it exists
    part_to_remove = re.findall("\\(([^)]+)\\)", tmp[0])
    if part_to_remove is not None and len(part_to_remove) > 0:
        tmp[0] = tmp[0].replace(f" ({part_to_remove[0]})", "").strip()

    return tmp[0]


def get_attempted_command(text: str) -> Optional[str]:
    ret = re.match(r'^Could not find command (\w+)\. Known commands: (?:...)*', text)
    if not ret:
        return None
    else:
        return ret.group(1)