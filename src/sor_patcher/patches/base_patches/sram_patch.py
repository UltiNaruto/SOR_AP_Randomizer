from ...data.patches import (
    INIT_SRAM_ADDRESS,
    INIT_SRAM_BYTES,
)
from ...file_formats.smd import RamType, SMD
from ...patches import Patch


class SRAMPatch(Patch):
    def apply(self, smd: SMD) -> None:
        # add SRAM support to save infos between 2 different sessions
        smd.header.serial_number.software_type = 'GM'
        smd.header.extra_memory.magic_number = 'RA'
        smd.header.extra_memory.ram_type = RamType.Save8BitOdd
        smd.header.extra_memory.address_range.start = 0x200000
        smd.header.extra_memory.address_range.end = 0x20FFFF

        # adds a function that initializes the SRAM if the magic word is not present
        smd.patch(
            INIT_SRAM_ADDRESS,
            INIT_SRAM_BYTES,
        )