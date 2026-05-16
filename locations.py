from __future__ import annotations

from typing import TYPE_CHECKING

from BaseClasses import ItemClassification, Location

from . import items

# from .rules import ItemLogic, get_chip_index

if TYPE_CHECKING:
    from .world import PixelDrawWorld


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

    "4_LOOP": 1022,
	"6_DIAG": 1023,
	"5_DIA": 1024,
	"7_PLUS": 1025,
	"4_TRI": 1026,
	"3/7_RECT": 1027,
	"9_SQC": 1028,
	"12_LINE": 1029,
	"7/11_SQC": 1030,
	"8/4_TRI": 1031,
	"7_X": 1032,
	"5_X": 1033,
	"6_SEMI": 1034,
	"9_QUAD": 1035,
	"11_OCTO": 1036,
	"8_ISOS": 1037,
	"13_AST": 1038,
	"12_RING": 1039,
	"6_TRAP": 1040,
	"20_HEX": 1041,
}

NORMAL_LOCATIONS = add_dicts([TOOL_LOCATIONS,SHAPE_LOCATIONS])

ENEMY_LOCATIONS = {
    "RED_PILL": 2000,
    "TRI_ENEMY": 2001,
    "ZOOM_ENEMY": 2002,
    "SMALL_BIRD": 2003,
}

CHIP_LOCATIONS = {
    "CHIP_PACK_1-1": 3000,

    "CHIP_PACK_2-1": 3001,
    "CHIP_PACK_2-2": 3002,

    "CHIP_PACK_3-1": 3003,
    "CHIP_PACK_3-2": 3004,
    "CHIP_PACK_3-3": 3005,

    "CHIP_PACK_4-1": 3006,
    "CHIP_PACK_4-2": 3007,
    "CHIP_PACK_4-3": 3008,
    "CHIP_PACK_4-4": 3009,

    "CHIP_PACK_5-1": 3010,
    "CHIP_PACK_5-2": 3011,
    "CHIP_PACK_5-3": 3012,
    "CHIP_PACK_5-4": 3013,
    "CHIP_PACK_5-5": 3014,
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

BLUEPRINT_LOCATIONS = {
    "BLUEPRINT_BOOK": 5000,

    "BLUEPRINT_DIAMOND": 5001,
    "BLUEPRINT_NETHERITE": 5002,
    "BLUEPRINT_FREE_CHIPS": 5003,
    "BLUEPRINT_TOOL_COLOR": 5004,
    "BLUEPRINT_WEAKEN_BOUNDS": 5005,
    "BLUEPRINT_CHIP_PACK_5": 5006,
}

LOCATION_NAME_TO_ID : dict[str, int | None] = add_dicts([NORMAL_LOCATIONS,ENEMY_LOCATIONS,CHIP_LOCATIONS,SHOP_LOCATIONS,BLUEPRINT_LOCATIONS])


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
    if world.options.randomize_blueprints:
        plane.add_locations(BLUEPRINT_LOCATIONS, PixelDrawLocation)


def create_events(world: PixelDrawWorld) -> None:
    return
