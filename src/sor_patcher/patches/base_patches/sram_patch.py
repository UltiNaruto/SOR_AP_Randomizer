from ...data import PATCHES
from ...file_formats.smd import RamType, SMD
from ...patches import Patch


class SRAMPatch(Patch):
    def apply(self, smd: SMD) -> None:
        if "init_sram_func" not in PATCHES.keys():
            raise RuntimeError("Couldn't find init_sram_func in patches!")

        # add SRAM support to save infos between 2 different sessions
        smd.header.serial_number.software_type = 'GM'
        smd.header.extra_memory.magic_number = 'RA'
        smd.header.extra_memory.ram_type = RamType.Save8BitOdd
        smd.header.extra_memory.address_range.start = 0x200000
        smd.header.extra_memory.address_range.end = 0x20FFFF

        # adds a function that initializes the SRAM if the magic word is not present
        smd.patch(
            PATCHES["init_sram_func"]["address"],
            PATCHES["init_sram_func"]["data"],
        )