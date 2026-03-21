from dataclasses import dataclass

from Options import Choice, OptionGroup, PerGameCommonOptions, Range, Toggle

# In this file, we define the options the player can pick.
# The most common types of options are Toggle, Range and Choice.

# Options will be in the game's template yaml.
# They will be represented by checkboxes, sliders etc. on the game's options page on the website.
# (Note: Options can also be made invisible from either of these places by overriding Option.visibility.
#  APQuest doesn't have an example of this, but this can be used for secret / hidden / advanced options.)

# For further reading on options, you can also read the Options API Document:
# https://github.com/ArchipelagoMW/Archipelago/blob/main/docs/options%20api.md


class TrapChance(Range):
    """
    Percentage chance that any given filler item will be replaced by a trap.
    """

    display_name = "Trap Chance"

    range_start = 0
    range_end = 100
    default = 0


class ActionsNeeded(Range):


    display_name = "Actions Needed"

    range_start = 0
    range_end = 39
    default = 39


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


# We must now define a dataclass inheriting from PerGameCommonOptions that we put all our options in.
# This is in the format "option_name_in_snake_case: OptionClassName".
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
        "actions_needed": 25,
    },
    "harder": {
        "trap_chance": 50,
        "death_link": True,
        "randomize_enemy_deaths": True,
        "actions_needed": 39,
    },
}
