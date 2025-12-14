import glob
import os
import pkgutil
import struct
import zipfile

from pathlib import Path
from typing import Optional

def _get_all_patches() -> dict[str, dict[str, int | Optional[bytes]]]:
    def _read_bin_file(bin: bytes) -> dict[str, int | Optional[bytes]]:
        return {
            "address": struct.unpack(">I",bin[0:4])[0],
            "data": bin[4:],
        }

    # Gathering all the patch names
    patch_dir = os.path.dirname(__file__)
    if '.apworld' in patch_dir:
        tmp_index = patch_dir.find(f'.apworld/')
        if tmp_index == -1:
            tmp_index = patch_dir.find(f'.apworld\\')
        if tmp_index == -1:
            raise RuntimeError("Shouldn't happen! Couldn't get apworld separator index for apworld path and inner path!")
        tmp_index += len('.apworld/')
        apworld_path = patch_dir[:tmp_index-1]
        patch_dir = f"{patch_dir[tmp_index:].replace('\\', '/')}/asm/"
        with zipfile.ZipFile(apworld_path) as zip:
            _all_patch_files = [
                f.replace(patch_dir, '')[:-4]
                for f in zip.namelist()
                if f.startswith(patch_dir) and f.endswith('.bin')
            ]
    else:
        _all_patch_files = [
            os.path.basename(f)[:-4] for f in glob.glob(str(Path(f"{patch_dir}/asm/*.bin")))
            if os.path.isfile(f) and not os.path.basename(f).startswith('__')
        ]

    # Reading each patches
    _patches = {}
    for patch_file in _all_patch_files:
        _patches[patch_file] = _read_bin_file(pkgutil.get_data(__package__, f"asm/{patch_file}.bin"))
    return _patches

global PATCHES
PATCHES: dict[str, dict[str, int | Optional[bytes]]] = _get_all_patches() # noqa

DATA_SECTION_ADDRESS: int = 0xE0000