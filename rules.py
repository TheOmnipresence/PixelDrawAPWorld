from __future__ import annotations

import math
import typing
from collections.abc import Callable
from typing import TYPE_CHECKING

from BaseClasses import CollectionState
from worlds.generic.Rules import add_rule, set_rule

if TYPE_CHECKING:
    from .world import PixelDrawWorld

from .locations import CHIP_LOCATIONS, SHOP_LOCATIONS, BLUEPRINT_LOCATIONS, TOOL_LOCATIONS, SHAPE_LOCATIONS

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
	"SHUFFLER":["7_LINE","5_DIAG"],
	"STOPPER":["3_DIAG"],
	"BULB":["SM_DIA"],
	"MC_PICK":["6_SQR","3_DIAG"],
	"HOOK":["7_SQC","10_SQR"],
	"BASE_SW":["7_LOOP","5_PLUS"],
	"PLACER":["BASE_RECT"],
	"STAMPER":["6/4_RECT"],
	"GRAVITATE":["8_CIR"],
	"SUMMON":["10_TRI"],
	"TERRAIN":["10_SQR"],
	"PARALYZER":["5_PLUS"],
	"PLATFORM":["BASE_RECT","SM_DIA"],
	"PLAGUE":["6/4_RECT","BASE_RECT"],
	"MAZER":["5_SQR"],
}


def set_all_rules(world: PixelDrawWorld) -> None:
    set_all_entrance_rules(world)
    set_all_location_rules(world)
    set_completion_condition(world)


def set_all_entrance_rules(world: PixelDrawWorld) -> None:
    return


def can_use_tool(world: PixelDrawWorld, tool: str, disregard_chips: bool = False) -> typing.Callable:
    result: list[str] = []
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
    elif not disregard_chips:
        return lambda state: (
                (state.has_any(result, world.player) or get_additional_compatibilities_logic(tool, state, world))
                and state.has(tool, world.player))
    else:
        return lambda state: state.has_any(result, world.player) and state.has(tool, world.player)


def get_additional_compatibilities_logic(tool: str, state, world: PixelDrawWorld) -> bool:
    for shapeIndex in range(len(additionalCompatibilities[tool])):
        match additionalCompatibilities[tool][shapeIndex]:
            case "NONE":
                pass
            case "BASE_RECT":
                if state.has("COMPATIBILITY_CHIP", world.player, shapeIndex) if world.options.randomize_compatibility_chips else can_get_chips(shapeIndex, world, state):
                    return True
            case _:
                if state.has(additionalCompatibilities[tool][shapeIndex], world.player):
                    if state.has("COMPATIBILITY_CHIP", world.player, shapeIndex) if world.options.randomize_compatibility_chips else can_get_chips(shapeIndex, world, state):
                        return True
    return False


def can_get_chips(amount:int, world: PixelDrawWorld, state) -> bool:
    result = 0
    for i in range(get_chip_index(list(CHIP_LOCATIONS.keys())[-1])):
        if get_chip_pack_logic(i + 1, world)(state):
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


def get_chip_pack_logic(index:int, world: PixelDrawWorld) -> Callable:
    item_logic = None
    if world.options.randomize_compatibility_chips:
        item_logic = ItemLogic(world)
    else:
        item_logic = ItemLogic(world, True)

    logic: Callable

    match index: # Individual pack logic goes here
        case 1:
            logic = item_logic.get_pattern_logic(4,["5_TRI"])
        case 2:
            logic = item_logic.get_pattern_logic(4)
        case 3:
            logic = item_logic.get_pattern_logic(6,["8_ISOS"])
        case 4:
            logic = item_logic.get_pattern_logic(8, ["8_CIR", "10_TRI", "11_DIA", "9_SQC", "7/11_SQC", "11_OCTO", "13_AST", "6_TRAP"])
        case 5:
            logic = lambda state: item_logic.get_pattern_logic(8,["11_DIA", "9_SQC", "7/11_SQC", "11_OCTO", "13_AST", "6_TRAP"])(state) and item_logic.has_blueprint("CHIP_PACK_5",state)
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


def get_hex_pattern_size(hex_str: str) -> int:
    return round(math.sqrt((len(hex_str) - 2) * 4))


def can_get_all_hex_patterns(item_logic:ItemLogic, patterns: set[str], state:CollectionState) -> bool:
    max_size = get_hex_pattern_size(list(patterns)[0])
    for i in patterns:
        size = get_hex_pattern_size(i)
        if size > max_size:
            max_size = size
    return item_logic.get_pattern_logic(max_size)(state)


def set_all_location_rules(world: PixelDrawWorld) -> None:
    item_logic = ItemLogic(world)

    item_logic.set_pattern_logic("6_SQR", 4)
    item_logic.set_pattern_logic("SM_DIA", 5, ["5_SQC", "5_DIA", "8_ISOS"])
    item_logic.set_pattern_logic("5_PLUS", 5, ["5_PLUS", "5_SQC", "5_DIA", "7_PLUS", "8_ISOS"])
    item_logic.set_pattern_logic("BULB", 5, ["5_SQC", "7_X", "8_ISOS"])
    item_logic.set_pattern_logic("MC_PICK", 4, ["5_SQC", "7_X", "9_QUAD"])
    item_logic.set_pattern_logic("7_LINE", 5, ["5_PLUS", "7_LINE", "5_SQC", "5_TRI", "7_LOOP", "6/4_RECT", "5_DIA", "7_PLUS", "3/7_RECT", "12_LINE", "8/4_TRI", "7_X", "6_SEMI", "9_QUAD", "8_ISOS", "12_RING"])
    item_logic.set_pattern_logic("5_SQC", 4, ["5_SQC", "4_LOOP", "9_QUAD"])
    item_logic.set_pattern_logic("10_SQR", 6)
    item_logic.set_pattern_logic("16_SQR", 8)
    item_logic.set_pattern_logic("STAMPER", 8, ["9_SQC", "7/11_SQC", "11_OCTO", "13_AST", "6_TRAP"])
    item_logic.set_pattern_logic("GRAVITATE", 4, ["5_SQC", "5_TRI", "5_DIA", "3/7_RECT", "12_LINE", "8/4_TRI", "9_QUAD"])
    item_logic.set_pattern_logic("50_SQR", 5)
    item_logic.set_pattern_logic("7_LOOP", 5)
    item_logic.set_pattern_logic("PLATFORM", 5, ["8_ISOS"])
    item_logic.set_pattern_logic("8_CIR", 4, ["5_SQC", "5_TRI", "7_X", "6_SEMI", "9_QUAD"])
    item_logic.set_pattern_logic("10_TRI", 5, ["5_SQC", "5_TRI", "6/4_RECT", "5_DIA", "3/7_RECT", "12_LINE", "8/4_TRI", "7_X", "6_SEMI", "9_QUAD", "8_ISOS"])
    item_logic.set_pattern_logic("11_DIA", 5)
    item_logic.set_pattern_logic("PLAGUE", 5, ["5_SQC", "5_DIA", "8_ISOS"])
    item_logic.set_pattern_logic("MAZER", 13)
    item_logic.set_pattern_logic("6/4_RECT", 4, ["5_SQC", "5_TRI", "3/7_RECT", "12_LINE", "8/4_TRI", "6_SEMI", "9_QUAD"])
    item_logic.set_pattern_logic("4_LOOP", 4, ["4_LOOP"])
    item_logic.set_pattern_logic("6_DIAG", 4, ["5_SQC", "5_TRI", "6_DIAG", "7_X", "9_QUAD", "12_RING"])
    item_logic.set_pattern_logic("5_DIA", 5, ["5_SQC", "5_DIA", "8_ISOS"])
    item_logic.set_pattern_logic("7_PLUS", 4, ["5_PLUS", "5_SQC", "5_TRI", "5_DIA", "7_PLUS", "7_X", "9_QUAD"])
    item_logic.set_pattern_logic("4_TRI", 4, ["5_SQC", "5_TRI", "4_TRI", "7_X", "6_SEMI", "9_QUAD"])
    item_logic.set_pattern_logic("3/7_RECT", 4, ["5_SQC", "3/7_RECT", "12_LINE", "8/4_TRI", "9_QUAD"])
    item_logic.set_pattern_logic("9_SQC", 4, ["5_SQC", "9_QUAD"])
    item_logic.set_pattern_logic("12_LINE", 4, ["5_PLUS", "7_LINE", "5_SQC", "5_TRI", "7_LOOP", "4_LOOP", "5_DIA", "7_PLUS", "4_TRI", "3/7_RECT", "12_LINE", "8/4_TRI", "7_X", "6_SEMI", "9_QUAD", "12_RING"])
    item_logic.set_pattern_logic("7/11_SQC", 5, ["5_SQC", "6/4_RECT", "5_DIA", "3/7_RECT", "12_LINE", "8/4_TRI", "8_ISOS"])
    item_logic.set_pattern_logic("8/4_TRI", 4, ["5_SQC", "5_TRI", "5_DIA", "4_TRI", "3/7_RECT", "12_LINE", "8/4_TRI", "7_X", "6_SEMI", "9_QUAD", "12_RING"])
    item_logic.set_pattern_logic("7_X", 5, ["7_X"])
    item_logic.set_pattern_logic("5_X", 5, ["7_X", "5_X"])
    item_logic.set_pattern_logic("6_SEMI", 4, ["5_SQC", "5_TRI", "5_DIA", "4_TRI", "3/7_RECT", "12_LINE", "8/4_TRI", "7_X", "6_SEMI", "9_QUAD", "12_RING"])
    item_logic.set_pattern_logic("9_QUAD", 4, ["5_SQC", "5_TRI", "5_DIA", "9_QUAD"])
    item_logic.set_pattern_logic("11_OCTO", 4, ["5_SQC", "7_X", "9_QUAD"])
    item_logic.set_pattern_logic("8_ISOS", 4, ["5_SQC", "9_QUAD"])
    item_logic.set_pattern_logic("13_AST", 4, ["7_X"])
    item_logic.set_pattern_logic("12_RING", 5, ["5_SQC", "8_ISOS"])
    item_logic.set_pattern_logic("6_TRAP", 12, ["6_TRAP"])
    item_logic.set_pattern_logic("20_HEX", 5, ["5_SQC", "6/4_RECT", "5_DIA", "3/7_RECT", "12_LINE", "8/4_TRI", "7_X", "6_SEMI", "8_ISOS", "12_RING"])


    if world.options.randomize_salesmen:
        for i in SHOP_LOCATIONS:
            item_logic.set_shop_logic(i)

    if world.options.randomize_enemy_deaths:
        set_rule(world.get_location("RED_PILL"), lambda state: state.has_any(item_logic.get_size(4) + ["5_SQC","5_TRI"], world.player) and item_logic.manipulators(state) and can_use_tool(world, "BASE_SW")(state))
        set_rule(world.get_location("TRI_ENEMY"), lambda state: can_use_tool(world, "BASE_SW")(state))
        set_rule(world.get_location("ZOOM_ENEMY"), lambda state: can_use_tool(world, "BASE_SW")(state))
        set_rule(world.get_location("SMALL_BIRD"), lambda state: can_use_tool(world, "BASE_SW")(state))

    if world.options.randomize_compatibility_chips:
        for i in range(get_chip_index(list(CHIP_LOCATIONS.keys())[-1])):
            set_chip_pack_rule(i + 1, world)

    if world.options.randomize_blueprints:
        for i in BLUEPRINT_LOCATIONS.keys():
            item_logic.set_blueprint_logic(i.removeprefix("BLUEPRINT_"))


def set_completion_condition(world: PixelDrawWorld) -> None:
    item_logic = ItemLogic(world)

    needed_actions_logic = lambda state: True
    completion_shape_logic = lambda state: True
    needed_patterns_logic = lambda state: True

    blueprints: list = list(BLUEPRINT_LOCATIONS.keys())
    if "BLUEPRINT_BOOK" in blueprints:
        blueprints.remove("BLUEPRINT_BOOK")
    without_blueprint_actions = world.options.actions_needed.range_end - len(blueprints)

    if world.options.actions_needed <= 37:
        pass
    elif world.options.actions_needed <= without_blueprint_actions:
        needed_actions_logic = lambda state: state.has_all(["5_SQR", "10_SQR", "16_SQR"], world.player) and item_logic.manipulators(state)
    else:
        needed_actions_logic = lambda state: state.has_all(["5_SQR","10_SQR","16_SQR"], world.player) and item_logic.manipulators(state) and state.has_from_list_unique(blueprints, world.player, world.options.actions_needed - without_blueprint_actions)

    if world.options.completion_shape.value != "":
        completion_shape_logic = item_logic.get_pattern_logic(get_hex_pattern_size(world.options.completion_shape.value))

    if world.options.needed_patterns.value:
        needed_patterns_logic = lambda state: can_get_all_hex_patterns(item_logic, world.options.needed_patterns.value, state)

    world.multiworld.completion_condition[world.player] = lambda state: needed_actions_logic(state) and completion_shape_logic(state) and needed_patterns_logic(state)


def get_manipulators(world: PixelDrawWorld, disregard_chips: bool = False) -> Callable:
    tools_logic = {}
    for tool in ["SHUFFLER", "PLATFORM", "MC_PICK", "PLACER", "STAMPER", "C_GOL", "DUSTER", "PLAGUE"]:
        tools_logic[tool] = can_use_tool(world, tool, disregard_chips)

    return lambda state:(
        tools_logic["SHUFFLER"](state) or tools_logic["PLATFORM"](state) or
        (tools_logic["MC_PICK"](state) and tools_logic["PLACER"](state)) or
        (tools_logic["STAMPER"](state) and (
            (tools_logic["C_GOL"](state) and tools_logic["DUSTER"](state)) or
            tools_logic["MC_PICK"](state) or
            tools_logic["PLAGUE"](state)
        ))
    )


class ItemLogic:
    world: PixelDrawWorld

    sizes: list[list] = [
        [],
        ["SM_DIA", "5_PLUS", "3_DIAG", "3_DIAG_IN", "7_LINE", "5_DIAG", "7_LOOP", "4_LOOP", "7_PLUS", "5_X"],
        ["6_DIAG", "4_TRI", "6_SEMI", "12_RING"],
        ["5_SQC", "5_TRI", "5_DIA", "3/7_RECT", "12_LINE", "8/4_TRI", "7_X", "9_QUAD"], # BASE_RECT is here, so any shapes here or before don't matter
        ["6/4_RECT", "8_ISOS"],
        ["5_SQR", "7_SQC", "10_TRI", "11_DIA", "8_CIR"],
        ["6_SQR", "7/11_SQC", "6_TRAP"],
        ["9_SQC", "11_OCTO", "13_AST"],
        [],
        [],
        ["10_SQR"],
        [],
        [],
        ["20_HEX"],
        [],
        [],
        ["16_SQR"],
    ]

    manipulators: Callable

    blueprint_tree: dict[str, list] = {
        "DIAMOND":[],
        "NETHERITE":["DIAMOND"],
        "FREE_CHIPS":[],
        "TOOL_COLOR":["FREE_CHIPS"],
        "WEAKEN_BOUNDS":["TOOL_COLOR"],
        "CHIP_PACK_5":["TOOL_COLOR"],
    }


    def __init__(self, world: PixelDrawWorld, disregard_chips: bool = False) -> None:
        self.world = world

        self.manipulators = get_manipulators(world, disregard_chips)


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
        if size > 16:
            return ["50_SQR"]
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
                logic = self.get_pattern_logic(13, [], lambda state: has_sword(state) and self.has_blueprint("DIAMOND",state))
        set_rule(self.world.get_location(item), logic)


    def has_blueprint(self, blueprint:str, state) -> bool:
        if self.world.options.randomize_blueprints:
            return state.has("BLUEPRINT_" + blueprint, self.world.player)
        else:
            return self.blueprint_logic(blueprint)(state)


    def blueprint_logic(self, blueprint:str) -> Callable:
        need_all_requirements = False
        logic = lambda state: True

        match blueprint: # Individual blueprint logic here
            case "BOOK":
                return self.get_pattern_logic(10)
            case "DIAMOND":
                logic = lambda state: state.has_from_list_unique(TOOL_LOCATIONS.keys(),self.world.player,7)
            case "NETHERITE":
                pass # actions >= 30, this is less than 37 so always available
            case "FREE_CHIPS":
                logic = lambda state: state.has_from_list_unique(SHAPE_LOCATIONS.keys(),self.world.player,10)
            case "TOOL_COLOR":
                godot_logic = self.get_pattern_logic(14)
                tool_logic = self.get_pattern_logic(4)
                logic = lambda state: (# normal, cgol, godot, or tool
                    godot_logic(state) or (state.has("BLUEPRINT_TOOL_COLOR",self.world.player) and tool_logic(state))
                )
            case "WEAKEN_BOUNDS":
                logic = self.get_pattern_logic(4, ["5_SQC", "5_TRI", "5_DIA", "7_PLUS", "3/7_RECT", "12_LINE", "8/4_TRI", "7_X", "9_QUAD"])
            case "CHIP_PACK_5":
                if self.world.options.randomize_compatibility_chips:
                    logic = lambda state: state.has("COMPATIBILITY_CHIP",self.world.player,10)
                else:
                    logic = lambda state: can_get_chips(10,self.world,state)
        return lambda state: self.get_recursive_blueprint_logic(blueprint,state,logic,need_all_requirements)


    def get_recursive_blueprint_logic(self, blueprint:str, state, logic, need_all_requirements: bool) -> bool:
        passed = False
        if self.blueprint_tree[blueprint]:
            for i in self.blueprint_tree[blueprint]:
                if need_all_requirements:
                    if not self.blueprint_logic(i)(state):
                        return False
                else:
                    if self.blueprint_logic(i)(state):
                        passed = True
                        break
            if not need_all_requirements and not passed:
                return False

        blueprint_logic = self.get_pattern_logic(10)
        if self.world.options.randomize_blueprints:
            return logic(state) and state.has("BLUEPRINT_BOOK", self.world.player)
        else:
            return logic(state) and blueprint_logic(state)


    def set_blueprint_logic(self, blueprint:str) -> None:
        logic = self.blueprint_logic(blueprint)
        set_rule(self.world.get_location("BLUEPRINT_" + blueprint), logic)


