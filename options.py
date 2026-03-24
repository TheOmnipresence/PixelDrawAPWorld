from dataclasses import dataclass

from Options import Choice, OptionGroup, PerGameCommonOptions, Range, Toggle



class TrapChance(Range):
    """
    Percentage chance that any given filler item will be replaced by a trap.
    """

    display_name = "Trap Chance"

    range_start = 0
    range_end = 100
    default = 0


class ActionsNeeded(Range):
    """
    The amount of actions needed to goal. If this is 37 or less, it is possible to win without any checks.
    """

    display_name = "Actions Needed"

    range_start = 0
    range_end = 53
    default = 40


class DeathLink(Toggle):
    """
    Whether or not deathlink will be used.
    """

    display_name = "Death Link"

    default = 0


class RandomizeEnemyDeath(Toggle):
    """
    Adds locations for killing enemies.
    """

    display_name = "Randomize Enemy Death"


@dataclass
class PixelDrawOptions(PerGameCommonOptions):
    trap_chance: TrapChance
    death_link: DeathLink
    randomize_enemy_deaths: RandomizeEnemyDeath
    actions_needed: ActionsNeeded


option_groups = [
    OptionGroup(
        "Gameplay Options",
        [TrapChance, DeathLink, RandomizeEnemyDeath, ActionsNeeded],
    ),
]

option_presets = {
    "normal": {
        "trap_chance": 0,
        "death_link": False,
        "randomize_enemy_deaths": False,
        "actions_needed": 40,
    },
    "harder": {
        "trap_chance": 50,
        "death_link": True,
        "randomize_enemy_deaths": True,
        "actions_needed": 50,
    },
}
