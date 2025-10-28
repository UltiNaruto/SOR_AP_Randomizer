import io
from typing import Any

from ..file_formats.smd import SMD
from ..patches.base_patches.constants import ConstantsPatch
from ..patches.base_patches.randomizer_loop import RandomizerLoop
from ..patches.base_patches.skip_to_options import SkipToOptions
from ..patches.base_patches.sram_patch import SRAMPatch
from ..patches.base_patches.timeout_client_func import TimeoutClientFunc
from ..utils.buffered_reader_be import BufferedReaderBE
from ..utils.buffered_writer_be import BufferedWriterBE


def apply_patches(config: dict[str, Any]) -> None:
    _game_version = '???'
    smd = SMD()
    smd.read(BufferedReaderBE(io.open(config['input_path'], 'rb')))

    if smd.header.system_type != 'SEGA MEGA DRIVE':
        raise RuntimeError("Unsupported console! Only the Megadrive/Genesis version is supported!")

    match smd.header.domestic_game_title:
        case "BARE KNUCKLE":
            match smd.header.region_support:
                case "JUE":
                    match smd.header.serial_number.revision:
                        case 0:
                            _game_version = 'w_rev00'
                        case _:
                            raise RuntimeError("Unsupported revision of Streets of Rage/Bare Knuckle!")
                case _:
                    raise RuntimeError("Unsupported region of Streets of Rage/Bare Knuckle!")
        case _:
            raise RuntimeError("Unsupported game. Only first Streets of Rage/Bare Knuckle game of the serie is supported!")

    # TODO: if game_version not w_rev00 then use bsdiff patch on known versions and reread the newly patched file

    # required by custom code
    smd.header.rom_address_range.end += 0x80000
    smd.datas += b'\xFF' * 0x80000

    PATCHES_TO_APPLY = [
        ConstantsPatch(
            config.get('seed_name', ''),
            config.get('slot_index', 0),
            config.get('easy_mode', False),
        ),
        SRAMPatch(),
        SkipToOptions(),
        TimeoutClientFunc(),
        RandomizerLoop(),
    ]

    for patch in PATCHES_TO_APPLY:
        patch.apply(smd)

    smd.write(BufferedWriterBE(io.open(config['output_path'], 'wb')))