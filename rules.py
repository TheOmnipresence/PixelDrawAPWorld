from __future__ import annotations

import typing
from typing import TYPE_CHECKING

from BaseClasses import CollectionState
from worlds.generic.Rules import add_rule, set_rule
from ..stardew_valley.stardew_rule import true_

if TYPE_CHECKING:
    from .world import PixelDrawWorld

toolsCompatibility = {
	"NONE":[],
	"VOIDER":[],
	"ERASER":[],
	"C_GOL":[		"NONE",		"BASE_RECT",	"5_SQR",	"6_SQR"																																												],
	"RAISER":[		"NONE",												"SM_DIA",	"5_PLUS",													"5_SQC"																							],
	"LEVELER":[		"NONE",		"BASE_RECT",	"5_SQR",																															"5_TRI"														],
	"DUSTER":[		"NONE",		"BASE_RECT",				"6_SQR",																																								"8_CIR",	],
	"SHUFFLER":[	"NONE",						"5_SQR"																																															],
	"STOPPER":[		"NONE",												"SM_DIA",												"7_LINE"																										],
	"BULB":[		"NONE",															"5_PLUS",		"3_DIAG",	"3_DIAG_IN"																														],
	"MC_PICK":[		"NONE",																										"7_LINE"																										],
	"HOOK":[		"NONE",									"6_SQR",																			"5_SQC"																							],
	"BASE_SW":[		"NONE",																			"3_DIAG",	"3_DIAG_IN",											"5_DIAG"																],
	"PLACER":[		"NONE",																			"3_DIAG",	"3_DIAG_IN"																														],
	"STAMPER":[		"NONE",									"6_SQR"																																												],
	"GRAVITATE":[	"NONE",																																							"5_TRI"														],
	"SUMMON":[		"NONE",						"5_SQR",																									"10_SQR"																			],
	"TERRAIN":[		"NONE",						"5_SQR",																																		"50_SQR",	"200_SQR",							],
	"PARALYZER":[	"NONE",																																																"7_SQC",				],
	"PLATFORMS":[	"NONE",																																										"50_SQR",				"7_SQC",				],
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
                return lambda state: True
            case _:
                result.append(toolshape)
    if not result:
        return lambda state: False
    else:
        return lambda state: (state.has_any(result, world.player) and state.has(tool, world.player))



def set_all_location_rules(world: PixelDrawWorld) -> None:
    # shuffler or (mc_pick and placer) or (stamper and c_gol and duster) or platforms
    #manipulators = (lambda state: can_use_tool(world,"SHUFFLER") or can_use_tool(world,"PLATFORMS") or (can_use_tool(world,"MC_PICK") and can_use_tool(world,"PLACER")) or (can_use_tool(world,"STAMPER") and can_use_tool(world,"C_GOL")))
    manipulators = (lambda state:
        can_use_tool(world, "SHUFFLER")(state) or
        can_use_tool(world, "PLATFORMS")(state) or
        (can_use_tool(world, "MC_PICK")(state) and can_use_tool(world, "PLACER")(state)) or
        (can_use_tool(world, "STAMPER")(state) and can_use_tool(world, "C_GOL")(state) and can_use_tool(world,"DUSTER")(state))
    )

    fifty_size = (lambda state: state.has_any(["50_SQR"], world.player))
    eight_size = (lambda state: state.has_any(["10_SQR","16_SQR"], world.player))
    seven_size = (lambda state: state.has_any([], world.player) or eight_size(state))
    six_size = (lambda state: state.has_any(["6_SQR"], world.player) or seven_size(state))
    five_size = (lambda state: state.has_any(["5_SQR","7_SQC"], world.player) or six_size(state))
    four_size = (lambda state: state.has_any([], world.player) or five_size(state))

    set_rule(world.get_location("6_SQR"),lambda state: four_size(state) and manipulators(state))
    set_rule(world.get_location("SM_DIA"),lambda state: (five_size(state) or state.has_any(["5_SQC"], world.player)) and manipulators(state))
    set_rule(world.get_location("5_PLUS"), lambda state: (five_size(state) or state.has_any(["5_PLUS","5_SQC"], world.player)) and manipulators(state))
    set_rule(world.get_location("BULB"), lambda state: (five_size(state) or state.has("5_SQC", world.player)) and manipulators(state))
    set_rule(world.get_location("MC_PICK"), lambda state: four_size(state) and manipulators(state))
    set_rule(world.get_location("7_LINE"), lambda state: (five_size(state) or state.has_any(["5_PLUS","7_LINE","5_SQC","5_TRI","7_LOOP"], world.player)) and manipulators(state))
    set_rule(world.get_location("5_SQC"), lambda state: (four_size(state) or state.has_any(["5_SQC"], world.player)) and manipulators(state))
    set_rule(world.get_location("10_SQR"), lambda state: six_size(state) and manipulators(state))
    set_rule(world.get_location("16_SQR"), lambda state: eight_size(state) and manipulators(state))
    set_rule(world.get_location("STAMPER"), lambda state: eight_size(state) and manipulators(state))
    set_rule(world.get_location("GRAVITATE"), lambda state: (four_size(state) or state.has_any(["5_SQC"], world.player)) and manipulators(state))
    set_rule(world.get_location("50_SQR"), lambda state: five_size(state) and manipulators(state))
    set_rule(world.get_location("7_LOOP"), lambda state: five_size(state) and manipulators(state))
    set_rule(world.get_location("PLATFORMS"), lambda state: five_size(state) and manipulators(state))
    #set_rule(world.get_location("200_SQR"), lambda state: fifty_size(state) and manipulators(state))
    set_rule(world.get_location("8_CIR"), lambda state: four_size(state) and manipulators(state))

    if world.options.randomize_enemy_deaths:
        set_rule(world.get_location("RED_PILL"), lambda state: (four_size(state) or state.has_any(["5_SQC","5_TRI"], world.player)) and manipulators(state) and state.has("BASE_SW",world.player))
        set_rule(world.get_location("TRI_ENEMY"), lambda state: state.has("BASE_SW", world.player))
        set_rule(world.get_location("ZOOM_ENEMY"), lambda state: state.has("BASE_SW", world.player))
        set_rule(world.get_location("SMALL_BIRD"), lambda state: state.has("BASE_SW", world.player))

def set_completion_condition(world: PixelDrawWorld) -> None:
    manipulators = (lambda state: can_use_tool(world, "SHUFFLER")(state) or can_use_tool(world, "PLATFORMS")(state) or (can_use_tool(world, "MC_PICK")(state) and can_use_tool(world, "PLACER")(state)) or (can_use_tool(world, "STAMPER")(state) and can_use_tool(world, "C_GOL")(state) and can_use_tool(world,"DUSTER")(state)))

    world.multiworld.completion_condition[world.player] = lambda state: state.has_all(["5_SQR","50_SQR"], world.player) and manipulators(state)