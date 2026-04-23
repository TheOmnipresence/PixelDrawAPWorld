from __future__ import annotations

import typing
from collections.abc import Callable
from typing import TYPE_CHECKING

from BaseClasses import CollectionState
from worlds.generic.Rules import add_rule, set_rule

if TYPE_CHECKING:
    from .world import PixelDrawWorld

from .locations import CHIP_LOCATIONS, SHOP_LOCATIONS

toolsCompatibility = {
	"NONE":[],
	"VOIDER":[],
	"ERASER":[],
	"C_GOL":[		"NONE",		"BASE_RECT",	"5_SQR",	"6_SQR"																																																					],
	"RAISER":[		"NONE",												"SM_DIA",	"5_PLUS",													"5_SQC"																																],
	"LEVELER":[		"NONE",		"BASE_RECT",	"5_SQR",																															"5_TRI",																			"6/4_RECT",	],
	"DUSTER":[		"NONE",		"BASE_RECT",				"6_SQR",																																								"8_CIR",										],
	"SHUFFLER":[	"NONE",						"5_SQR"																																																								],
	"STOPPER":[		"NONE",												"SM_DIA",												"7_LINE"																																			],
	"BULB":[		"NONE",															"5_PLUS",		"3_DIAG",	"3_DIAG_IN",																																"11_DIA",				],
	"MC_PICK":[		"NONE",																										"7_LINE"																																			],
	"HOOK":[		"NONE",									"6_SQR",																			"5_SQC",																						"10_TRI",							],
	"BASE_SW":[		"NONE",																			"3_DIAG",	"3_DIAG_IN",											"5_DIAG"																									],
	"PLACER":[		"NONE",																			"3_DIAG",	"3_DIAG_IN",																																						],
	"STAMPER":[		"NONE",									"6_SQR",																																																				],
	"GRAVITATE":[	"NONE",																																							"5_TRI",													"10_TRI",							],
	"SUMMON":[		"NONE",						"5_SQR",																									"10_SQR",																						"11_DIA",				],
	"TERRAIN":[		"NONE",						"5_SQR",																																		"50_SQR",	"200_SQR",																],
	"PARALYZER":[	"NONE",																																																"7_SQC",							"11_DIA",	"6/4_RECT",	],
	"PLATFORM":[	"NONE",																																										"50_SQR",				"7_SQC",	"8_CIR",										],
	"PLAGUE":[		"NONE",																																	"10_SQR",																			"10_TRI",							],
	"MAZER":[		"NONE",									"6_SQR",																						"10_SQR",							"50_SQR",																			],
}

additionalCompatibilities = {
	"NONE":[],
	"VOIDER":[],
	"ERASER":[],
	"C_GOL":["10_SQR","50_SQR"],
	"RAISER":["11_DIA"],
	"LEVELER":["11_DIA"],
	"DUSTER":["7_SQC"],
	"SHUFFLER":["7_LINE"],
	"STOPPER":["3_DIAG"],
	"BULB":["SM_DIA"],
	"MC_PICK":["6_SQR"],
	"HOOK":["7_SQC"],
	"BASE_SW":["7_LOOP"],
	"PLACER":["BASE_RECT"],
	"STAMPER":["6/4_RECT"],
	"GRAVITATE":["8_CIR"],
	"SUMMON":["10_TRI"],
	"TERRAIN":["10_SQR"],
	"PARALYZER":["5_PLUS"],
	"PLATFORM":["BASE_RECT"],
	"PLAGUE":["6/4_RECT"],
	"MAZER":["5_SQR"],
}


def set_all_rules(world: PixelDrawWorld) -> None:
    set_all_entrance_rules(world)
    set_all_location_rules(world)
    set_completion_condition(world)


def set_all_entrance_rules(world: PixelDrawWorld) -> None:
    return


def can_use_tool(world: PixelDrawWorld,tool:str) -> typing.Callable:
    result:list[str] = []
    for toolshape in toolsCompatibility[tool]:
        match toolshape:
            case "NONE":
                pass
            case "BASE_RECT":
                return lambda state: state.has(tool, world.player)
            case _:
                if toolshape != "200_SQR" and toolshape != "50_SQR": result.append(toolshape)

    if not result:
        return lambda state: False
    else:
        return lambda state: (
                (state.has_any(result, world.player) or get_additional_compatibilities_logic(tool, state, world))
                and state.has(tool, world.player))


def get_additional_compatibilities_logic(tool:str, state, world: PixelDrawWorld) -> bool:
    for shapeIndex in range(len(additionalCompatibilities[tool])):
        match additionalCompatibilities[tool][shapeIndex]:
            case "NONE":
                pass
            case "BASE_RECT":
                if state.has("COMPATIBILITY_CHIP", world.player, shapeIndex) if world.options.randomize_compatibility_chips else can_get_chips(shapeIndex, world):
                    return True
            case _:
                if state.has(additionalCompatibilities[tool][shapeIndex], world.player):
                    if state.has("COMPATIBILITY_CHIP", world.player, shapeIndex) if world.options.randomize_compatibility_chips else can_get_chips(shapeIndex, world):
                        return True
    return False


def can_get_chips(amount:int, world: PixelDrawWorld) -> bool:
    result = 0
    for i in range(get_chip_index(list(CHIP_LOCATIONS.keys())[-1])):
        if get_chip_pack_logic(i + 1, world):
            result += get_chip_amount(i + 1)
            if result >= amount: return True

    return False


def set_chip_pack_rule(index: int, world: PixelDrawWorld) -> None:
    relevant_chips = []
    for i in CHIP_LOCATIONS:
        if get_chip_index(i) == index:
            relevant_chips.append(i)

    for i in relevant_chips:
        set_rule(world.get_location(i), get_chip_pack_logic(index, world))


def get_chip_pack_logic(index:int, world: PixelDrawWorld) -> typing.Callable:
    item_logic = ItemLogic(world)

    logic: Callable

    match index: ## Individual pack logic goes here
        case 1:
            logic = item_logic.get_pattern_logic(4,["5_TRI"])
            # logic = lambda state: ((four_size(state) or state.has("5_TRI", world.player)) and manipulators(state))
        case 2:
            logic = item_logic.get_pattern_logic(4)
            # logic = lambda state: (four_size(state) and manipulators(state))
        case _:
            logic = lambda state: True

    return logic


def get_chip_amount(index:int) -> int:
    relevant_chips = []
    for i in CHIP_LOCATIONS:
        if get_chip_index(i) == index:
            relevant_chips.append(i)

    return len(relevant_chips)


def get_chip_index(chip_name:str) -> int:
    chip_name = chip_name.removeprefix("CHIP_PACK_")

    return int(chip_name.split("-")[0])


def set_all_location_rules(world: PixelDrawWorld) -> None:
    # shuffler or (mc_pick and placer) or (stamper and c_gol and duster) or platform
    #manipulators = (lambda state: can_use_tool(world,"SHUFFLER") or can_use_tool(world,"PLATFORM") or (can_use_tool(world,"MC_PICK") and can_use_tool(world,"PLACER")) or (can_use_tool(world,"STAMPER") and can_use_tool(world,"C_GOL")))
    # manipulators = (lambda state:
    #     can_use_tool(world, "SHUFFLER")(state) or
    #     can_use_tool(world, "PLATFORM")(state) or
    #     (can_use_tool(world, "MC_PICK")(state) and can_use_tool(world, "PLACER")(state)) or
    #     (can_use_tool(world, "STAMPER")(state) and ((can_use_tool(world, "C_GOL")(state) and can_use_tool(world,"DUSTER")(state)) or can_use_tool(world, "PLAGUE")(state) or can_use_tool(world, "MC_PICK")(state)))
    # )

    # fifty_size = (lambda state: state.has_any(["50_SQR"], world.player))
    # eight_size = (lambda state: state.has_any(["10_SQR","16_SQR"], world.player))
    # seven_size = (lambda state: state.has_any([], world.player) or eight_size(state))
    # six_size = (lambda state: state.has_any(["6_SQR"], world.player) or seven_size(state))
    # five_size = (lambda state: state.has_any(["5_SQR","7_SQC","10_TRI","11_DIA"], world.player) or six_size(state))
    # four_size = (lambda state: state.has_any(["6/4_RECT"], world.player) or five_size(state))

    item_logic = ItemLogic(world)
    item_logic.set_pattern_logic("6_SQR",4)
    item_logic.set_pattern_logic("SM_DIA",5,["5_SQC"])
    item_logic.set_pattern_logic("5_PLUS",5,["5_PLUS","5_SQC"])
    item_logic.set_pattern_logic("BULB",5,["5_SQC"])
    item_logic.set_pattern_logic("MC_PICK",4,["5_SQC"])
    item_logic.set_pattern_logic("7_LINE",5,["5_PLUS","7_LINE","5_SQC","5_TRI","7_LOOP","6/4_RECT"])
    item_logic.set_pattern_logic("5_SQC",4,["5_SQC","5_TRI"])
    item_logic.set_pattern_logic("10_SQR",6)
    item_logic.set_pattern_logic("16_SQR",8)
    item_logic.set_pattern_logic("STAMPER",8)
    item_logic.set_pattern_logic("GRAVITATE",4,["5_SQC"])
    item_logic.set_pattern_logic("50_SQR",5)
    item_logic.set_pattern_logic("7_LOOP",5)
    item_logic.set_pattern_logic("PLATFORM",5)
    item_logic.set_pattern_logic("8_CIR",4,["5_SQC","5_TRI"])
    item_logic.set_pattern_logic("10_TRI",5,["5_TRI","5_SQC","6/4_RECT"])
    item_logic.set_pattern_logic("11_DIA",5)
    item_logic.set_pattern_logic("PLAGUE",5,["5_SQC"])
    item_logic.set_pattern_logic("MAZER",13)
    item_logic.set_pattern_logic("6/4_RECT",4,["5_SQC","5_TRI"])

    if world.options.randomize_salesmen:
        for i in SHOP_LOCATIONS:
            item_logic.set_shop_logic(i)

    # set_rule(world.get_location("6_SQR"),lambda state: four_size(state) and manipulators(state))
    # set_rule(world.get_location("SM_DIA"),lambda state: (five_size(state) or state.has_any(["5_SQC"], world.player)) and manipulators(state))
    # set_rule(world.get_location("5_PLUS"), lambda state: (five_size(state) or state.has_any(["5_PLUS","5_SQC"], world.player)) and manipulators(state))
    # set_rule(world.get_location("BULB"), lambda state: (five_size(state) or state.has("5_SQC", world.player)) and manipulators(state))
    # set_rule(world.get_location("MC_PICK"), lambda state: four_size(state) and manipulators(state))
    # set_rule(world.get_location("7_LINE"), lambda state: (five_size(state) or state.has_any(["5_PLUS","7_LINE","5_SQC","5_TRI","7_LOOP"], world.player)) and manipulators(state))
    # set_rule(world.get_location("5_SQC"), lambda state: (four_size(state) or state.has_any(["5_SQC"], world.player)) and manipulators(state))
    # set_rule(world.get_location("10_SQR"), lambda state: six_size(state) and manipulators(state))
    # set_rule(world.get_location("16_SQR"), lambda state: eight_size(state) and manipulators(state))
    # set_rule(world.get_location("STAMPER"), lambda state: eight_size(state) and manipulators(state))
    # set_rule(world.get_location("GRAVITATE"), lambda state: (four_size(state) or state.has_any(["5_SQC"], world.player)) and manipulators(state))
    # set_rule(world.get_location("50_SQR"), lambda state: five_size(state) and manipulators(state))
    # set_rule(world.get_location("7_LOOP"), lambda state: five_size(state) and manipulators(state))
    # set_rule(world.get_location("PLATFORM"), lambda state: five_size(state) and manipulators(state))
    # set_rule(world.get_location("200_SQR"), lambda state: fifty_size(state) and manipulators(state))
    # set_rule(world.get_location("8_CIR"), lambda state: four_size(state) and manipulators(state))
    # set_rule(world.get_location("10_TRI"), lambda state: (five_size(state) or state.has("5_TRI",world.player)) and manipulators(state))
    # set_rule(world.get_location("11_DIA"), lambda state: five_size(state) and manipulators(state))
    # set_rule(world.get_location("PLAGUE"), lambda state: (five_size(state) or state.has_any(["5_SQC"], world.player)) and manipulators(state))
    # set_rule(world.get_location("MAZER"), lambda state: state.has("16_SQR",world.player) and manipulators(state))
    # set_rule(world.get_location("6/4_RECT"), lambda state: four_size(state) and manipulators(state))

    if world.options.randomize_enemy_deaths:
        set_rule(world.get_location("RED_PILL"), lambda state: state.has_any(item_logic.get_size(4) + ["5_SQC","5_TRI"], world.player) and item_logic.manipulators(state) and can_use_tool(world, "BASE_SW")(state))
        set_rule(world.get_location("TRI_ENEMY"), lambda state: can_use_tool(world, "BASE_SW")(state))
        set_rule(world.get_location("ZOOM_ENEMY"), lambda state: can_use_tool(world, "BASE_SW")(state))
        set_rule(world.get_location("SMALL_BIRD"), lambda state: can_use_tool(world, "BASE_SW")(state))
    if world.options.randomize_compatibility_chips:
        for i in range(get_chip_index(list(CHIP_LOCATIONS.keys())[-1])):
            set_chip_pack_rule(i + 1, world)


def set_completion_condition(world: PixelDrawWorld) -> None:
    item_logic = ItemLogic(world)

    world.multiworld.completion_condition[world.player] = lambda state: state.has_all(["5_SQR","16_SQR","50_SQR"], world.player) and item_logic.manipulators(state)


class ItemLogic:
    world : PixelDrawWorld
    sizes : list[list] = [
        [],
        ["SM_DIA", "5_PLUS", "3_DIAG", "3_DIAG_IN", "7_LINE", "5_DIAG", "7_LOOP"],
        [],
        ["5_SQC", "5_TRI"],
        ["6/4_RECT"],
        ["5_SQR", "7_SQC", "10_TRI", "11_DIA", "8_CIR"],
        ["6_SQR"],
        [],
        [],
        [],
        ["10_SQR"],
        [],
        [],
        [],
        [],
        [],
        ["16_SQR"],
    ]
    manipulators : Callable

    def __init__(self, world: PixelDrawWorld) -> None:
        self.world = world

        self.manipulators = (lambda state:
            can_use_tool(world, "SHUFFLER")(state) or
            can_use_tool(world, "PLATFORM")(state) or
            (can_use_tool(world, "MC_PICK")(state) and can_use_tool(world, "PLACER")(state)) or
            (can_use_tool(world, "STAMPER")(state) and
                ((  can_use_tool(world, "C_GOL")(state) and can_use_tool(world, "DUSTER")(state)  ) or
                can_use_tool(world, "PLAGUE")(state) or can_use_tool(world, "MC_PICK")(state)  ))
            )


    def set_pattern_logic(self, name: str, size: int, other_shapes: list = None) -> None:
        if other_shapes is None:
            other_shapes = []
        set_rule(self.world.get_location(name), self.get_pattern_logic(size, other_shapes))


    def get_pattern_logic(self, size: int, other_shapes: list = None, other_logic: Callable = None) -> Callable:
        if other_shapes is None:
            other_shapes = []
        if other_logic is None:
            other_logic = lambda state: True
        return lambda state: self.manipulators(state) and state.has_any(self.get_size(size) + other_shapes, self.world.player) and other_logic(state)


    def get_size(self, size: int) -> list:
        result = []
        for i in range(len(self.sizes) - size):
            result += self.sizes[-i - 1]
        return result


    def set_shop_logic(self, item:str) -> None:
        has_sword = lambda state: can_use_tool(self.world, "BASE_SW")(state)
        logic = lambda state: True
        match item.split("_ITEM_")[0]:
            case "CUBIC_SALESMAN":
                logic = self.get_pattern_logic(5, [], has_sword)
            case "MINECRAFT_USER":
                logic = self.get_pattern_logic(13, [], has_sword)
        set_rule(self.world.get_location(item), logic)