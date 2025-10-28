import hashlib
import json
import os
import tempfile

from .sor_patcher.patcher import patch as sor_patch

import Utils
from settings import get_settings
from ..Files import APProcedurePatch, APPatchExtension

def get_base_rom_as_bytes() -> bytes:
    with open(get_settings().streets_of_rage_settings.rom_file, "rb") as infile:
        base_rom_bytes = bytes(Utils.read_snes_rom(infile))
    return base_rom_bytes


class StreetsOfRageMultiPatch(APPatchExtension):
    game = 'Streets of Rage'

    @staticmethod
    def apply_sor1_multi_patch(caller: APProcedurePatch, rom: bytes, patcher_file) -> bytes:
        input_md5 = hashlib.md5(rom).hexdigest()
        # SOR 1 (W) (REV00) MegaDrive
        if input_md5 == '569cfec15813294a8f0cf88cccc8c151':
            file_name = get_settings().streets_of_rage_settings['rom_file']

            try:
                fd, tmp_name = tempfile.mkstemp()
                patcher_json = json.loads(caller.get_file(patcher_file))
                patcher_json['input_path'] = file_name
                patcher_json['output_path'] = tmp_name
                sor_patch(json.dumps(patcher_json))
                with os.fdopen(fd, 'rb') as tmp:
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
