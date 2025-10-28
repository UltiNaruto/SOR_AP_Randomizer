import struct

from ...data.patches import DATA_SECTION_ADDRESS
from ...file_formats.smd import SMD
from ...patches import Patch
from ...utils.byteutils import replace_bytes_at
from ...utils.padding import pad

stage_table: list[dict[str, list[int|tuple[int, int]]]] = [
    # Stage 1 - Shopping Mall
    {
        "object_types": [
            0x11,           # booth type
        ],
        "objects": [
            (0x7E0, 0x20),  # Rach Shop Phone Booth 1 (Apple)
            (0x890, 0x20),  # Rach Shop Phone Booth 2 (Bottle)
            (0x9A8, 0x20),  # Rach Shop Phone Booth 3 (Pipe)
            (0xB68, 0x20),  # ABC Shop Phone Booth 1 (Nothing)
            (0xB90, 0x20),  # ABC Shop Phone Booth 2 (Bottle)
            (0xBB8, 0x20),  # ABC Shop Phone Booth 3 (Nothing)
            (0xE58, 0x20),  # Boss Phone Booth (Chicken)
        ],
    },
    # Stage 2 - Inner City Slums
    {
        "object_types": [
            0x19,           # barrel type
        ],
        "objects": [
            (0x4D8, 0x38),  # Red Bricks Door Barrel 1 (1000 Points)
            (0x570, 0x38),  # Red Bricks Door Barrel 2 (Sleeping Powder)
            (0x708, 0x30),  # Broken Windows Door Barrel 1 (Bottle)
            (0x730, 0x30),  # Broken Windows Door Barrel 2 (Apple)
            (0x7E8, 0x30),  # Graffiti Wall Barrel 1 (Bottle)
            (0x838, 0x30),  # Graffiti Wall Barrel 2 (Extra Life)
            (0xA28, 0x30),  # Fence Barrel (Pipe)
            (0xB28, 0x30),  # Blue Brick Poster Barrel (Apple)
            (0xCC8, 0x60),  # Blue Brick Before Boss Barrel (Knife)
            (0xE40, 0x30),  # Red Brick Boss Barrel (Chicken)
        ],
    },
    # Stage 3 - Beachside
    {
        "object_types": [
            0x18,           # tires type
        ],
        "objects": [
            (0x460, 0x30),  # Before First Projector Tires (Baseball Bat)
            (0x7F0, 0x30),  # Third Fence Tires 1 (Apple)
            (0x888, 0x30),  # Third Fence Tires 2 (1000 Points)
            (0xA18, 0x30),  # Third Fence Tires 3 (Chicken)
        ],
    },
    # Stage 4 - Bridge Under Construction
    {
        "object_types": [
            0x1B,           # signalisation cone type
            0x1C,           # signalisation pole type
            0x1D,           # safety barrier type
        ],
        "objects": [
            (0x678, 0x60),  # First Hole Signalisation Block (Sleeping Powder)
            (0x718, 0x60),  # First Hole Safety Barrier (1000 Points)
            (0x880, 0x28),  # Second Hole Signalisation Pole (Apple)
            (0x940, 0x68),  # Second Hole Signalisation Block (Extra Life)
            (0x9C8, 0x28),  # Third Hole Signalisation Pole (Nothing)
            (0xA20, 0x30),  # Third Hole Safety Barrier 1 (1000 Points)
            (0xA40, 0x48),  # Third Hole Safety Barrier 2 (Apple)
            (0xB60, 0x28),  # Big Hole Signalisation Block 1 (Bottle)
            (0xD30, 0x20),  # Big Hole Signalisation Block 2 (Chicken)
        ],
    },
    # Stage 5 - Aboard The Ferry
    {
        "object_types": [
            0x1F,           # container type
        ],
        "objects": [
            (0x630, 0x38),  # Double Wooden Wall Container 1 (1000 Points)
            (0x670, 0x38),  # Double Wooden Wall Container 2 (Sleeping Powder)
            (0x630, 0x60),  # Double Wooden Wall Container 3 (1000 Points)
            (0x670, 0x60),  # Double Wooden Wall Container 4 (Apple)
            (0xB40, 0x30),  # First Ladder Container (Chicken)
            (0xE88, 0x20),  # Before Second Ladder Container (Chicken)
            (0x11A0, 0x48), # Before Boss Container (Police)
            (0x1420, 0x50), # Boss Container (Chicken)
        ],
    },
    # Stage 6 - Factory
    {
        "object_types": [
            0x41,           # crate type
        ],
        "objects": [
            (0x488, 0x30),  # First Treadmill Crate 1 (5000 Points)
            (0x548, 0x40),  # First Treadmill Crate 2 (1000 Points)
            (0x778, 0x50),  # Miniboss Crate 1 (Apple)
            (0x938, 0x50),  # Miniboss Crate 2 (Chicken)
            (0xD40, 0x20),  # After Double Treadmill Crate 1 (Sleeping Powder)
            (0xE20, 0x68),  # After Double Treadmill Crate 2 (Nothing)
            (0xFC0, 0x20),  # Before Big Single Treadmill Crate 1 (Police)
            (0x1008, 0x20), # Before Big Single Treadmill Crate 2 (Extra Life)
            (0x1040, 0x68), # Before Big Single Treadmill Crate 3 (Pipe)
            (0x1488, 0x50), # Boss Crate (Chicken)
        ],
    },
    # Stage 7 - Elevator
    {
        "object_types": [],
        "objects": [],
    },
    # Stage 8 - Syndicate Mansion
    {
        "object_types": [
            0x45,           # table type
        ],
        "objects": [
            (0x10D8, 0x20), # Before Stage 1 Boss Table 1 (Nothing)
            (0x1068, 0x50), # Before Stage 1 Boss Table 2 (Nothing)
            (0xF80, 0x20),  # Stage 1 Boss Table (Apple)
            (0xC80, 0x20),  # Stage 2 Boss Table (Chicken)
            (0xA18, 0x20),  # Stage 3 Boss Table 1 (Sleeping Powder)
            (0x960, 0x68),  # Stage 3 Boss Table 2 (Chicken)
            (0x770, 0x20),  # Before Stage 4 Boss Table (Chicken)
            (0x628, 0x68),  # Stage 4 Boss Table 1 (Knife)
            (0x5E8, 0x28),  # Stage 4 Boss Table 2 (Sleeping Powder)
            (0x550, 0x68),  # Stage 4 Boss Table 3 (Apple)
            (0x468, 0x68),  # Before Stage 5 Boss Table (Nothing)
            (0x380, 0x28),  # Stage 5 Boss Table (Chicken)
        ],
    },
]


class ConstantsPatch(Patch):
    seed_name: str
    slot_index: int
    easy_mode: bool

    def __init__(self, seed_name: str, slot_index: int, easy_mode: bool):
        self.seed_name = seed_name
        self.slot_index = slot_index
        self.easy_mode = easy_mode

    # we use the range 0x0E0000-0x0FFFFF for our constants
    def apply(self, smd: SMD) -> None:
        stage_count = 8
        pointer_to_object_types_for_stage = [DATA_SECTION_ADDRESS] * stage_count
        pointer_to_objects_for_stage = [DATA_SECTION_ADDRESS] * stage_count
        constants = b''

        # pre-allocate the size for pointer table
        offset_to_object_types_for_stage_pointers = len(constants)
        for i in range(len(pointer_to_object_types_for_stage)):
            constants += struct.pack('>I', 0)

        # pre-allocate the size for pointer table
        offset_to_objects_for_stage_pointers = len(constants)
        for i in range(len(pointer_to_objects_for_stage)):
            constants += struct.pack('>I', 0)

        # Easy mode (aka unlimited lives)
        constants += struct.pack('B', self.easy_mode)
        # Filler byte
        constants += b'\x00'
        # Slot index
        constants += struct.pack('>H', self.slot_index)
        # Seed name (length + data)
        constants += struct.pack('>I', len(self.seed_name))
        constants += bytes(self.seed_name, 'utf-8')
        constants += b'\x00' * (64 - len(self.seed_name))

        # stage datas (will be used in vblank loop to write to SRAM when we are ingame)
        for i in range(stage_count):
            pointer_to_object_types_for_stage[i] += len(constants)
            constants += struct.pack('B', len(stage_table[i]['object_types']))
            for object_type in stage_table[i]['object_types']:
                constants += struct.pack('B', object_type)

            # ugly hack to pad to 4 bytes - 1 for object count
            padded = pad(len(constants), 4)
            constants += b'\x00' * padded
            if padded == 0:
                constants += struct.pack('>I', 0)
            constants = constants[:-1]

            pointer_to_objects_for_stage[i] += len(constants)
            constants += struct.pack('B', len(stage_table[i]['objects']))
            constants += b''.join([
                struct.pack('>HH', x, y)
                for x, y in stage_table[i]['objects']
            ])

        for i in range(stage_count):
            constants = replace_bytes_at(
                constants,
                offset_to_object_types_for_stage_pointers + (i * 4),
                struct.pack('>I', pointer_to_object_types_for_stage[i])
            )
            constants = replace_bytes_at(
                constants,
                offset_to_objects_for_stage_pointers + (i * 4),
                struct.pack('>I', pointer_to_objects_for_stage[i])
            )

        smd.patch(DATA_SECTION_ADDRESS, constants)