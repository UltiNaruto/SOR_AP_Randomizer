import logging
from typing import Any, Callable, cast, List, Optional, TYPE_CHECKING

from .GameInterface import GameInterface
from ..Utils import get_attempted_command, items_start_id, locations_start_id, MAGIC_EMPTY_SEED, STAGES

from NetUtils import ClientStatus, RawJSONtoTextParser

# noinspection PyProtectedMember
from worlds._bizhawk.client import BizHawkClient

if TYPE_CHECKING:
    # noinspection PyProtectedMember
    from worlds._bizhawk.context import BizHawkClientContext


logger = logging.getLogger("Client")


async def update_current_stage(ctx, new_stage: int) -> None:
    # Update current stage for PopTracker
    if ctx.current_stage != new_stage:
        ctx.current_stage = new_stage
        await ctx.send_msgs([{
            'cmd': 'Set',
            'key': f'{ctx.slot}_{ctx.team}_streets_of_rage_area',
            'default': 0,
            'want_reply': True,
            'operations': [{
                'operation': 'replace',
                'value': new_stage,
            }]
        }])


def display_stages_access(ctx):
    logger.info('You have access to :')
    items_received = [it.item for it in ctx.items_received]
    for i in range(8):
        item_id = items_start_id() + 12 + i
        if item_id in items_received:
            logger.info(f'- {STAGES[i]} (Stage {i+1})')


class StreetsOfRageClient(BizHawkClient):
    system = ('GEN',)
    patch_suffix = ('.apsor1',)
    disconnect_pending: bool = False
    game = 'Streets of Rage'
    game_state: bool = False
    has_new_checks: bool = False
    ctx: Optional["BizHawkClientContext"] = None
    on_print_json_orig: Callable[[dict], None]

    def on_print_json(self, args: dict) -> None:
        valid_commands = [
            '!goal',
            '!keys',
        ]

        if self.ctx is not None:
            if args['type'] == 'Chat':
                text = RawJSONtoTextParser(self.ctx)(args["data"])
                if text.startswith(self.ctx.auth):
                    input_cmd = text[len(self.ctx.auth) + 2:]
                    if input_cmd in valid_commands:
                        return
            if args['type'] == 'CommandResult':
                text = RawJSONtoTextParser(self.ctx)(args["data"])
                input_cmd = get_attempted_command(text)
                if input_cmd is not None:
                    input_cmd = f'!{input_cmd}'
                    if input_cmd in valid_commands:
                        match input_cmd:
                            case '!goal':
                                stages_to_clear = self.ctx.slot_data["stages_to_clear"]  # type: ignore
                                logger.info(f'Your goal is to beat {stages_to_clear} stage{("s" if stages_to_clear > 1 else "")}')
                            case '!keys':
                                display_stages_access(self.ctx)  # type: ignore
                        return

        self.on_print_json_orig(args)

    async def validate_rom(self, ctx: "BizHawkClientContext") -> bool:
        try:
            internal_name, software_type, sram = await GameInterface.get_rom_infos(ctx)
        except RuntimeError:
            return False

        # by default sram is not used and software type isn't GM for vanilla rom
        if internal_name == 'STREETS OF RAGE' and \
           software_type == 'GM' and \
           sram == 'RA':
            ctx.current_stage = None
            ctx.players = [None]*2
            ctx.game = self.game
            ctx.items_handling = 0b111
            ctx.want_slot_data = True
            ctx.finished_game = False
            ctx.ingame_items_received = []
            ctx.logger = logging.getLogger("Streets of Rage")
            ctx.notifications = []
            if 'server_seed_name' not in ctx.__dict__:
                ctx.server_seed_name = None

            # noinspection PyUnreachableCode
            if ctx.server_seed_name:
                ctx.remote_seed_name = f"{ctx.server_seed_name[-20:]:20}"
                if len(ctx.locations_checked) != 0:
                    # This is in the hopes of avoiding sending reused data
                    ctx.locations_checked.clear()
                    ctx.locations_scouted.clear()
                    ctx.stored_data_notification_keys.clear()
                    ctx.checked_locations.clear()
            else:
                ctx.remote_seed_name = MAGIC_EMPTY_SEED
            ctx.rom_seed_name = MAGIC_EMPTY_SEED

            ctx.previous_deathlinks = set()
            ctx.my_stored_data = {}
            ctx.stage_keys = {
                'Shopping Mall': False,
                'Inner City Slums': False,
                'Beachside': False,
                'Bridge Under Construction': False,
                'Aboard The Ferry': False,
                'Factory': False,
                'Elevator': False,
                'Syndicate Mansion': False,
            }
            await GameInterface.set_message_interval(ctx, 0)

            self.ctx = ctx
            # hook CommonContext.on_print_json(args)
            self.on_print_json_orig = ctx.on_print_json
            ctx.on_print_json = self.on_print_json

            return True
        return False

    def on_package(self, ctx, cmd: str, args: dict) -> None:
        if cmd == 'RoomInfo':
            logger.debug(f'{args['seed_name']=} ?= {ctx.remote_seed_name=}') # type: ignore
            ctx.remote_seed_name = f"{args['seed_name'][-20:]:20}"
            if ctx.remote_seed_name != ctx.remote_seed_name:
                if ctx.remote_seed_name != MAGIC_EMPTY_SEED:
                    self.game_state = False
                    self.disconnect_pending = True
                if len(ctx.locations_checked) != 0:
                    # This is in the hopes of avoiding sending reused data
                    ctx.locations_checked.clear()
                    ctx.locations_scouted.clear()
                    ctx.stored_data_notification_keys.clear()
                    ctx.checked_locations.clear()
                ctx.stored_data = {}
        elif cmd == 'Bounced':
            if "DeathLink" in args.get("tags", {}) and args["data"]["time"] not in ctx.previous_deathlinks: # type: ignore
                ctx.previous_deathlinks.add(args["data"]["time"]) # type: ignore
                if ctx.save_data is not None: # type: ignore
                    ctx.save_data['deathl']['in'] += 1 # type: ignore
        elif cmd == 'Connected':
            ctx.stored_data = {}
        elif cmd == "Retrieved":
            for (k,v) in args["keys"].items():
                ctx.stored_data[k] = v if v else 0
        elif cmd == 'PrintJSON':
            if args['type'] == 'ItemSend':
                if args['item'].player == ctx.slot:
                    ctx.notifications.append(RawJSONtoTextParser(ctx)(args["data"])) # type: ignore
            if args['type'] == 'Tutorial':
                display_stages_access(ctx) # type: ignore

        # noinspection PyTypeChecker
        super().on_package(ctx, cmd, args)

    @staticmethod
    async def handle_death_link(ctx) -> None:
        is_alive = await GameInterface.is_alive(ctx, 1)

        # Death link is disabled
        if ctx.slot_data['death_link'] == 0:
            return

        if GameInterface.was_alive and not is_alive:
            if ctx.slot_data['death_link'] > 0:
                ctx.save_data['deathl']['out'] += 1
            GameInterface.was_alive = False

        # Receiving death link
        if not f'{ctx.slot}_{ctx.team}_streets_of_rage_deathl_in' in ctx.stored_data:
            ctx.stored_data[f'{ctx.slot}_{ctx.team}_streets_of_rage_deathl_in'] = 0
        for i in range(ctx.save_data['deathl']['in'] - ctx.stored_data[
            f'{ctx.slot}_{ctx.team}_streets_of_rage_deathl_in']):
            died = False
            while not died:
                p1 = await GameInterface.is_alive(ctx, 1)
                if not p1: # wait until player is alive again
                    continue

                await GameInterface.kill(ctx)
            ctx.stored_data[f'{ctx.slot}_{ctx.team}_streets_of_rage_deathl_in'] += 1

        # Sending death link
        if not f'{ctx.slot}_{ctx.team}_streets_of_rage_deathl_out' in ctx.stored_data:
            ctx.stored_data[f'{ctx.slot}_{ctx.team}_streets_of_rage_deathl_out'] = 0
        for i in range(ctx.save_data['deathl']['out'] - ctx.stored_data[
            f'{ctx.slot}_{ctx.team}_streets_of_rage_deathl_out']):
            await ctx.send_death("Player died")
            ctx.previous_deathlinks.add(ctx.last_death_link)
            ctx.stored_data[f'{ctx.slot}_{ctx.team}_streets_of_rage_deathl_out'] += 1

    @staticmethod
    async def handle_goal(ctx) -> None:
        # noinspection PyBroadException
        try:
            current_stage = await GameInterface.get_current_stage(ctx)
            has_beaten_final_boss = await GameInterface.has_beaten_final_boss(ctx)

            # Finished game
            if current_stage == 7 and has_beaten_final_boss and not ctx.finished_game:
                ctx.finished_game = True
                await ctx.send_msgs([{"cmd": "StatusUpdate", "status": ClientStatus.CLIENT_GOAL}])
        except: # no idea why this disconnects us
            pass

    @staticmethod
    async def handle_ingame_inventory(ctx) -> None:
        # TODO: Check for safe moments to spawn items (using RAM and patcher)

        for idx in ctx.ingame_items_received:
            if idx == 1:
                while not await GameInterface.add_health(ctx, 1, 0x50):
                    pass
            if idx == 2:
                while not await GameInterface.add_health(ctx, 1, 0x14):
                    pass
            if idx == 3:
                lives = await GameInterface.get_lives(ctx)
                await GameInterface.set_lives(ctx, min(lives + 1, 9))
            if idx == 4:
                if ctx.current_stage < 7:
                    police = await GameInterface.get_police(ctx)
                    await GameInterface.set_police(ctx, min(police + 1, 9))
            # 5 to 9 are items to spawn
            if idx == 10:
                while not await GameInterface.add_score(ctx, 0x1000):
                    pass
            if idx == 11:
                while not await GameInterface.add_score(ctx, 0x5000):
                    pass

        # Do not allow police to be usable in stage 8 as it's broken at some point
        if ctx.current_stage == 7:
            ctx.ingame_items_received = [it for it in ctx.ingame_items_received if it == 4]
        else:
            ctx.ingame_items_received.clear()

    @staticmethod
    async def handle_inventory(ctx) -> None:
        # read inventory
        for it in ctx.items_received:
            it_idx = ctx.items_received.index(it)

            idx = it.item - items_start_id()

            # Stage key received
            if 12 <= idx <= 19:
                key_idx = idx - 12
                if not ctx.stage_keys[STAGES[key_idx]]:
                    ctx.stage_keys[STAGES[key_idx]] = True

            # Do not receive the same item twice
            if it_idx <= ctx.save_data['last_received_item']:
                continue

            if 1 <= idx <= 11:
                ctx.ingame_items_received.append(idx)

            # Set last received item
            ctx.save_data['last_received_item'] = it_idx
            await GameInterface.write_last_received_item(ctx, it_idx)

    @staticmethod
    async def handle_locations(ctx) -> None:
        collected_location = False

        for i in range(8):
            # Don't check for cleared objects in stage 7 and 9
            if i not in [6, 8]:
                start_idx = GameInterface.stage_objects_start_loc_idx[i]
                end_idx = GameInterface.stage_clear_loc_idx[i]
                for j in range(start_idx, end_idx):
                    loc_id = locations_start_id() + j
                    # Check if location for stage object was not sent
                    if j in ctx.save_data['stages_objects_cleared'][STAGES[i]] and \
                       loc_id not in ctx.checked_locations:
                        ctx.locations_checked.add(loc_id)
                    # Check if location for stage object was not collected
                    if j not in ctx.save_data['stages_objects_cleared'][STAGES[i]] and \
                       loc_id in ctx.checked_locations:
                        ctx.save_data['stages_objects_cleared'][STAGES[i]].append(j)
                        collected_location = True

            loc_id = locations_start_id() + GameInterface.stage_clear_loc_idx[i]
            # Check if location for stage clear was not sent
            if not loc_id in ctx.checked_locations and \
               ctx.save_data['stages_cleared'][STAGES[i]]:
                ctx.locations_checked.add(loc_id)
            # Check if location for stage clear was not collected
            if loc_id in ctx.checked_locations and \
               not ctx.save_data['stages_cleared'][STAGES[i]]:
                ctx.save_data['stages_cleared'][STAGES[i]] = True
                collected_location = True

        if len(ctx.locations_checked) > 0:
            await ctx.send_msgs([{"cmd": "LocationChecks", "locations": list(ctx.locations_checked)}])
            ctx.locations_checked.clear()

        if collected_location:
            await GameInterface.sync_checks(ctx)

    @staticmethod
    async def handle_notifications(ctx) -> None:
        try:
            msg = ctx.notifications.pop()
            if msg is not None:
                await GameInterface.display_message(ctx, msg)
        except IndexError:
            pass

    @staticmethod
    async def handle_request_stage_change(ctx) -> None:
        requested_stage = await GameInterface.get_requested_stage(ctx)
        if requested_stage is not None and requested_stage > 0:
            if requested_stage < 9:
                stage_name = STAGES[requested_stage - 1]
                if ctx.stage_keys[stage_name]:
                    await GameInterface.set_requested_stage_response(ctx, 0xFF)
                    await GameInterface.go_to_1player(ctx)
                else:
                    await GameInterface.set_requested_stage_response(ctx, 0)
                    await GameInterface.display_message(ctx, f"You don't have the key for {stage_name} stage")
            else:
                stage_cleared_count = sum([1 for _, sc in ctx.save_data['stages_cleared'].items() if sc])
                # you cannot request stage 9 if you haven't beaten stage 8 yet so add 1
                if not ctx.save_data['stages_cleared']['Syndicate Mansion']:
                    stage_cleared_count += 1
                stages_to_clear = ctx.slot_data.get('stages_to_clear', 8)
                left_to_clear = max(0, stages_to_clear - stage_cleared_count)
                if left_to_clear == 0:
                    await GameInterface.set_requested_stage_response(ctx, 0xFF)
                else:
                    await GameInterface.set_requested_stage_response(ctx, 0)
                    await GameInterface.display_message(ctx, f"You need to beat {left_to_clear} more stage{('s' if left_to_clear > 1 else '')}")

    async def game_watcher(self, ctx) -> None:
        game_status = await GameInterface.get_game_status(ctx)
        menu_state = await GameInterface.get_menu_state(ctx)
        is_paused = await GameInterface.is_paused(ctx)

        if (not ctx.server or not ctx.server.socket.open or ctx.server.socket.closed
            or ctx.remote_seed_name == MAGIC_EMPTY_SEED # type: ignore
            or getattr(ctx, "slot_data", None) is None):
            return

        # Read SRAM
        ctx.save_data = await GameInterface.read_save_to_sram(ctx)
        if ctx.save_data is None:
            await GameInterface.reset_sram_datas(ctx)
            return

        # do not allow player to connect to different seeds than the one they are supposed to
        # noinspection PyUnresolvedReferences
        if ctx.save_data['seed_name'] != ctx.remote_seed_name or \
           ctx.save_data['slot'] != ctx.slot:
            await ctx.server.socket.close()
            await GameInterface.disconnect(ctx)
            return

        await GameInterface.connect(ctx)

        if game_status < 0x10:
            GameInterface.was_alive = False
            GameInterface.current_stage = None

            await update_current_stage(ctx, 0)# type: ignore
            GameInterface.prev_menu_state = 0

        # Options menu
        if game_status == 0x12:
            GameInterface.was_alive = False
            GameInterface.current_stage = None
            await update_current_stage(ctx, 0) # type: ignore

            if GameInterface.prev_menu_state != menu_state:
                GameInterface.prev_menu_state = menu_state

        # Credits
        if GameInterface.prev_game_status == 0x24 and \
           game_status == 0x26:
            await self.handle_goal(ctx)

        # Ingame
        if game_status == 0x16 and not is_paused:
            current_stage = await GameInterface.get_current_stage(ctx)

            # error while reading current stage?
            if current_stage is None:
                return

            await update_current_stage(ctx, current_stage + 1) # type: ignore

            # Get Player 1 only
            # noinspection PyBroadException
            try:
                ctx.players = await GameInterface.get_players(ctx)
            except:
                return

            is_alive = await GameInterface.is_alive(ctx, 1)

            await self.handle_death_link(ctx) # type: ignore

            # TODO: add player 2 support (MAYBE!)

            # Do not send anything if player is not alive
            if not is_alive:
                return

            await self.handle_ingame_inventory(ctx) # type: ignore

            GameInterface.was_alive = is_alive

        await self.handle_request_stage_change(ctx)
        await self.handle_locations(ctx) # type: ignore
        await self.handle_inventory(ctx) # type: ignore
        await self.handle_notifications(ctx) # type: ignore

        if GameInterface.prev_game_status != game_status:
            GameInterface.prev_game_status = game_status