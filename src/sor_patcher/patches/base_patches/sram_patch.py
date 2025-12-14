from ...data import PATCHES
from ...file_formats.smd import RamType, SMD
from ...patches import Patch
from ...utils.byteutils import replace_bytes_at


class SRAMPatch(Patch):
    bizhawk_version: str

    def __init__(self, bizhawk_version: str):
        self.bizhawk_version = bizhawk_version

    def apply(self, smd: SMD) -> None:
        if "init_sram_func" not in PATCHES.keys():
            raise RuntimeError("Couldn't find init_sram_func in patches!")

        # add SRAM support to save infos between 2 different sessions
        smd.header.serial_number.software_type = 'GM'
        smd.header.extra_memory.magic_number = 'RA'
        smd.header.extra_memory.ram_type = RamType.Save8BitOdd
        smd.header.extra_memory.address_range.start = 0x200000
        smd.header.extra_memory.address_range.end = 0x20FFFF

        init_sram_func_data = PATCHES["init_sram_func"]["data"]
        if self.bizhawk_version == '>=2.10':
            init_sram_func_data = replace_bytes_at(init_sram_func_data, 0x17A, b'\x22\x48\x4E\x75')
            init_sram_func_data = replace_bytes_at(init_sram_func_data, 0x17E, b'\0' * (len(init_sram_func_data) - 0x17E))

        # adds a function that initializes the SRAM if the magic word is not present
        smd.patch(
            PATCHES["init_sram_func"]["address"],
            init_sram_func_data,
        )