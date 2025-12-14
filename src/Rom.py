import bsdiff4
import hashlib
import json
import os
import pkgutil
import tempfile

from typing import Mapping

from .sor_patcher.patcher import patch as sor_patch

import Utils
from settings import get_settings
from ..Files import APProcedurePatch, APPatchExtension


PATCH_FOR_VERSION: Mapping[str, str] = {
    # SOR 1 Megadrive - SEGA Mega Drive & Genesis Classic (3DS)
    '0de64a4f7dd5b0f11fbeea8c2c83f253': 'md_gen_classic_3ds',

    # SOR 1 Megadrive - SEGA Mega Drive & Genesis Classic (Steam)
    '59a3b22a1899461dceba50d1ade88d3a': 'md_gen_classic_steam',
}


def get_base_rom_as_bytes() -> bytes:
    with open(get_settings().streets_of_rage_settings.rom_file, "rb") as infile:
        base_rom_bytes = bytes(Utils.read_snes_rom(infile))

    input_md5 = hashlib.md5(base_rom_bytes).hexdigest()

    if input_md5 in PATCH_FOR_VERSION.keys():
        base_rom_bytes = bsdiff4.patch(
            base_rom_bytes,
            pkgutil.get_data(__name__[:__name__.rfind('.')], f'data/patches/{PATCH_FOR_VERSION[input_md5]}.bsdiff4')
        )

    return base_rom_bytes


class StreetsOfRageMultiPatch(APPatchExtension):
    game = 'Streets of Rage'

    @staticmethod
    def apply_sor1_multi_patch(caller: APProcedurePatch, rom: bytes, patcher_file) -> bytes:
        input_md5 = hashlib.md5(rom).hexdigest()
        # SOR 1 (W) (REV00) MegaDrive
        if input_md5 == '569cfec15813294a8f0cf88cccc8c151':
            try:
                src_fd, src_name = tempfile.mkstemp()
                dst_fd, dst_name = tempfile.mkstemp()
                bizhawk_version = '>=2.10' if get_settings().streets_of_rage_settings.using_2_10_plus_bizhawk_version else '<2.10'

                # copy base rom to temp file
                # will be used as input rom
                with os.fdopen(src_fd, 'wb') as tmp:
                    tmp.write(get_base_rom_as_bytes())

                # call patcher with modified paths
                patcher_json = json.loads(caller.get_file(patcher_file))
                patcher_json['input_path'] = src_name
                patcher_json['output_path'] = dst_name
                sor_patch(json.dumps(patcher_json), bizhawk_version)

                # read patched rom and return it
                with os.fdopen(dst_fd, 'rb') as tmp:
                    randomized_rom_data = tmp.read()

                return randomized_rom_data
            except:
                raise
        else:
            raise Exception("Supplied ROM doesn't match any of the supported ROMs!")


class StreetsOfRageProcedurePatch(APProcedurePatch):
    game = 'Streets of Rage'
    patch_file_ending = '.apsor1'
    result_file_ending = '.md'
    hash = 'Multiple'

    procedure = [
        ('apply_sor1_multi_patch', ["patcher.json"]),
    ]

    @classmethod
    def get_source_data(cls) -> bytes:
        return get_base_rom_as_bytes()
