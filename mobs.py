from enum import Enum
from collections import namedtuple

from data import Color, Graphic


class MobID(Enum):
    PLAYER = 1
    GREEN_ZOMBIE = 2
    GREEN_SLIME = 3
    GREEN_SKELETON = 4
    AIR_WIZARD = 5


MobData = namedtuple("MobData", ("name", "graphic", "max_health"))
mob_data = {
    MobID.PLAYER: MobData("player", (Graphic.PLAYER, Color.WHITE), 10),
    MobID.GREEN_ZOMBIE: MobData("zombie", (Graphic.ZOMBIE, Color.MOB_GREEN), 10),
    MobID.GREEN_SLIME: MobData("slime", (Graphic.SLIME, Color.MOB_GREEN), 10),
    MobID.GREEN_SKELETON: MobData("skeleton", (Graphic.SKELETON, Color.MOB_GREEN), 10),
    MobID.AIR_WIZARD: MobData("air wizard", (Graphic.AIR_WIZARD, Color.RED), 100),
}


class Mob:
    def __init__(self, mobid: MobID):
        self.id = mobid
        self.mob_data = mob_data[self.id]
        self.name = self.mob_data.name
        self.graphic = self.mob_data.graphic
        self.health = self.mob_data.max_health
