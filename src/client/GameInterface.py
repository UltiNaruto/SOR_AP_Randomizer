import struct
from typing import Any, Optional, cast

from ..Utils import MAGIC_EMPTY_SEED, STAGES

# noinspection PyProtectedMember
import worlds._bizhawk as bizhawk


class GameInterface:
    prev_game_status: int = 0
    prev_menu_state: int = 0
    save_data: dict[str, Any] = {}
    stage_clear_loc_idx = [
        7,
        18,
        23,
        33,
        42,
        53,
        54,
        67,
        -1,
    ]
    stage_objects_start_loc_idx = [
        0,
        8,
        19,
        24,
        34,
        43,
        -1,
        55,
        -1,
    ]
    was_alive: bool = False

    @staticmethod
    async def get_rom_infos(ctx) -> tuple[Optional[str], Optional[str], Optional[str]]:
        try:
            rom_infos = await bizhawk.read(ctx.bizhawk_ctx, [
                (0x150, 0x30, 'MD CART'),
                (0x180, 0x2, 'MD CART'),
                (0x1B0, 0x2, 'MD CART'),
            ])

            if len(rom_infos) != 3:
                raise bizhawk.RequestFailedError("Couldn't get rom infos!")

            return (
                    rom_infos[0].decode('utf-8').strip(' '),
                    rom_infos[1].decode('utf-8').strip(' '),
                    rom_infos[2].decode('utf-8').strip(' '),
                   )
        except bizhawk.ConnectorError:
            raise RuntimeError
        except bizhawk.NotConnectedError:
            raise RuntimeError
        except bizhawk.RequestFailedError:
            raise RuntimeError
        except bizhawk.SyncError:
            raise RuntimeError

    @staticmethod
    async def get_game_status(ctx) -> int:
        try:
            status: list[bytes] = await bizhawk.read(ctx.bizhawk_ctx, [
                (0xFF01, 1, '68K RAM'),
            ])

            if len(status) <= 0:
                raise bizhawk.RequestFailedError("Couldn't read game state!")

            return status[0][0]
        except bizhawk.ConnectorError:
            return 0
        except bizhawk.NotConnectedError:
            return 0
        except bizhawk.RequestFailedError:
            return 0
        except bizhawk.SyncError:
            return 0

    @staticmethod
    async def get_menu_state(ctx) -> int:
        try:
            status: list[bytes] = await bizhawk.read(ctx.bizhawk_ctx, [
                (0xFB0F, 1, '68K RAM'),
            ])

            if len(status) <= 0:
                raise bizhawk.RequestFailedError("Couldn't read game state!")

            return status[0][0]
        except bizhawk.ConnectorError:
            return 0
        except bizhawk.NotConnectedError:
            return 0
        except bizhawk.RequestFailedError:
            return 0
        except bizhawk.SyncError:
            return 0

    @staticmethod
    async def has_beaten_final_boss(ctx) -> Optional[int]:
        try:
            final_boss_flag: list[bytes] = await bizhawk.read(ctx.bizhawk_ctx, [
                (0x14, 1, 'SRAM'),
            ])

            if len(final_boss_flag) <= 0:
                raise bizhawk.RequestFailedError("Couldn't read final boss flag!")

            return final_boss_flag[0][0] == 1
        except bizhawk.ConnectorError:
            return None
        except bizhawk.NotConnectedError:
            return None
        except bizhawk.RequestFailedError:
            return None
        except bizhawk.SyncError:
            return None

    @staticmethod
    async def get_current_stage(ctx) -> Optional[int]:
        try:
            current_stage: list[bytes] = await bizhawk.read(ctx.bizhawk_ctx, [
                (0xFF03, 1, '68K RAM'),
            ])

            if len(current_stage) <= 0:
                raise bizhawk.RequestFailedError("Couldn't read current stage!")

            return current_stage[0][0]
        except bizhawk.ConnectorError:
            return None
        except bizhawk.NotConnectedError:
            return None
        except bizhawk.RequestFailedError:
            return None
        except bizhawk.SyncError:
            return None

    @staticmethod
    async def get_requested_stage(ctx) -> Optional[int]:
        try:
            requested_stage: list[bytes] = await bizhawk.read(ctx.bizhawk_ctx, [
                (0xFFFD, 1, '68K RAM'),
            ])

            if len(requested_stage) <= 0:
                raise bizhawk.RequestFailedError("Couldn't read current stage!")

            return struct.unpack('b', requested_stage[0])[0]
        except bizhawk.ConnectorError:
            return None
        except bizhawk.NotConnectedError:
            return None
        except bizhawk.RequestFailedError:
            return None
        except bizhawk.SyncError:
            return None

    @staticmethod
    async def set_requested_stage_response(ctx, response: int) -> Optional[bool]:
        try:
            await bizhawk.write(ctx.bizhawk_ctx, [
                (0xFFFD, [response], '68K RAM'),
            ])

            return True
        except bizhawk.ConnectorError:
            return None
        except bizhawk.NotConnectedError:
            return None
        except bizhawk.RequestFailedError:
            return None
        except bizhawk.SyncError:
            return None

    @staticmethod
    async def get_players(ctx) -> list[dict[str, int | bytes]]:
        try:
            entity_entries_addresses = [(i, 2, '68K RAM') for i in range(0xB800, 0xBA00, 0x80)]
            entity_list_bytes: list[bytes] = await bizhawk.read(ctx.bizhawk_ctx, entity_entries_addresses)
            entity_entries_addresses = [addr for addr, _, _ in entity_entries_addresses]

            if len(entity_list_bytes) != len(entity_list_bytes):
                raise bizhawk.RequestFailedError("Couldn't read entity list!")

            players = [{
                'address': entity_entries_addresses[i],
                'datas': entity_list_bytes[i],
            } for i in range(len(entity_entries_addresses))
                if entity_list_bytes[i] != b'\0\0' and
                   entity_list_bytes[i][0] in [1, 2]
            ]

            return players
        except bizhawk.ConnectorError:
            return []
        except bizhawk.NotConnectedError:
            return []
        except bizhawk.RequestFailedError:
            return []
        except bizhawk.SyncError:
            return []

    @staticmethod
    async def get_entity(ctx, addr: int) -> Optional[dict[str, int]]:
        try:
            entity = await bizhawk.read(ctx.bizhawk_ctx, [
                (addr + 0x10, 2, '68K RAM'), # Position X
                (addr + 0x14, 2, '68K RAM'), # Position Y
                (addr + 0x30, 1, '68K RAM'), # Alive State
                (addr + 0x33, 1, '68K RAM'), # Health (for player)
                (addr + 0x41, 1, '68K RAM'), # Loot Type (for destructibles)
                (addr + 0x7a, 2, '68K RAM'), # Location ID
                (addr + 0x7c, 2, '68K RAM'), # Original Position X
                (addr + 0x7e, 2, '68K RAM'), # Original Position Y
            ])

            if len(entity) <= 0:
                raise bizhawk.RequestFailedError(f"Couldn't read entity at address RAM:{addr:04X}!")

            return {
                'x': struct.unpack('>H', entity[0])[0],
                'y': struct.unpack('>H', entity[1])[0],
                'state': struct.unpack('B', entity[2])[0],
                'health': struct.unpack('B', entity[3])[0],
                'loot_type': struct.unpack('B', entity[4])[0],
                'location_id': struct.unpack('>h', entity[5])[0],
                'original_x': struct.unpack('>H', entity[6])[0],
                'original_y': struct.unpack('>H', entity[7])[0],
            }
        except bizhawk.ConnectorError:
            return None
        except bizhawk.NotConnectedError:
            return None
        except bizhawk.RequestFailedError:
            return None
        except bizhawk.SyncError:
            return None

    @staticmethod
    async def get_lives(ctx) -> int:
        try:
            lives = await bizhawk.read(ctx.bizhawk_ctx, [
                (0xFF20, 1, '68K RAM'),
            ])

            if len(lives) <= 0:
                raise bizhawk.RequestFailedError("Couldn't get number of lives!")

            return struct.unpack('B', lives[0])[0]
        except bizhawk.ConnectorError:
            return 0
        except bizhawk.NotConnectedError:
            return 0
        except bizhawk.RequestFailedError:
            return 0
        except bizhawk.SyncError:
            return 0

    @staticmethod
    async def get_police(ctx) -> int:
        try:
            police = await bizhawk.read(ctx.bizhawk_ctx, [
                (0xFF21, 1, '68K RAM'),
            ])

            if len(police) <= 0:
                raise bizhawk.RequestFailedError("Couldn't get number of lives!")

            return struct.unpack('B', police[0])[0]
        except bizhawk.ConnectorError:
            return 0
        except bizhawk.NotConnectedError:
            return 0
        except bizhawk.RequestFailedError:
            return 0
        except bizhawk.SyncError:
            return 0

    @staticmethod
    async def is_paused(ctx) -> bool:
        try:
            paused: list[bytes] = await bizhawk.read(ctx.bizhawk_ctx, [
                (0xFA46, 1, '68K RAM'),
            ])

            if len(paused) <= 0:
                raise bizhawk.RequestFailedError("Couldn't check paused state!")

            return paused[0] != b'\x00'
        except bizhawk.ConnectorError:
            return True
        except bizhawk.NotConnectedError:
            return True
        except bizhawk.RequestFailedError:
            return True
        except bizhawk.SyncError:
            return True

    @staticmethod
    async def set_game_status(ctx, game_status: int) -> None:
        try:
            await bizhawk.write(ctx.bizhawk_ctx, [
                (0xFF01, [game_status], '68K RAM'),
            ])
        except bizhawk.ConnectorError:
            pass
        except bizhawk.NotConnectedError:
            pass
        except bizhawk.RequestFailedError:
            pass
        except bizhawk.SyncError:
            pass

    @staticmethod
    async def set_menu_state(ctx, menu_state: int) -> None:
        try:
            await bizhawk.write(ctx.bizhawk_ctx, [
                (0xFB0F, [menu_state], '68K RAM'),
            ])
        except bizhawk.ConnectorError:
            pass
        except bizhawk.NotConnectedError:
            pass
        except bizhawk.RequestFailedError:
            pass
        except bizhawk.SyncError:
            pass

    @staticmethod
    async def set_lives(ctx, lives: int) -> None:
        try:
            await bizhawk.write(ctx.bizhawk_ctx, [
                (0xFF20, [lives], '68K RAM'), # set lives
            ])
        except bizhawk.ConnectorError:
            pass
        except bizhawk.NotConnectedError:
            pass
        except bizhawk.RequestFailedError:
            pass
        except bizhawk.SyncError:
            pass

    @staticmethod
    async def set_police(ctx, police: int) -> None:
        try:
            await bizhawk.write(ctx.bizhawk_ctx, [
                (0xFF21, [police], '68K RAM'), # set police count
            ])
        except bizhawk.ConnectorError:
            pass
        except bizhawk.NotConnectedError:
            pass
        except bizhawk.RequestFailedError:
            pass
        except bizhawk.SyncError:
            pass

    @staticmethod
    async def add_score(ctx, val: int) -> bool:
        try:
            score = await bizhawk.read(ctx.bizhawk_ctx, [
                (0xFF08, 4, '68K RAM'),
            ])

            if len(score) != 1:
                raise bizhawk.RequestFailedError("Couldn't get score!")

            score_val = struct.unpack('>I', score[0])[0]
            await bizhawk.write(ctx.bizhawk_ctx, [
                (0xFF08, list(struct.pack('>I', score_val + val)), '68K RAM'),
            ])
            return True
        except bizhawk.ConnectorError:
            return False
        except bizhawk.NotConnectedError:
            return False
        except bizhawk.RequestFailedError:
            return False
        except bizhawk.SyncError:
            return False

    @staticmethod
    async def is_alive(ctx, player: int) -> bool:
        try:
            if ctx.players is None or len(ctx.players) == 0:
                return False

            p1 = await GameInterface.get_entity(ctx, ctx.players[player - 1]['address'])
            if p1 is None:
                return False

            if p1['health'] <= 0:
                return False

            return True
        except bizhawk.ConnectorError:
            return False
        except bizhawk.NotConnectedError:
            return False
        except bizhawk.RequestFailedError:
            return False
        except bizhawk.SyncError:
            return False

    @staticmethod
    async def kill(ctx) -> bool:
        try:
            await bizhawk.write(ctx.bizhawk_ctx, [
                (0xFA4A, [1], '68K RAM'), # Set timer to 1 frame
                (0xFA49, [1], '68K RAM'), # Activate Time Over penalty which results in death
            ])
            return True
        except bizhawk.ConnectorError:
            return False
        except bizhawk.NotConnectedError:
            return False
        except bizhawk.RequestFailedError:
            return False
        except bizhawk.SyncError:
            return False

    @staticmethod
    async def add_health(ctx, player: int, health: int) -> bool:
        try:
            if ctx.players is None or len(ctx.players) == 0:
                return False

            entity = await GameInterface.get_entity(ctx, ctx.players[player - 1]['address'])

            if entity is None:
                raise bizhawk.RequestFailedError("Couldn't get entity!")

            await bizhawk.write(ctx.bizhawk_ctx, [
                (ctx.players[player - 1]['address'] + 0x33, [min(entity['health'] + health, 0x50)], '68K RAM'), # Set health
            ])
            return True
        except bizhawk.ConnectorError:
            return False
        except bizhawk.NotConnectedError:
            return False
        except bizhawk.RequestFailedError:
            return False
        except bizhawk.SyncError:
            return False

    @staticmethod
    async def read_save_to_sram(ctx) -> Optional[dict[str, int|str|dict[str, list[int]|str]]]:
        try:
            ret = {
                'deathl': {
                    'in': 0,
                    'out': 0,
                },
                'deaths': 0,
                'last_received_item': -1,
                'seed_name': MAGIC_EMPTY_SEED if ctx.remote_seed_name is None else ctx.remote_seed_name,
                'slot': -1 if ctx.slot is None else ctx.slot,
                'stage_keys': {
                    'Shopping Mall': False,
                    'Inner City Slums': False,
                    'Beachside': False,
                    'Bridge Under Construction': False,
                    'Aboard The Ferry': False,
                    'Factory': False,
                    'Elevator': False,
                    'Syndicate Mansion': False,
                    'Mr. X': False,
                },
                'stages_cleared': {
                    'Shopping Mall': False,
                    'Inner City Slums': False,
                    'Beachside': False,
                    'Bridge Under Construction': False,
                    'Aboard The Ferry': False,
                    'Factory': False,
                    'Elevator': False,
                    'Syndicate Mansion': False,
                    'Mr. X': False,
                },
                'stages_objects_cleared': {
                    'Shopping Mall': [],
                    'Inner City Slums': [],
                    'Beachside': [],
                    'Bridge Under Construction': [],
                    'Aboard The Ferry': [],
                    'Factory': [],
                    'Elevator': [],
                    'Syndicate Mansion': [],
                },
            }

            sram_read_request: list[bytes] = await bizhawk.read(ctx.bizhawk_ctx, [
                (0, 0x78, 'SRAM'),   # magic word
            ])

            if len(sram_read_request) != 1:
                raise bizhawk.RequestFailedError("Couldn't read SRAM!")

            sram = sram_read_request[0]
            if sram[0x00:0x04] != b'SOR1':
                return None

            ret['last_received_item'] = struct.unpack('>i', sram[0x08:0x0C])[0]
            for i in range(9):
                ret['stages_cleared'][STAGES[i]] = sram[0x0C+i] > 0
            for i in range(8):
                if GameInterface.stage_objects_start_loc_idx[i] == -1:
                    continue
                tmp = struct.unpack('>H', sram[0x18+i*2:0x18+(i+1)*2])[0]
                for j in range(15):
                    if tmp & 1 == 1:
                        cast(list[int], cast(object, ret['stages_objects_cleared'][STAGES[i]])).append(GameInterface.stage_objects_start_loc_idx[i] + j)
                    tmp >>= 1
                    # no need to check further if the value is already 0
                    if tmp == 0:
                        break
            for i in range(9):
                ret['stage_keys'][STAGES[i]] = sram[0x28+i] > 0
            ret['deathl']['in'] = sram[0x34]
            ret['deathl']['out'] = sram[0x35]
            ret['deaths'] = sram[0x36]

            slot = struct.unpack('>h', sram[0x04:0x06])[0]
            if slot <= 0:
                return None

            ret['slot'] = slot

            seed_name_length = struct.unpack('>h', sram[0x37:0x39])[0]

            if seed_name_length == 0:
                ret['seed_name'] = ''
                return None

            seed_name = sram[0x39:0x78].decode('utf-8').rstrip('\0')
            if len(seed_name) == 0:
                return None

            if len(seed_name) != seed_name_length:
                raise RuntimeError(f'Mismatched length for seed name ({len(seed_name)} != {seed_name_length})')

            ret['seed_name'] = seed_name
            return ret
        except bizhawk.ConnectorError:
            return None
        except bizhawk.NotConnectedError:
            return None
        except bizhawk.RequestFailedError:
            return None
        except bizhawk.SyncError:
            return None

    @staticmethod
    async def reset_sram_datas(ctx) -> None:
        try:
            await bizhawk.write(ctx.bizhawk_ctx, [
                (0, list(b'\0\0\0\0'), 'SRAM'),
            ])
        except bizhawk.ConnectorError:
            pass
        except bizhawk.NotConnectedError:
            pass
        except bizhawk.RequestFailedError:
            pass
        except bizhawk.SyncError:
            pass

    @staticmethod
    async def sync_stage_keys(ctx) -> None:
        if ctx.save_data is None:
            return

        try:
            stage_keys = [0] * 9
            for i in range(9):
                if ctx.save_data['stage_keys'][STAGES[i]]:
                    stage_keys[i] = 1

            await bizhawk.write(ctx.bizhawk_ctx, [
                (0x28, stage_keys, 'SRAM'),
            ])
        except bizhawk.ConnectorError:
            pass
        except bizhawk.NotConnectedError:
            pass
        except bizhawk.RequestFailedError:
            pass
        except bizhawk.SyncError:
            pass

    @staticmethod
    async def sync_checks(ctx) -> None:
        if ctx.save_data is None:
            return

        try:
            stages_cleared = [0] * 9
            for i in range(9):
                if ctx.save_data['stages_cleared'][STAGES[i]]:
                    stages_cleared[i] = 1

            stages_objects_cleared = [0] * 16
            for i in range(8):
                if GameInterface.stage_objects_start_loc_idx[i] == -1:
                    continue
                tmp = 0
                for stage_object in ctx.save_data['stages_objects_cleared'][STAGES[i]]:
                    tmp |= (1 << (stage_object - GameInterface.stage_objects_start_loc_idx[i]))
                tmp2 = struct.pack('>h', tmp)
                stages_objects_cleared[i * 2] = tmp2[0]
                stages_objects_cleared[i * 2 + 1] = tmp2[1]

            await bizhawk.write(ctx.bizhawk_ctx, [
                (0xC, stages_cleared, 'SRAM'),
                (0x18, stages_objects_cleared, 'SRAM'),
            ])
        except bizhawk.ConnectorError:
            pass
        except bizhawk.NotConnectedError:
            pass
        except bizhawk.RequestFailedError:
            pass
        except bizhawk.SyncError:
            pass


    @staticmethod
    async def write_last_received_item(ctx, last_received_item: int) -> None:
        try:
            await bizhawk.write(ctx.bizhawk_ctx, [
                (8, struct.pack('>i', last_received_item), 'SRAM'),
            ])
        except bizhawk.ConnectorError:
            pass
        except bizhawk.NotConnectedError:
            pass
        except bizhawk.RequestFailedError:
            pass
        except bizhawk.SyncError:
            pass

    @staticmethod
    async def go_to_1player(ctx) -> None:
        try:
            current_stage = await GameInterface.get_current_stage(ctx)

            await bizhawk.write(ctx.bizhawk_ctx, [
                (0xFF18, [1], '68K RAM'), # Set to 1 player
                (0xFF21, [0 if current_stage == 8 else 1], '68K RAM')
            ])
            await GameInterface.set_game_status(ctx, 0x20)
        except bizhawk.ConnectorError:
            pass
        except bizhawk.NotConnectedError:
            pass
        except bizhawk.RequestFailedError:
            pass
        except bizhawk.SyncError:
            pass

    @staticmethod
    async def display_message(ctx, msg: str) -> None:
        try:
            await bizhawk.display_message(ctx.bizhawk_ctx, msg)
        except bizhawk.ConnectorError:
            pass
        except bizhawk.NotConnectedError:
            pass
        except bizhawk.RequestFailedError:
            pass
        except bizhawk.SyncError:
            pass

    @staticmethod
    async def set_message_interval(ctx, value: int) -> None:
        try:
            await bizhawk.set_message_interval(ctx.bizhawk_ctx, value)
        except bizhawk.ConnectorError:
            pass
        except bizhawk.NotConnectedError:
            pass
        except bizhawk.RequestFailedError:
            pass
        except bizhawk.SyncError:
            pass