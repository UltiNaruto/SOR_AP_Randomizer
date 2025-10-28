import logging
import re
from typing import Optional

from .Context import StreetsOfRageContext
from .GameInterface import GameInterface
from ..Utils import MAGIC_EMPTY_SEED, items_start_id, locations_start_id

from NetUtils import ClientStatus
# noinspection PyProtectedMember
from worlds._bizhawk import (
    disconnect as bizhawk_disconnect,
    read as bizhawk_read,
    ConnectorError,
    NotConnectedError,
    RequestFailedError,
    SyncError,
)
# noinspection PyProtectedMember
from worlds._bizhawk.client import BizHawkClient

logger = logging.getLogger("Client")


class StreetsOfRageClient(BizHawkClient):
    system = ('GEN',)
    patch_suffix = ('.apsor1',)
    disconnect_pending: bool = False
    game = 'Streets of Rage'
    game_state: bool = False
    has_new_checks: bool = False
    game_interface: Optional[GameInterface] = None

    @staticmethod
    async def get_rom_infos(ctx: StreetsOfRageContext) -> tuple[Optional[str], Optional[str], Optional[str]]:
        try:
            rom_infos = await bizhawk_read(ctx.bizhawk_ctx, [
                (0x150, 0x30, 'MD CART'),
                (0x180, 0x2, 'MD CART'),
                (0x1B0, 0x2, 'MD CART'),
            ])

            if len(rom_infos) != 3:
                raise RequestFailedError("Couldn't get rom infos!")

            return (
                    rom_infos[0].decode('utf-8').strip(' '),
                    rom_infos[1].decode('utf-8').strip(' '),
                    rom_infos[2].decode('utf-8').strip(' '),
                   )
        except ConnectorError:
            raise RuntimeError
        except NotConnectedError:
            raise RuntimeError
        except RequestFailedError:
            raise RuntimeError
        except SyncError:
            raise RuntimeError

    async def validate_rom(self, ctx: StreetsOfRageContext) -> bool:
        StreetsOfRageContext.init_custom_context(ctx)

        try:
            internal_name, software_type, sram = await StreetsOfRageClient.get_rom_infos(ctx)
        except RuntimeError:
            return False

        # by default sram is not used and software type isn't GM for vanilla rom
        if internal_name == 'STREETS OF RAGE' and \
           software_type == 'GM' and \
           sram == 'RA':
            ctx.game = self.game
            ctx.items_handling = 0b111
            ctx.finished_game = False
            self.game_interface = GameInterface(ctx)
            return True
        return False

    def on_package(self, ctx: StreetsOfRageContext, cmd: str, args: dict) -> None:
        if cmd == 'RoomInfo':
            logger.debug(f'{args['seed_name']=} ?= {ctx.rom_seed_name=}')
            ctx.remote_seed_name = f"{args['seed_name'][-20:]:20}"
            if ctx.rom_seed_name != ctx.remote_seed_name:
                if ctx.rom_seed_name != MAGIC_EMPTY_SEED:
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
            if "DeathLink" in args.get("tags", {}) and args["data"]["time"] not in ctx.previous_deathlinks:
                ctx.previous_deathlinks.add(args["data"]["time"])
                if self.game_interface.save_data is not None:
                    self.game_interface.save_data['deathl']['in'] += 1
        elif cmd == 'Connected':
            ctx.stored_data = {}
        elif cmd == "Retrieved":
            for (k,v) in args["keys"].items():
                ctx.stored_data[k] = v if v else 0
        elif cmd == 'PrintJSON':
            if args['type'] == 'ItemSend':
                if args['item'].player == ctx.slot:
                    text = re.sub(
                        r'\[/?(?:b|i|u|s|left|center|right|quote|code|list|img|spoil|color|ref).*?]',
                        '',
                        ctx.ui.json_to_kivy_parser(args['data'])
                    )
                    ctx.notifications.append(text)

        # noinspection PyTypeChecker
        super().on_package(ctx, cmd, args)

    async def handle_death_link(self, ctx: StreetsOfRageContext) -> None:
        is_alive = await self.game_interface.is_alive()

        # Death link is disabled
        if ctx.slot_data['death_link'] == 0:
            return

        if self.game_interface.was_alive and not is_alive:
            if ctx.slot_data['death_link'] > 0:
                self.game_interface.save_data['deathl']['out'] += 1
            self.game_interface.was_alive = False

        # Receiving death link
        if not f'{ctx.slot}_{ctx.team}_streets_of_rage_deathl_in' in ctx.stored_data:
            ctx.stored_data[f'{ctx.slot}_{ctx.team}_streets_of_rage_deathl_in'] = 0
        for i in range(self.game_interface.save_data['deathl']['in'] - ctx.stored_data[
            f'{ctx.slot}_{ctx.team}_streets_of_rage_deathl_in']):
            died = False
            while not died:
                p1 = await self.game_interface.get_entity(self.game_interface.player['address'])
                if p1 is None:
                    continue

                if p1['health'] <= 0:
                    continue

                await self.game_interface.kill()
            ctx.stored_data[f'{ctx.slot}_{ctx.team}_streets_of_rage_deathl_in'] += 1

        # Sending death link
        if not f'{ctx.slot}_{ctx.team}_streets_of_rage_deathl_out' in ctx.stored_data:
            ctx.stored_data[f'{ctx.slot}_{ctx.team}_streets_of_rage_deathl_out'] = 0
        for i in range(self.game_interface.save_data['deathl']['out'] - ctx.stored_data[
            f'{ctx.slot}_{ctx.team}_streets_of_rage_deathl_out']):
            await ctx.send_death("Player died")
            ctx.previous_deathlinks.add(ctx.last_death_link)
            ctx.stored_data[f'{ctx.slot}_{ctx.team}_streets_of_rage_deathl_out'] += 1

    async def handle_goal(self, ctx: StreetsOfRageContext) -> None:
        # noinspection PyBroadException
        try:
            current_stage = await self.game_interface.get_current_stage()
            has_beaten_final_boss = await self.game_interface.has_beaten_final_boss()

            # Finished game
            if current_stage == 7 and has_beaten_final_boss:
                await ctx.send_msgs([{"cmd": "StatusUpdate", "status": ClientStatus.CLIENT_GOAL}])
        except: # no idea why this disconnects us
            pass

    async def handle_ingame_inventory(self, ctx: StreetsOfRageContext) -> None:
        # TODO: Check for safe moments to spawn items (using RAM and patcher)

        for idx in ctx.ingame_items_received:
            if idx == 1:
                while not await self.game_interface.add_health(0x50):
                    pass
            if idx == 2:
                while not await self.game_interface.add_health(0x14):
                    pass
            if idx == 3:
                lives = await self.game_interface.get_lives()
                await self.game_interface.set_lives(min(lives + 1, 9))
            if idx == 4:
                if self.game_interface.current_stage < 7:
                    police = await self.game_interface.get_police()
                    await self.game_interface.set_police(min(police + 1, 9))
            # 5 to 9 are items to spawn
            if idx == 10:
                while not await self.game_interface.add_score(0x1000):
                    pass
            if idx == 11:
                while not await self.game_interface.add_score(0x5000):
                    pass

        # Do not allow police to be usable in stage 8 as it's broken at some point
        if self.game_interface.current_stage == 7:
            ctx.ingame_items_received = [it for it in ctx.ingame_items_received if it == 4]
        else:
            ctx.ingame_items_received.clear()

    async def handle_inventory(self, ctx: StreetsOfRageContext) -> None:
        # read inventory
        for it in ctx.items_received:
            it_idx = ctx.items_received.index(it)

            idx = it.item - items_start_id()

            # Stage key received
            if 12 <= idx <= 19:
                key_idx = idx - 12
                if not ctx.stage_keys[self.game_interface.stages[key_idx]]:
                    ctx.stage_keys[self.game_interface.stages[key_idx]] = True

            # Do not receive the same item twice
            if it_idx <= self.game_interface.save_data['last_received_item']:
                continue

            if 1 <= idx <= 11:
                ctx.ingame_items_received.append(idx)

            # Set last received item
            self.game_interface.save_data['last_received_item'] = it_idx
            await self.game_interface.write_last_received_item(it_idx)

    async def handle_locations(self, ctx: StreetsOfRageContext) -> None:
        collected_location = False

        for i in range(8):
            # Don't check for cleared objects in stage 7 and 9
            if i not in [6, 8]:
                start_idx = self.game_interface.stage_objects_start_loc_idx[i]
                end_idx = self.game_interface.stage_clear_loc_idx[i]
                for j in range(start_idx, end_idx):
                    loc_id = locations_start_id() + j
                    # Check if location for stage object was not sent
                    if j in self.game_interface.save_data['stages_objects_cleared'][self.game_interface.stages[i]] and \
                       loc_id not in ctx.checked_locations:
                        ctx.locations_checked.add(loc_id)
                    # Check if location for stage object was not collected
                    if j not in self.game_interface.save_data['stages_objects_cleared'][self.game_interface.stages[i]] and \
                       loc_id in ctx.checked_locations:
                        self.game_interface.save_data['stages_objects_cleared'][self.game_interface.stages[i]].append(j)
                        collected_location = True

            loc_id = locations_start_id() + self.game_interface.stage_clear_loc_idx[i]
            # Check if location for stage clear was not sent
            if not loc_id in ctx.checked_locations and \
               self.game_interface.save_data['stages_cleared'][self.game_interface.stages[i]]:
                ctx.locations_checked.add(loc_id)
            # Check if location for stage clear was not collected
            if loc_id in ctx.checked_locations and \
               not self.game_interface.save_data['stages_cleared'][self.game_interface.stages[i]]:
                self.game_interface.save_data['stages_cleared'][self.game_interface.stages[i]] = True
                collected_location = True

        if len(ctx.locations_checked) > 0:
            await ctx.send_msgs([{"cmd": "LocationChecks", "locations": list(ctx.locations_checked)}])
            ctx.locations_checked.clear()

        if collected_location:
            await self.game_interface.sync_checks()

    async def handle_notifications(self, ctx: StreetsOfRageContext) -> None:
        try:
            msg = ctx.notifications.pop()
            if msg is not None:
                await self.game_interface.display_message(msg)
        except IndexError:
            pass

    async def handle_request_stage_change(self, ctx: StreetsOfRageContext) -> None:
        requested_stage = await self.game_interface.get_requested_stage()
        if requested_stage is not None and requested_stage > 0:
            if requested_stage < 9:
                stage_name = self.game_interface.stages[requested_stage - 1]
                if ctx.stage_keys[stage_name]:
                    await self.game_interface.set_requested_stage_response(0xFF)
                    await self.game_interface.go_to_1player()
                else:
                    await self.game_interface.set_requested_stage_response(0)
                    await self.game_interface.display_message(f"You don't have the key for {stage_name} stage")
            else:
                stage_cleared_count = sum([1 for _, sc in self.game_interface.save_data['stages_cleared'].items() if sc])
                # you cannot request stage 9 if you haven't beaten stage 8 yet so add 1
                if not self.game_interface.save_data['stages_cleared']['Syndicate Mansion']:
                    stage_cleared_count += 1
                stages_to_clear = ctx.slot_data.get('stages_to_clear', 8)
                left_to_clear = max(0, stages_to_clear - stage_cleared_count)
                if left_to_clear == 0:
                    await self.game_interface.set_requested_stage_response(0xFF)
                else:
                    await self.game_interface.set_requested_stage_response(0)
                    await self.game_interface.display_message(f"You need to beat {left_to_clear} more stage{('s' if left_to_clear > 1 else '')}")

    async def game_watcher(self, ctx: StreetsOfRageContext) -> None:
        game_status = await self.game_interface.get_game_status()
        menu_state = await self.game_interface.get_menu_state()
        is_paused = await self.game_interface.is_paused()

        if (not ctx.server or not ctx.server.socket.open or ctx.server.socket.closed
            or ctx.remote_seed_name == MAGIC_EMPTY_SEED
            or getattr(ctx, "slot_data", None) is None):
            return

        # Read SRAM
        has_read_sram = await self.game_interface.read_save_to_sram()
        if has_read_sram is None or not has_read_sram:
            if not has_read_sram:
                await self.game_interface.reset_sram_datas()
            return

        # do not allow player to connect to different seeds than the one they are supposed to
        if self.game_interface.save_data['seed_name'] != ctx.remote_seed_name or \
           self.game_interface.save_data['slot'] != ctx.slot:
            await ctx.server.socket.close()
            bizhawk_disconnect(ctx.bizhawk_ctx)
            await self.game_interface.disconnect()
            return

        await self.game_interface.connect()

        if game_status < 0x10:
            self.game_interface.was_alive = False
            self.game_interface.current_stage = None
            await self.game_interface.update_current_stage(0)
            self.game_interface.prev_menu_state = 0

        # Options menu
        if game_status == 0x12:
            self.game_interface.was_alive = False
            self.game_interface.current_stage = None
            await self.game_interface.update_current_stage(0)

            if self.game_interface.prev_menu_state != menu_state:
                self.game_interface.prev_menu_state = menu_state

        # Credits
        if self.game_interface.prev_game_status == 0x24 and \
           game_status == 0x26:
            await self.handle_goal(ctx)

        # Ingame
        if game_status == 0x16 and not is_paused:
            current_stage = await self.game_interface.get_current_stage()

            # error while reading current stage?
            if current_stage is None:
                return

            # do not consider stage 9 as a valid stage and refer to stage 8 instead
            if current_stage == 8:
                current_stage = 7
            await self.game_interface.update_current_stage(current_stage + 1)

            # Get Player 1 only
            # noinspection PyBroadException
            try:
                self.game_interface.player = (await self.game_interface.get_players())[0]
            except:
                return

            is_alive = await self.game_interface.is_alive()

            await self.handle_death_link(ctx)

            # TODO: add player 2 support (MAYBE!)

            # Do not send anything if player is not alive
            if not is_alive:
                return

            await self.handle_ingame_inventory(ctx)

            self.game_interface.was_alive = is_alive

        await self.handle_request_stage_change(ctx)
        await self.handle_locations(ctx)
        await self.handle_inventory(ctx)
        await self.handle_notifications(ctx)

        if self.game_interface.prev_game_status != game_status:
            self.game_interface.prev_game_status = game_status
