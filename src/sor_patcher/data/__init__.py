import glob
import os
import pkgutil
import struct

from pathlib import Path
from typing import Optional

global _all_patch_files
_all_patch_files: list[str] = [
    os.path.basename(f)[:-4] for f in glob.glob(str(Path(f"{os.path.dirname(__file__)}/asm/*.bin")))
    if os.path.isfile(f) and not os.path.basename(f).startswith('__')
]

def _get_all_patches() -> dict[str, dict[str, int | Optional[bytes]]]:
    def _read_bin_file(bin: bytes) -> dict[str, int | Optional[bytes]]:
        return {
            "address": struct.unpack(">I",bin[0:4])[0],
            "data": bin[4:],
        }

    _patches = {}
    for patch_file in _all_patch_files:
        _patches[patch_file] = _read_bin_file(pkgutil.get_data(__package__, f"asm/{patch_file}.bin"))
    return _patches

global PATCHES
# noinspection PyRedeclaration
PATCHES: dict[str, dict[str, int | Optional[bytes]]] = _get_all_patches()

DATA_SECTION_ADDRESS: int = 0xE0000