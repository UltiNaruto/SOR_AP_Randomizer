import glob
import importlib
import inspect
import os
import re
from itertools import chain
from pathlib import Path
from types import ModuleType
from typing import Iterable, Optional, TypeVar, Union

MAGIC_EMPTY_SEED = ' ' * 20
VERSION = "0.1.4"

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


T = TypeVar('T')


def _import_all_submodules(mod: Union[str, ModuleType], parent_submodule="") -> list[ModuleType]:
    if type(mod) is str:
        path = Path(mod)
        if parent_submodule == "":
            parent_submodule = f"{__package__}.{os.path.basename(mod)}"
    elif type(mod) is ModuleType:
        path = Path(mod.__file__).parent
        if parent_submodule == "":
            parent_submodule = f"{__package__}.{os.path.basename(str(path))}"
    else:
        raise RuntimeError("Shouldn't happen, but import_all_submodules first argument is not str or ModuleType!")

    submodules = glob.glob(f"{str(path)}/*")
    submodules = [
        *[os.path.basename(f)[:-3] for f in submodules if # exclude __init__.py
         (os.path.isfile(f) and not os.path.basename(f).startswith('__') and Path(f).suffix == ".py")],
        *[f for f in submodules
          if os.path.isdir(f)],
    ]
    ret = []
    for submodule in submodules:
        if os.path.isdir(submodule):
            ret.extend(_import_all_submodules(submodule, f'{parent_submodule}.{os.path.basename(submodule)}'))
        else:
            ret.append(importlib.import_module(f".{submodule}", parent_submodule))
    return ret


def get_all_classes_from_parent_module(mod: ModuleType, _type: T) -> list[T]:
    def get_all_classes_from_module(m: ModuleType) -> Iterable[T]:
        ret = []
        for name, obj in inspect.getmembers(m, inspect.isclass):
            if obj.__module__ == m.__name__:
                ret.append(obj)
        return ret

    mods = _import_all_submodules(mod)
    return sorted(list(chain.from_iterable([
        get_all_classes_from_module(mod)
        for mod in mods
    ])), key=lambda x: x.__name__)


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
    tmp = region_name.split(" - ", 1)
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