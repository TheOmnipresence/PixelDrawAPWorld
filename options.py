from dataclasses import dataclass

from Options import Choice, OptionGroup, PerGameCommonOptions, Range, Toggle, FreeText, NamedRange, OptionList, OptionSet


class TrapChance(Range):
    """
    Percentage chance that any given filler item will be replaced by a trap.
    """

    display_name = "Trap Chance"

    range_start = 0
    range_end = 100
    default = 0


class ActionsNeeded(NamedRange):
    """
    The amount of actions needed to goal. If this is 37 or less, it is possible to win without any checks.
    """

    display_name = "Actions Needed"

    range_start = 0
    range_end = 60
    special_range_names = {
        "not_for_goal": 0,
        "all_base_actions": 37,
        "default": 45,
        "max": range_end
    }
    default = 45


class DeathLink(Toggle):
    """
    Whether or not deathlink will be used.
    """

    display_name = "Death Link"

    default = 0


class DeathLinkAmnesty(Range):
    """
    The amount of deaths required to send a deathlink.
    """

    display_name = "Death Link Amnesty"

    range_start = 1
    range_end = 20
    default = 1


class RandomizeEnemyDeath(Toggle):
    """
    Adds locations for killing enemies.
    """

    display_name = "Randomize Enemy Death"


class RandomizeCompatibilityChips(Toggle):
    """
    Randomizes compatibility chips.
    Each action that gets you them has as many checks as it would have chips normally.
    Each chip is an item.
    """

    display_name = "Randomize Compatibility Chips"
    default = False


class AdditionalCompatibilityChips(Range):
    """
    Adds x amount of extra compatibility chips to the item pool (if there are not enough locations left, it will cut off).
    This only matters if compatibility chips are randomized.
    """

    display_name = "Additional Compatibility Chips"
    default = 0

    range_start = 0
    range_end = 20


class RandomizeSalesmen(Toggle):
    """
    Randomizes salesmen items, aside from currency conversion.
    """

    display_name = "Randomize Salesmen"
    default = False


class CompletionShape(FreeText):
    """
    The extra shape that you will need to scan to goal, after all other requirements.
    If left blank, there is no ending shape needed. This must be either in binary or hexadecimal (starting with '0x' for hex, and either nothing or '0b' for binary) formats.
    """

    display_name = "Completion Shape"

    default = ""


class NeededPatterns(OptionSet):
    """
    The extra patterns needed to goal. If left empty, none are needed.
    These must be either in binary or hexadecimal (starting with '0x' for hex, and either nothing or '0b' for binary) formats.
    """

    display_name = "Needed Patterns"

    default = []


@dataclass
class PixelDrawOptions(PerGameCommonOptions):
    trap_chance: TrapChance
    death_link: DeathLink
    randomize_enemy_deaths: RandomizeEnemyDeath
    randomize_compatibility_chips: RandomizeCompatibilityChips
    additional_compatibility_chips: AdditionalCompatibilityChips
    randomize_salesmen: RandomizeSalesmen
    actions_needed: ActionsNeeded
    completion_shape: CompletionShape
    needed_patterns: NeededPatterns
    death_link_amnesty: DeathLinkAmnesty


option_groups = [
    OptionGroup(
        "Gameplay Options",
        [TrapChance, DeathLink, DeathLinkAmnesty, RandomizeEnemyDeath, RandomizeCompatibilityChips, AdditionalCompatibilityChips, RandomizeSalesmen],
    ),
    OptionGroup(
        "Goal Requirements",
        [ActionsNeeded, CompletionShape, NeededPatterns],
    )
]

option_presets = {
    "normal": {
        "trap_chance": 0,
        "death_link": False,
        "death_link_amnesty": 1,
        "randomize_enemy_deaths": False,
        "randomize_compatibility_chips": False,
        "additional_compatibility_chips": 0,
        "randomize_salesmen": False,
        "actions_needed": 40,
        "completion_shape": "",
        "needed_patterns": [],
    },
    "harder": {
        "trap_chance": 50,
        "death_link": True,
        "death_link_amnesty": 1,
        "randomize_enemy_deaths": True,
        "randomize_compatibility_chips": True,
        "additional_compatibility_chips": 0,
        "randomize_salesmen": True,
        "actions_needed": 50,
        "completion_shape": "0xfec68aba9ac6fe",
        "needed_patterns": [],
    },
}
