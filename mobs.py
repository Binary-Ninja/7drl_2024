from enum import Enum, auto
from collections import namedtuple

from data import Color, Graphic
from items import ItemID


class MobID(Enum):
    PLAYER = 1
    GREEN_ZOMBIE = 2
    GREEN_SLIME = 3
    GREEN_SKELETON = 4
    AIR_WIZARD = 5
    WORKBENCH = 6


class MobTag(Enum):
    PUSHABLE = auto()
    CRAFTING = auto()


# First item is the result, the rest are the ingredients.
recipies = {
    MobID.WORKBENCH: (
        ((ItemID.WORKBENCH, 1), (ItemID.WOOD, 10)),
        ((ItemID.DIRT, 12), (ItemID.STONE, 6), (ItemID.WOOD, 6)),
    ),
}


MobData = namedtuple("MobData", ("name", "graphic", "max_health", "tags",
                                 "recipies"), defaults=(10, tuple(), None,))
mob_data = {
    MobID.PLAYER: MobData("player", (Graphic.PLAYER, Color.WHITE)),
    MobID.GREEN_ZOMBIE: MobData("zombie", (Graphic.ZOMBIE, Color.MOB_GREEN)),
    MobID.GREEN_SLIME: MobData("slime", (Graphic.SLIME, Color.MOB_GREEN)),
    MobID.GREEN_SKELETON: MobData("skeleton", (Graphic.SKELETON, Color.MOB_GREEN), 10,
                                  (MobTag.PUSHABLE,)),
    MobID.AIR_WIZARD: MobData("air wizard", (Graphic.AIR_WIZARD, Color.RED), 100),
    MobID.WORKBENCH: MobData("workbench", (Graphic.WORKBENCH, Color.BROWN), 10,
                             (MobTag.PUSHABLE, MobTag.CRAFTING), recipies[MobID.WORKBENCH]),
}


class Mob:
    def __init__(self, mobid: MobID):
        self.id = mobid
        self.mob_data = mob_data[self.id]
        self.name = self.mob_data.name
        self.graphic = self.mob_data.graphic
        self.health = self.mob_data.max_health
        self.tags = self.mob_data.tags
        self.recipies = self.mob_data.recipies

    def has_tag(self, tag: MobTag) -> bool:
        return tag in self.tags
