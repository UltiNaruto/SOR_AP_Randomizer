import struct
from typing import Any, Optional

# noinspection PyProtectedMember
from worlds._bizhawk import (
    display_message as bizhawk_display_msg,
    read as bizhawk_read,
    write as bizhawk_write,
    ConnectorError,
    NotConnectedError,
    RequestFailedError,
    SyncError,
)
from .Context import StreetsOfRageContext
from ..Utils import MAGIC_EMPTY_SEED, STAGES


class GameInterface:
    ctx: StreetsOfRageContext
    current_stage: Optional[int] = None
    player: dict[str, int | bytes] = {}
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

    def __init__(self, ctx: StreetsOfRageContext):
        self.ctx = ctx

    async def update_current_stage(self, new_stage: int) -> None:
        # Update current stage for PopTracker
        if self.current_stage != new_stage:
            self.current_stage = new_stage
            await self.ctx.send_msgs([{
                'cmd': 'Set',
                'key': f'{self.ctx.slot}_{self.ctx.team}_streets_of_rage_area',
                'default': 0,
                'want_reply': True,
                'operations': [{
                    'operation': 'replace',
                    'value': new_stage,
                }]
            }])

    async def get_game_status(self) -> int:
        try:
            status: list[bytes] = await bizhawk_read(self.ctx.bizhawk_ctx, [
                (0xFF01, 1, '68K RAM'),
            ])

            if len(status) <= 0:
                raise RequestFailedError("Couldn't read game state!")

            return status[0][0]
        except ConnectorError:
            return 0
        except NotConnectedError:
            return 0
        except RequestFailedError:
            return 0
        except SyncError:
            return 0

    async def get_menu_state(self) -> int:
        try:
            status: list[bytes] = await bizhawk_read(self.ctx.bizhawk_ctx, [
                (0xFB0F, 1, '68K RAM'),
            ])

            if len(status) <= 0:
                raise RequestFailedError("Couldn't read game state!")

            return status[0][0]
        except ConnectorError:
            return 0
        except NotConnectedError:
            return 0
        except RequestFailedError:
            return 0
        except SyncError:
            return 0

    async def has_beaten_final_boss(self) -> Optional[int]:
        try:
            final_boss_flag: list[bytes] = await bizhawk_read(self.ctx.bizhawk_ctx, [
                (0x14, 1, 'SRAM'),
            ])

            if len(final_boss_flag) <= 0:
                raise RequestFailedError("Couldn't read final boss flag!")

            return final_boss_flag[0][0] == 1
        except ConnectorError:
            return None
        except NotConnectedError:
            return None
        except RequestFailedError:
            return None
        except SyncError:
            return None

    async def get_current_stage(self) -> Optional[int]:
        try:
            current_stage: list[bytes] = await bizhawk_read(self.ctx.bizhawk_ctx, [
                (0xFF03, 1, '68K RAM'),
            ])

            if len(current_stage) <= 0:
                raise RequestFailedError("Couldn't read current stage!")

            return current_stage[0][0]
        except ConnectorError:
            return None
        except NotConnectedError:
            return None
        except RequestFailedError:
            return None
        except SyncError:
            return None

    async def get_requested_stage(self) -> Optional[int]:
        try:
            requested_stage: list[bytes] = await bizhawk_read(self.ctx.bizhawk_ctx, [
                (0xFFFD, 1, '68K RAM'),
            ])

            if len(requested_stage) <= 0:
                raise RequestFailedError("Couldn't read current stage!")

            return struct.unpack('b', requested_stage[0])[0]
        except ConnectorError:
            return None
        except NotConnectedError:
            return None
        except RequestFailedError:
            return None
        except SyncError:
            return None

    async def set_requested_stage_response(self, response: int) -> Optional[bool]:
        try:
            await bizhawk_write(self.ctx.bizhawk_ctx, [
                (0xFFFD, [response], '68K RAM'),
            ])

            return True
        except ConnectorError:
            return None
        except NotConnectedError:
            return None
        except RequestFailedError:
            return None
        except SyncError:
            return None

    async def get_players(self) -> list[dict[str, int | bytes]]:
        try:
            entity_entries_addresses = [(i, 2, '68K RAM') for i in range(0xB800, 0xBA00, 0x80)]
            entity_list_bytes: list[bytes] = await bizhawk_read(self.ctx.bizhawk_ctx, entity_entries_addresses)
            entity_entries_addresses = [addr for addr, _, _ in entity_entries_addresses]

            if len(entity_list_bytes) != len(entity_list_bytes):
                raise RequestFailedError("Couldn't read entity list!")

            players = [{
                'address': entity_entries_addresses[i],
                'datas': entity_list_bytes[i],
            } for i in range(len(entity_entries_addresses))
                if entity_list_bytes[i] != b'\0\0' and
                   entity_list_bytes[i][0] in [1, 2]
            ]

            return players
        except ConnectorError:
            return []
        except NotConnectedError:
            return []
        except RequestFailedError:
            return []
        except SyncError:
            return []

    async def get_entity(self, addr: int) -> Optional[dict[str, int]]:
        try:
            entity = await bizhawk_read(self.ctx.bizhawk_ctx, [
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
                raise RequestFailedError(f"Couldn't read entity at address RAM:{addr:04X}!")

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
        except ConnectorError:
            return None
        except NotConnectedError:
            return None
        except RequestFailedError:
            return None
        except SyncError:
            return None

    async def get_lives(self) -> int:
        try:
            lives = await bizhawk_read(self.ctx.bizhawk_ctx, [
                (0xFF20, 1, '68K RAM'),
            ])

            if len(lives) <= 0:
                raise RequestFailedError("Couldn't get number of lives!")

            return struct.unpack('B', lives[0])[0]
        except ConnectorError:
            return 0
        except NotConnectedError:
            return 0
        except RequestFailedError:
            return 0
        except SyncError:
            return 0

    async def get_police(self) -> int:
        try:
            police = await bizhawk_read(self.ctx.bizhawk_ctx, [
                (0xFF21, 1, '68K RAM'),
            ])

            if len(police) <= 0:
                raise RequestFailedError("Couldn't get number of lives!")

            return struct.unpack('B', police[0])[0]
        except ConnectorError:
            return 0
        except NotConnectedError:
            return 0
        except RequestFailedError:
            return 0
        except SyncError:
            return 0

    async def is_paused(self) -> bool:
        try:
            paused: list[bytes] = await bizhawk_read(self.ctx.bizhawk_ctx, [
                (0xFA46, 1, '68K RAM'),
            ])

            if len(paused) <= 0:
                raise RequestFailedError("Couldn't check paused state!")

            return paused[0] != b'\x00'
        except ConnectorError:
            return True
        except NotConnectedError:
            return True
        except RequestFailedError:
            return True
        except SyncError:
            return True

    async def set_game_status(self, game_status: int) -> None:
        try:
            await bizhawk_write(self.ctx.bizhawk_ctx, [
                (0xFF01, [game_status], '68K RAM'),
            ])
        except ConnectorError:
            pass
        except NotConnectedError:
            pass
        except RequestFailedError:
            pass
        except SyncError:
            pass

    async def set_menu_state(self, menu_state: int) -> None:
        try:
            await bizhawk_write(self.ctx.bizhawk_ctx, [
                (0xFB0F, [menu_state], '68K RAM'),
            ])
        except ConnectorError:
            pass
        except NotConnectedError:
            pass
        except RequestFailedError:
            pass
        except SyncError:
            pass

    async def set_lives(self, lives: int) -> None:
        try:
            await bizhawk_write(self.ctx.bizhawk_ctx, [
                (0xFF20, [lives], '68K RAM'), # set lives
            ])
        except ConnectorError:
            pass
        except NotConnectedError:
            pass
        except RequestFailedError:
            pass
        except SyncError:
            pass

    async def set_police(self, police: int) -> None:
        try:
            await bizhawk_write(self.ctx.bizhawk_ctx, [
                (0xFF21, [police], '68K RAM'), # set police count
            ])
        except ConnectorError:
            pass
        except NotConnectedError:
            pass
        except RequestFailedError:
            pass
        except SyncError:
            pass

    async def add_score(self, val: int) -> bool:
        try:
            score = await bizhawk_read(self.ctx.bizhawk_ctx, [
                (0xFF08, 4, '68K RAM'),
            ])

            if len(score) != 1:
                raise RequestFailedError("Couldn't get score!")

            score_val = struct.unpack('>I', score[0])[0]
            await bizhawk_write(self.ctx.bizhawk_ctx, [
                (0xFF08, list(struct.pack('>I', score_val + val)), '68K RAM'),
            ])
            return True
        except ConnectorError:
            return False
        except NotConnectedError:
            return False
        except RequestFailedError:
            return False
        except SyncError:
            return False

    async def is_alive(self) -> bool:
        try:
            p1 = await self.get_entity(self.player['address'])
            if p1 is None:
                return False

            if p1['health'] <= 0:
                return False

            return True
        except ConnectorError:
            return False
        except NotConnectedError:
            return False
        except RequestFailedError:
            return False
        except SyncError:
            return False

    async def kill(self) -> bool:
        try:
            await bizhawk_write(self.ctx.bizhawk_ctx, [
                (0xFA4A, [1], '68K RAM'), # Set timer to 1 frame
                (0xFA49, [1], '68K RAM'), # Activate Time Over penalty which results in death
            ])
            return True
        except ConnectorError:
            return False
        except NotConnectedError:
            return False
        except RequestFailedError:
            return False
        except SyncError:
            return False

    async def add_health(self, health: int) -> bool:
        try:
            entity = await self.get_entity(self.player['address'])

            if entity is None:
                raise RequestFailedError("Couldn't get entity!")

            await bizhawk_write(self.ctx.bizhawk_ctx, [
                (self.player['address'] + 0x33, [min(entity['health'] + health, 0x50)], '68K RAM'), # Set health
            ])
            return True
        except ConnectorError:
            return False
        except NotConnectedError:
            return False
        except RequestFailedError:
            return False
        except SyncError:
            return False

    async def read_save_to_sram(self) -> Optional[bool]:
        try:
            self.save_data = {
                'deathl': {
                    'in': 0,
                    'out': 0,
                },
                'deaths': 0,
                'last_received_item': -1,
                'seed_name': MAGIC_EMPTY_SEED if self.ctx.remote_seed_name is None else self.ctx.remote_seed_name,
                'slot': -1 if self.ctx.slot is None else self.ctx.slot,
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

            sram_read_request: list[bytes] = await bizhawk_read(self.ctx.bizhawk_ctx, [
                (0, 0x6C, 'SRAM'),   # magic word
            ])

            if len(sram_read_request) != 1:
                raise RequestFailedError("Couldn't read SRAM!")

            sram = sram_read_request[0]
            if sram[0x00:0x04] != b'SOR1':
                return False

            self.save_data['last_received_item'] = struct.unpack('>i', sram[0x08:0x0C])[0]
            for i in range(9):
                self.save_data['stages_cleared'][STAGES[i]] = sram[0x0C+i] > 0
            for i in range(8):
                if self.stage_objects_start_loc_idx[i] == -1:
                    continue
                tmp = struct.unpack('>H', sram[0x18+i*2:0x18+(i+1)*2])[0]
                for j in range(15):
                    if tmp & 1 == 1:
                        self.save_data['stages_objects_cleared'][STAGES[i]].append(self.stage_objects_start_loc_idx[i] + j)
                    tmp >>= 1
                    # no need to check further if the value is already 0
                    if tmp == 0:
                        break
            self.save_data['deathl']['in'] = sram[0x29]
            self.save_data['deathl']['out'] = sram[0x2A]
            self.save_data['deaths'] = sram[0x2B]

            slot = struct.unpack('>h', sram[0x04:0x06])[0]
            if slot <= 0:
                return False

            self.save_data['slot'] = slot

            seed_name_length = struct.unpack('>h', sram[0x2B:0x2D])[0]

            if seed_name_length == 0:
                self.save_data['seed_name'] = ''
                return False

            seed_name = sram[0x2D:0x6C].decode('utf-8').rstrip('\0')
            if len(seed_name) == 0:
                return False

            self.save_data['seed_name'] = seed_name
            return True
        except ConnectorError:
            return None
        except NotConnectedError:
            return None
        except RequestFailedError:
            return None
        except SyncError:
            return None

    async def reset_sram_datas(self) -> None:
        try:
            await bizhawk_write(self.ctx.bizhawk_ctx, [
                (0, list(b'\0\0\0\0'), 'SRAM'),
            ])
        except ConnectorError:
            pass
        except NotConnectedError:
            pass
        except RequestFailedError:
            pass
        except SyncError:
            pass

    async def sync_checks(self) -> None:
        try:
            stages_cleared = [0] * 9
            for i in range(9):
                if self.save_data['stages_cleared'][STAGES[i]]:
                    stages_cleared[i] = 1

            stages_objects_cleared = [0] * 16
            for i in range(8):
                if self.stage_objects_start_loc_idx[i] == -1:
                    continue
                tmp = 0
                for stage_object in self.save_data['stages_objects_cleared'][STAGES[i]]:
                    tmp |= (1 << (stage_object - self.stage_objects_start_loc_idx[i]))
                tmp2 = struct.pack('>h', tmp)
                stages_objects_cleared[i * 2] = tmp2[0]
                stages_objects_cleared[i * 2 + 1] = tmp2[1]

            await bizhawk_write(self.ctx.bizhawk_ctx, [
                (0xC, stages_cleared, 'SRAM'),
                (0x18, stages_objects_cleared, 'SRAM'),
            ])
        except ConnectorError:
            pass
        except NotConnectedError:
            pass
        except RequestFailedError:
            pass
        except SyncError:
            pass


    async def write_last_received_item(self, last_received_item: int) -> None:
        try:
            await bizhawk_write(self.ctx.bizhawk_ctx, [
                (8, struct.pack('>i', last_received_item), 'SRAM'),
            ])
        except ConnectorError:
            pass
        except NotConnectedError:
            pass
        except RequestFailedError:
            pass
        except SyncError:
            pass

    async def go_to_1player(self) -> None:
        try:
            current_stage = await self.get_current_stage()

            await bizhawk_write(self.ctx.bizhawk_ctx, [
                (0xFF18, [1], '68K RAM'), # Set to 1 player
                (0xFF21, [0 if current_stage == 8 else 1], '68K RAM')
            ])
            await self.set_game_status(0x20)
        except ConnectorError:
            pass
        except NotConnectedError:
            pass
        except RequestFailedError:
            pass
        except SyncError:
            pass

    async def display_message(self, msg: str) -> None:
        await bizhawk_display_msg(self.ctx.bizhawk_ctx, msg)

    async def connect(self):
        try:
            await bizhawk_write(self.ctx.bizhawk_ctx, [
                (0xFFFE, [1], '68K RAM'),
            ])
        except ConnectorError:
            pass
        except NotConnectedError:
            pass
        except RequestFailedError:
            pass
        except SyncError:
            pass

    async def disconnect(self):
        try:
            await bizhawk_write(self.ctx.bizhawk_ctx, [
                (0xFFFE, [0], '68K RAM'),
            ])
        except ConnectorError:
            pass
        except NotConnectedError:
            pass
        except RequestFailedError:
            pass
        except SyncError:
            pass