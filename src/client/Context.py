import logging
from typing import Any, cast, List, Optional

from NetUtils import Endpoint, NetworkItem
from ..Utils import MAGIC_EMPTY_SEED


class StreetsOfRageContext:
    # noinspection PyUnresolvedReferences
    bizhawk_ctx: "BizHawkContext"

    checked_locations: set[int]
    ingame_items_received: list[int]
    items_received: list[NetworkItem]
    last_death_link: float
    locations_checked: set[int]
    locations_scouted: set[int]
    logger: logging.Logger
    notifications: list[str]
    remote_seed_name: str
    rom_hash: str
    rom_seed_name: str
    previous_deathlinks: set
    server: Optional[Endpoint]
    slot: Optional[int]
    slot_data: Optional[dict[str, Any]]
    stored_data: dict[str, Any]
    stored_data_notification_keys: set[str]
    stage_keys: dict[str, bool]
    team: Optional[int]

    # noinspection PyUnresolvedReferences
    ui: Optional["kvui.GameManager"]

    # noinspection PyUnresolvedReferences
    @staticmethod
    def init_custom_context(ctx: "BizHawkClientContext") -> None:
        ctx = cast(StreetsOfRageContext, ctx)

        ctx.ingame_items_received = []
        ctx.logger = logging.getLogger("Client")
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

    async def send_death(self, death_text: str = "") -> None:
        pass

    async def send_msgs(self, msgs: List[Any]) -> None:
        pass