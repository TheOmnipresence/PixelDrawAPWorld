from collections.abc import Mapping
from typing import Any

# Imports of base Archipelago modules must be absolute.
from worlds.AutoWorld import World

# Imports of your world's files must be relative.
from . import items, locations, regions, rules, web_world
from . import options as pixeldraw_options  # rename due to a name conflict with World.options

class PixelDrawWorld(World):
    """
    PixelDraw description goes here lol
    """

    game = "PixelDraw"

    web = web_world.PixelDrawWebWorld()

    options_dataclass = pixeldraw_options.PixelDrawOptions
    options: pixeldraw_options.PixelDrawOptions  # Common mistake: This has to be a colon (:), not an equals sign (=).

    location_name_to_id = locations.LOCATION_NAME_TO_ID
    item_name_to_id = items.ITEM_NAME_TO_ID

    origin_region_name = "Plane"

    def create_regions(self) -> None:
        regions.create_and_connect_regions(self)
        locations.create_all_locations(self)

    def set_rules(self) -> None:
        rules.set_all_rules(self)

    def create_items(self) -> None:
        items.create_all_items(self)

    def create_item(self, name: str) -> items.PixelDrawItem:
        return items.create_item_with_correct_classification(self, name)

    def get_filler_item_name(self) -> str:
        return items.get_random_filler_item_name(self)

    def fill_slot_data(self) -> Mapping[str, Any]:
        return self.options.as_dict(
            "trap_chance", "death_link", "randomize_enemy_deaths", "actions_needed"
        )
