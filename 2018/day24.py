from enum import Enum

class D(Enum):
    RAD = 0
    BLUDG = 1
    FIRE = 2
    SLASH = 3
    COLD = 4


class ArmyGroup:
    def __init__(self, units, hp, immune, weak, atype, dmg, init) -> None:
        self.units = units
        self.hp = hp
        self.atype = atype
        self.weak = weak
        self.immune = immune
        self.dmg = dmg
        self.init = init

S_IMM = [
    ArmyGroup(17, 5390, [], [D.RAD, D.BLUDG], 4507, D.FIRE, 2),
    ArmyGroup(989, 1274, [D.FIRE], [D.BLUDG, D.SLASH], 25, D.SLASH, 3)
]
S_INF = [
    ArmyGroup(801, 4706, [], [D.RAD], D.BLUDG, 116, 1),
    ArmyGroup(4485, 2961, [D.RAD], [D.FIRE, D.COLD], 12, D.SLASH, 4)
]
R_IMM = [

]
R_INF = [

]