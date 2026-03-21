from __future__ import annotations

from typing import TYPE_CHECKING

from BaseClasses import Entrance, Region

if TYPE_CHECKING:
    from .world import PixelDrawWorld


def create_and_connect_regions(world: PixelDrawWorld) -> None:
    create_all_regions(world)
    connect_regions(world)


def create_all_regions(world: PixelDrawWorld) -> None:
    plane = Region("Plane", world.player, world.multiworld)

    regions = [plane]

    world.multiworld.regions += regions


def connect_regions(world: PixelDrawWorld) -> None:
    return
