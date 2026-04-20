from __future__ import annotations

from typing import TYPE_CHECKING

from BaseClasses import ItemClassification, Location

from . import items

if TYPE_CHECKING:
    from .world import PixelDrawWorld

# Every location must have a unique integer ID associated with it.
# We will have a lookup from location name to ID here that, in world.py, we will import and bind to the world class.
# Even if a location doesn't exist on specific options, it must be present in this lookup.
def add_dicts(dictionaries:list[dict]) -> dict:
    result = {}
    for dictionary in dictionaries:
        for i in dictionary:
            result[i] = dictionary[i]
    return result


TOOL_LOCATIONS = {
    "C_GOL": 3,
    "RAISER": 4,
    "LEVELER": 5,
    "DUSTER": 6,
    "SHUFFLER": 7,
    "STOPPER": 8,
    "BULB": 9,
    "MC_PICK": 10,
    "HOOK": 11,
    "BASE_SW": 12,
    "PLACER": 13,
    "STAMPER": 14,
    "GRAVITATE": 15,
    "SUMMON": 16,
    "TERRAIN": 17,
    "PARALYZER": 18,
    "PLATFORM": 19,
    "PLAGUE": 20,
    "MAZER": 21,
}

SHAPE_LOCATIONS = {
    "5_SQR": 1002,
    "6_SQR": 1003,
    "SM_DIA": 1004,
    "5_PLUS": 1005,
    "3_DIAG": 1006,
    "3_DIAG_IN": 1007,
    "7_LINE": 1008,
    "5_SQC": 1009,
    "10_SQR": 1010,
    "5_DIAG": 1011,
    "16_SQR": 1012,
    "5_TRI": 1013,
    "50_SQR": 1014,
    # "200_SQR": 1015,
    "7_LOOP": 1016,
    "7_SQC": 1017,
    "8_CIR": 1018,
    "10_TRI": 1019,
    "11_DIA": 1020,
    "6/4_RECT": 1021,
}

NORMAL_LOCATIONS = add_dicts([TOOL_LOCATIONS,SHAPE_LOCATIONS])

ENEMY_LOCATIONS = {
    "RED_PILL": 2000,
    "TRI_ENEMY": 2001,
    "ZOOM_ENEMY": 2002,
    "SMALL_BIRD": 2003,
}

CHIP_LOCATIONS = {
    "CHIP_PACK_1": 3000,
    "CHIP_PACK_2-1": 3001,
    "CHIP_PACK_2-2": 3002,
}

SHOP_LOCATIONS = {
	"CUBIC_SALESMAN_ITEM_1":4000,
	"CUBIC_SALESMAN_ITEM_2":4001,
	"CUBIC_SALESMAN_ITEM_3":4002,
	"MINECRAFT_USER_ITEM_1":4003,
	"MINECRAFT_USER_ITEM_2":4004,
	"MINECRAFT_USER_ITEM_3-1":4005,
	"MINECRAFT_USER_ITEM_3-2":4006,
	"MINECRAFT_USER_ITEM_3-3":4007,
	"MINECRAFT_USER_ITEM_3-4":4008,
	"MINECRAFT_USER_ITEM_3-5":4009,
	"MINECRAFT_USER_ITEM_3-6":4010,
	"MINECRAFT_USER_ITEM_3-7":4011,
}

LOCATION_NAME_TO_ID : dict[str, int | None] = add_dicts([NORMAL_LOCATIONS,ENEMY_LOCATIONS,CHIP_LOCATIONS,SHOP_LOCATIONS])


class PixelDrawLocation(Location):
    game = "PixelDraw"


def get_location_names_with_ids(location_names: list[str]) -> dict[str, int | None]:
    return {location_name: LOCATION_NAME_TO_ID[location_name] for location_name in location_names}


def create_all_locations(world: PixelDrawWorld) -> None:
    create_regular_locations(world)
    create_events(world)


def create_regular_locations(world: PixelDrawWorld) -> None:
    plane = world.get_region("Plane")
    plane.add_locations(NORMAL_LOCATIONS, PixelDrawLocation)

    if world.options.randomize_enemy_deaths:
        plane.add_locations(ENEMY_LOCATIONS, PixelDrawLocation)
    if world.options.randomize_compatibility_chips:
        plane.add_locations(CHIP_LOCATIONS, PixelDrawLocation)
    if world.options.randomize_salesmen:
        plane.add_locations(SHOP_LOCATIONS, PixelDrawLocation)


def create_events(world: PixelDrawWorld) -> None:
    return
