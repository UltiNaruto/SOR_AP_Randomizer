import json
import logging
import os
import pkgutil
import random
from pathlib import Path
from typing import ClassVar

from BaseClasses import ItemClassification, Item, Location, MultiWorld, Tutorial
from Options import Toggle
from worlds.AutoWorld import World, WebWorld

from .logic import locations_, regions_, set_rules

from .Items import StreetsOfRageItem
from .Options import StreetsOfRageOptions, streets_of_rage_option_groups
from .Rom import StreetsOfRageProcedurePatch
from .Settings import StreetsOfRageSettings
from .Utils import items_start_id, locations_start_id, STAGES

logger = logging.getLogger("Streets of Rage")

from . import client


# Will be removed once merged into Archipelago repo
def assert_apworld_properly_installed() -> None:
    path = Path(__file__).parent.resolve()
    parent_path = path.parent.parent.as_posix()
    lib_worlds_path = parent_path.replace("custom_worlds", f"lib/worlds/{os.path.basename(path.as_posix())}.apworld")
    if parent_path.endswith("lib/worlds"):
        raise RuntimeError("This apworld isn't allowed to be placed in lib/worlds."
                           "Please install this apworld through the launcher or place it in custom_worlds.")
    if parent_path.endswith("custom_worlds") and os.path.exists(lib_worlds_path):
        os.remove(lib_worlds_path)


class StreetsOfRageWeb(WebWorld):
    tutorial = [Tutorial(
        "Multiworld Setup Guide",
        "A guide to setting up the Streets of Rage on your computer. This guide covers single-player, multiworld, and related software.",
        "English",
        "data/setup_en.md",
        "setup/en",
        ["UltiNaruto"],
    )]

    option_groups = streets_of_rage_option_groups


class StreetsOfRageWorld(World):
    game = "Streets of Rage"
    topology_present = False
    data_version = 1

    settings_key = "streets_of_rage_settings"
    settings: ClassVar[StreetsOfRageSettings]

    options_dataclass = StreetsOfRageOptions
    options: StreetsOfRageOptions

    items: dict[str, dict[str, str | int]] = json.loads(str(pkgutil.get_data(__name__, "data/items/streets_of_rage.json"), 'utf-8'))
    item_name_to_id = {key: items_start_id() + value["index"] for key, value in items.items() if value["index"] < 65535}
    item_name_groups = {'Stage Keys': [name for name in item_name_to_id.keys() if name.endswith(' Key')]}
    location_name_to_id = {loc_name: locations_start_id() + idx for loc_name, idx in locations_().items()}
    web = StreetsOfRageWeb()
    required_client_version = (0, 6, 3)

    apworld_version = (0, 0, 4)
    starting_location: str = 'Shopping Mall'
    seed: int

    def __init__(self, multiworld: "MultiWorld", player: int):
        super().__init__(multiworld, player)

        assert_apworld_properly_installed()

    def generate_early(self) -> None:
        self.seed = self.random.randrange(99999999)
        self.starting_location = STAGES[self.options.start_location.value]
        self.push_precollected(self.create_item(f'{self.starting_location} Key'))

    def create_items(self) -> None:
        any_traps = self.options.game_over_traps.value == Toggle.option_true or \
                    self.options.death_traps.value == Toggle.option_true

        itempool = []
        for item_name, item in self.items.items():
            if any_traps and item_name == 'Nothing':
                continue

            # do not add Extra Life items if we are in easy mode
            # since we already have unlimited lives
            if self.options.easy_mode.value == Toggle.option_true and \
               item_name == 'Extra Life':
                continue

            # can't shuffle them yet since they aren't
            # spawnable yet
            if item_name in [
                'Baseball Bat',
                'Bottle',
                'Knife',
                'Pipe',
                'Sleeping Powder',
            ]:
                continue

            for _ in range(item["default_shuffled_count"]):
                itempool.append(item_name)

        itempool.remove(f'{self.starting_location} Key')

        # remove starting items from item pool
        items_to_exclude = [excluded_items.name
                            for excluded_items in self.multiworld.precollected_items[self.player]]

        for item in items_to_exclude:
            if item in itempool:
                itempool.remove(item)

        # add traps in pool if they are enabled
        trappool = []
        if self.options.game_over_traps.value == Toggle.option_true:
            trappool.append('Game Over Trap')
        if self.options.death_traps.value == Toggle.option_true:
            trappool.append('Death Trap')

        while len(itempool) < len(self.location_name_to_id):
            try:
                # randomly put filler or traps if enabled
                if not any_traps or self.random.random() >= 0.5:
                    itempool.append(self.get_filler_item_name())
                else:
                    itempool.append(random.choice(trappool))
            except IndexError:
                itempool.append('Nothing')

        itempool = list(map(lambda name: self.create_item(name), itempool))

        self.multiworld.itempool += itempool

    def create_item(self, name: str, location: Location | None = None) -> Item:
        try:
            i = self.items[name]
        except KeyError:
            # this is a nothing
            if name == 'Nothing':
                item = Item(name, ItemClassification.filler, None, self.player)
            # this is an event item
            else:
                item = Item(name, ItemClassification.progression, None, self.player)
            if location is not None:
                item.location = location
            return item

        classification = ItemClassification.filler
        match i["progression"]:
            case "progression":
                classification = ItemClassification.progression
            case "progression_deprioritized":
                classification = ItemClassification.progression_deprioritized
            case "progression_skip_balancing":
                classification = ItemClassification.progression_skip_balancing
            case "useful":
                classification = ItemClassification.useful
            case "deprioritized":
                classification = ItemClassification.deprioritized
            case "filler":
                classification = ItemClassification.filler
            case "skip_balancing":
                classification = ItemClassification.skip_balancing
            case "trap":
                classification = ItemClassification.trap

        return StreetsOfRageItem(name, classification, self.item_name_to_id[name], self.player)

    def set_rules(self) -> None:
        set_rules(self.multiworld, self.player)

    def get_filler_item_name(self) -> str:
        filler_items = [
            '1000 Points',
            '5000 Points',
            'Apple',
            'Chicken',
            'Police',
        ]
        if self.options.easy_mode.value == Toggle.option_false:
            filler_items.insert(4, 'Extra Life')
        self.random.shuffle(filler_items)
        return self.random.choice(filler_items)

    def create_regions(self):
        regions = regions_(self.player, self.multiworld)

        # Create all regions
        for _, r in regions.items():
            self.multiworld.regions += [r]
            for loc in r.locations:
                loc.show_in_spoiler = loc.address is not None

        # Connect all the remaining regions
        for region_name, r in regions.items():
            for exit_, _ in r.exits_.items():
                connection = r.create_exit(f"{region_name} -> {exit_}")
                connection.connect(self.multiworld.get_region(exit_, self.player))

    def fill_slot_data(self):
        options_dict = self.options.as_dict(
            "death_link", "death_traps", "game_over_traps", "stages_to_clear", "start_location"
        )
        options_dict.update({
            "seed": self.seed
        })
        return options_dict

    def generate_output(self, output_directory: str) -> None:
        patcher_json = {
            'seed_name': self.multiworld.seed_name,
            'slot_index': self.player,
            'easy_mode': self.options.easy_mode.value == Toggle.option_true,
        }

        patch = StreetsOfRageProcedurePatch(player=self.player, player_name=self.player_name)
        patch.write_file("patcher.json", json.dumps(patcher_json).encode("UTF-8"))
        out_file_name = self.multiworld.get_out_file_name_base(self.player)
        patch.write(os.path.join(output_directory, f"{out_file_name}{patch.patch_file_ending}"))
