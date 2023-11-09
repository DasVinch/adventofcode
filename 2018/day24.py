from __future__ import annotations

from enum import Enum

class WHO(Enum):
    INF = 0
    IMM = 1

class D(Enum):
    RAD = 0
    BLUDG = 1
    FIRE = 2
    SLASH = 3
    COLD = 4

from dataclasses import dataclass

@dataclass
class ArmyGroup:
    army: WHO
    units: int
    hp: int
    immune: list[D]
    weak: list[D]
    dmg: int
    atype: D
    init: int

    def postinit(self) -> None:
        self.select: ArmyGroup | None = None
        self.selected_by: ArmyGroup | None = None

    @property
    def eff_power(self) -> int:
        return self.dmg * self.units
    
    def damage_to(self, other: ArmyGroup) -> int:
        if self.atype in other.immune:
            return 0
        if self.atype in other.weak:
            return 2*self.eff_power
        return self.eff_power

    def max_damageable(self: ArmyGroup, t: list[ArmyGroup]) -> ArmyGroup | None:
        max_dmg: int = 0
        max_node: ArmyGroup | None = None
        for aggrod in t:
            assert aggrod.army != self.army
            this_dmg = self.damage_to(aggrod)
            if (this_dmg > max_dmg or 
                (max_node is not None and this_dmg == max_dmg and
                (aggrod.eff_power > max_node.eff_power or
                (aggrod.eff_power == max_node.eff_power and aggrod.init > max_node.init))
                )
            ):
                max_dmg = this_dmg
                max_node = aggrod

        return max_node

    def assign_target(self, t: list[ArmyGroup]) -> ArmyGroup | None:
        max_node = self.max_damageable(t)
        if max_node is None:
            return None
        
        assert self.select is None
        self.select = max_node

        assert max_node.selected_by is None
        max_node.selected_by = self
        
        return max_node
    
    def deal_damage_to_selection(self) -> None:
        assert self.select is not None

        dmg = self.damage_to(self.select)
        print(f'{self} doing {dmg} {self.atype} damage to\n      {self.select}.')
        
        self.select.units -= dmg // self.select.hp
        if self.select.units < 0:
            self.select.units = 0

    

S_IMM = lambda: [
    ArmyGroup(WHO.IMM, 17, 5390, [], [D.RAD, D.BLUDG], 4507, D.FIRE, 2),
    ArmyGroup(WHO.IMM, 989, 1274, [D.FIRE], [D.BLUDG, D.SLASH], 25, D.SLASH, 3)
]
S_INF = lambda: [
    ArmyGroup(WHO.INF, 801, 4706, [], [D.RAD], 116, D.BLUDG, 1),
    ArmyGroup(WHO.INF, 4485, 2961, [D.RAD], [D.FIRE, D.COLD], 12, D.SLASH, 4)
]

#Immune System:
R_IMM = lambda: [
    # 76 units each with 3032 hit points
    # with an attack that does 334 radiation damage at initiative 7
    ArmyGroup(WHO.IMM, 76, 3032, [], [], 334, D.RAD, 7),
    # 4749 units each with 8117 hit points
    # with an attack that does 16 bludgeoning damage at initiative 16
    ArmyGroup(WHO.IMM, 4749, 8117, [], [], 16, D.BLUDG, 16),
    # 4044 units each with 1287 hit points (immune to radiation, fire)
    # with an attack that does 2 fire damage at initiative 20
    ArmyGroup(WHO.IMM, 4044, 1287, [D.RAD, D.FIRE], [], 2, D.FIRE, 20),
    # 1130 units each with 11883 hit points (weak to radiation)
    # with an attack that does 78 radiation damage at initiative 14
    ArmyGroup(WHO.IMM, 1130, 11883, [], [D.RAD], 78, D.RAD, 14),
    # 1698 units each with 2171 hit points (weak to slashing, fire)
    # with an attack that does 11 bludgeoning damage at initiative 12
    ArmyGroup(WHO.IMM, 1698, 2171, [], [D.SLASH, D.FIRE], 11, D.BLUDG, 12),
    # 527 units each with 1485 hit points
    # with an attack that does 26 bludgeoning damage at initiative 17
    ArmyGroup(WHO.IMM, 527, 1485, [], [], 26, D.BLUDG, 17),
    # 2415 units each with 4291 hit points (immune to radiation)
    # with an attack that does 17 cold damage at initiative 5
    ArmyGroup(WHO.IMM, 2415, 4291, [D.RAD], [], 17, D.COLD, 5),
    # 3266 units each with 6166 hit points (immune to cold, slashing; weak to radiation)
    # with an attack that does 17 bludgeoning damage at initiative 18
    ArmyGroup(WHO.IMM, 3266, 6166, [D.COLD, D.SLASH], [D.RAD], 17, D.BLUDG, 18),
    # 34 units each with 8390 hit points (immune to cold, fire, slashing)
    # with an attack that does 2311 cold damage at initiative 10
    ArmyGroup(WHO.IMM, 34, 8390, [D.COLD, D.FIRE, D.SLASH], [], 2311, D.COLD, 10),
    # 3592 units each with 5129 hit points (immune to cold, fire; weak to radiation)
    # with an attack that does 14 radiation damage at initiative 11
    ArmyGroup(WHO.IMM, 3592, 5129, [D.COLD, D.FIRE], [D.RAD], 14, D.RAD, 11),
]
# Infection:
R_INF = lambda: [
    # 3748 units each with 11022 hit points (weak to bludgeoning)
    # with an attack that does 4 bludgeoning damage at initiative 6
    ArmyGroup(WHO.INF, 3748, 11022, [], [D.BLUDG], 4, D.BLUDG, 6),
    # 2026 units each with 11288 hit points (weak to fire, slashing)
    # with an attack that does 10 slashing damage at initiative 13
    ArmyGroup(WHO.INF, 2026, 11288, [], [D.FIRE, D.SLASH], 10, D.SLASH, 13),
    # 4076 units each with 23997 hit points (immune to cold)
    # with an attack that does 11 bludgeoning damage at initiative 19
    ArmyGroup(WHO.INF, 4076, 23997, [D.COLD], [], 11, D.BLUDG, 19),
    # 4068 units each with 40237 hit points (immune to cold; weak to slashing)
    # with an attack that does 18 slashing damage at initiative 4
    ArmyGroup(WHO.INF, 4068, 40237, [D.COLD], [D.SLASH], 18, D.SLASH, 4),
    # 3758 units each with 16737 hit points (weak to slashing)
    # with an attack that does 6 radiation damage at initiative 2
    ArmyGroup(WHO.INF, 3758, 16737, [], [D.SLASH], 6, D.RAD, 2),
    # 1184 units each with 36234 hit points (weak to bludgeoning, fire; immune to cold)
    # with an attack that does 60 radiation damage at initiative 1
    ArmyGroup(WHO.INF, 1184, 36234, [D.COLD], [D.BLUDG, D.FIRE], 60, D.RAD, 1),
    # 1297 units each with 36710 hit points (immune to cold)
    # with an attack that does 47 fire damage at initiative 3
    ArmyGroup(WHO.INF, 1297, 36710, [D.COLD], [], 47, D.FIRE, 3),
    # 781 units each with 18035 hit points (immune to bludgeoning, slashing)
    # with an attack that does 36 fire damage at initiative 15
    ArmyGroup(WHO.INF, 781, 18035, [D.BLUDG, D.SLASH], [], 36, D.FIRE, 15),
    # 1491 units each with 46329 hit points (immune to slashing, bludgeoning)
    # with an attack that does 56 fire damage at initiative 8
    ArmyGroup(WHO.INF, 1491, 46329, [D.SLASH, D.BLUDG], [], 56, D.FIRE, 8),
    # 1267 units each with 34832 hit points (immune to cold)
    # with an attack that does 49 radiation damage at initiative 9
    ArmyGroup(WHO.INF, 1267, 34832, [D.COLD], [], 49, D.RAD, 9),
]

def sort_choosing_order(t: list[ArmyGroup]):
    t.sort(key=lambda ag: (ag.eff_power, ag.init),reverse=True)

def sort_combat_order(t: list[ArmyGroup]):
    t.sort(key = lambda ag: ag.init, reverse=True)


class Combat:
    def __init__(self, immune: list[ArmyGroup], infection: list[ArmyGroup]) -> None:
        self.immune = immune
        self.infection = infection

        self.all_groups = immune + infection

        for g in self.all_groups:
            g.postinit()

    def one_combat(self):
        self.selection_phase()
        self.combat_phase()
        self.cleanup()

    def cleanup(self) -> None:
        self.immune = [g for g in self.immune if g.units > 0]
        self.infection = [g for g in self.infection if g.units > 0]
        self.all_groups = [g for g in self.all_groups if g.units > 0]

    def complete(self) -> bool:
        return len(self.immune) == 0 or len(self.infection) == 0
    
    def winner(self) -> WHO:
        return self.all_groups[0].army

    def selection_phase(self) -> None:
        sort_choosing_order(self.all_groups)
        for group in self.all_groups:
            candidate_targets = [g for g in self.all_groups if g.army != group.army and g.selected_by is None]
            group.assign_target(candidate_targets)

    def combat_phase(self) -> None:
        sort_combat_order(self.all_groups)
        for group in self.all_groups:
            if group.select is not None:
                group.deal_damage_to_selection()
                group.select.selected_by = None
            group.select = None

def try_boost(imm: list[ArmyGroup], inf: list[ArmyGroup], boost: int):
    for ag in imm:
        ag.orig_dmg = ag.dmg
        ag.dmg += boost
    
    print(imm)
    this_combat = Combat(imm, inf)
    while not this_combat.complete():
        this_combat.one_combat()
    
    print(this_combat.winner())
    print(sum([g.units for g in this_combat.all_groups]))

    for ag in imm:
        ag.dmg = ag.orig_dmg


if __name__ == "__main__":
    combat = Combat(S_IMM(), S_INF())
    combat = Combat(R_IMM(), R_INF())

    while not combat.complete():
        combat.one_combat()

    print(sum([g.units for g in combat.all_groups]))


    try_boost(R_IMM(), R_INF(), 115) # Infection wins
    try_boost(R_IMM(), R_INF(), 119) # Immune wins
    # 116, 117, 118 don't terminate. Remaining standing groups but damage is not enough to kill 1 unit of selected group.