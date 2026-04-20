from __future__ import annotations

from typing import TYPE_CHECKING

from BaseClasses import Item, ItemClassification

from .locations import CHIP_LOCATIONS, NORMAL_LOCATIONS

if TYPE_CHECKING:
    from .world import PixelDrawWorld

# Every item must have a unique integer ID associated with it.
# We will have a lookup from item name to ID here that, in world.py, we will import and bind to the world class.
# Even if an item doesn't exist on specific options, it must be present in this lookup.
ITEM_NAME_TO_ID = {
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

    #"CREEPER": 2001,
    #"RESPAWN": 2002,
    #"RED_PILL": 2003,
    #"TOWER": 2004,
    #"W": 2005,
    #"L": 2006,
    #"ZIG": 2007,
    #"ZAG": 2008,
    #"COMPASS": 2009,
    #"SENDER": 2010,
    #"UNSENDER": 2011,
    #"GROUNDER": 2012,
    #"CUBE": 2013,
    #"TRI_ENEMY": 2014,
    #"TORCH": 2015,
    #"ZOOM_ENEMY": 2016,
    #"STONE": 2017,
    #"IRON": 2018,
    #"GOLD": 2019,
    #"DIAMOND": 2020,
    #"NETHERITE": 2021,
    #"SMALL_SPEED": 2022,
    #"NO": 2023,
    #"THUMB": 2024,
    #"DOT": 2025,
    #"L_HA": 2026,
    #"CHAIR": 2027,
    #"CROWN": 2028,
    #"6_PACK": 2029,
    #"SMALL_BIRD": 2030,
    #"SUMMON_BIRDS": 2031,
    #"DIA_TOWER": 2032,
    #"WALKING_PERSON": 2033,
    #"TEA": 2034,
    #"FLOAT": 2035,
    #"START": 2036,
    #"TUT_AREA_2": 2037,
    #"TUT_AREA_3": 2038,
    #"COLORED_NORMAL_COLOR": 2039,
    #"COLORED_C_GOL_COLOR": 2040,
    #"CAR": 2041,
    #"BOUNCE": 2042,
    #"UNDERSIDE": 2043,
    #"MULTIGRAVITY": 2044,
    #"SCALE_UP": 2045,
    #"SCALE_DOWN": 2046,
    #"MED_SPEED": 2047,

    "RANDOM_ACTION": 3000,
    "RANDOM_ENEMY": 3001,
    "COMPATIBILITY_CHIP": 3002,

    "MC_INVENTORY":4000,
}

# Items should have a defined default classification.
# In our case, we will make a dictionary from item name to classification.
DEFAULT_ITEM_CLASSIFICATIONS = {
    "C_GOL": ItemClassification.progression,
    "RAISER": ItemClassification.useful,
    "LEVELER": ItemClassification.useful,
    "DUSTER": ItemClassification.progression,
    "SHUFFLER": ItemClassification.progression,
    "STOPPER": ItemClassification.useful,
    "BULB": ItemClassification.useful,
    "MC_PICK": ItemClassification.progression,
    "HOOK": ItemClassification.useful,
    "BASE_SW": ItemClassification.progression,
    "PLACER": ItemClassification.progression,
    "STAMPER": ItemClassification.progression,
    "GRAVITATE": ItemClassification.useful,
    "SUMMON": ItemClassification.useful,
    "TERRAIN": ItemClassification.useful,
    "PARALYZER": ItemClassification.useful,
    "PLATFORM": ItemClassification.progression,
    "PLAGUE": ItemClassification.progression,
    "MAZER": ItemClassification.useful,

    "5_SQR": ItemClassification.progression,
    "6_SQR": ItemClassification.progression,
    "SM_DIA": ItemClassification.useful,
    "5_PLUS": ItemClassification.useful,
    "3_DIAG": ItemClassification.useful,
    "3_DIAG_IN": ItemClassification.useful,
    "7_LINE": ItemClassification.useful,
    "5_SQC": ItemClassification.useful,
    "10_SQR": ItemClassification.progression,
    "5_DIAG": ItemClassification.progression,
    "16_SQR": ItemClassification.progression,
    "5_TRI": ItemClassification.useful,
    "50_SQR": ItemClassification.progression,
    # "200_SQR": ItemClassification.progression,
    "7_LOOP": ItemClassification.useful,
    "7_SQC": ItemClassification.useful,
    "8_CIR": ItemClassification.useful,
    "10_TRI": ItemClassification.useful,
    "11_DIA": ItemClassification.useful,
    "6/4_RECT": ItemClassification.useful,

    "RANDOM_ACTION": ItemClassification.filler,
    "RANDOM_ENEMY": ItemClassification.trap,
    "COMPATIBILITY_CHIP": ItemClassification.useful,

    "MC_INVENTORY": ItemClassification.useful,
}


class PixelDrawItem(Item):
    game = "PixelDraw"


def get_random_filler_item_name(world: PixelDrawWorld) -> str:
    if world.random.randint(0, 99) < world.options.trap_chance:
        return "RANDOM_ENEMY"
    return "RANDOM_ACTION"


def create_item_with_correct_classification(world: PixelDrawWorld, name: str) -> PixelDrawItem:
    return PixelDrawItem(name, DEFAULT_ITEM_CLASSIFICATIONS[name], ITEM_NAME_TO_ID[name], world.player)


def create_all_items(world: PixelDrawWorld) -> None:
    baseitempool = list(NORMAL_LOCATIONS.keys())
    otheritems = []

    if world.options.randomize_compatibility_chips:
        for i in range(len(CHIP_LOCATIONS)):
            otheritems.append("COMPATIBILITY_CHIP")
    if world.options.randomize_salesmen:
        for i in range(7):
            otheritems.append("MC_INVENTORY")

    itempool: list[Item] = []
    for item in baseitempool + otheritems:
        itempool.append(world.create_item(item))

    number_of_items = len(itempool)

    number_of_unfilled_locations = len(world.multiworld.get_unfilled_locations(world.player))

    needed_number_of_filler_items = number_of_unfilled_locations - number_of_items

    if world.options.randomize_compatibility_chips and world.options.additional_compatibility_chips > 0 and needed_number_of_filler_items > 0:
        for _ in range(world.options.additional_compatibility_chips):
            needed_number_of_filler_items -= 1
            itempool.append(world.create_item("COMPATIBILITY_CHIP"))
            if needed_number_of_filler_items <= 0:
                break

    itempool += [world.create_filler() for _ in range(needed_number_of_filler_items)]

    world.multiworld.itempool += itempool