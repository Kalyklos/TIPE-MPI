from stack_v import *
class Creature:
    def __init__ (self, strength, life, keywords, effect):
        self.strength = strength
        self.life = life
        self.keywords = keywords
        self.effect = effect
        self.actual_life = self.life
        self.actual_strength = self.strength
        self.can_attack = False

    def clean_phase (self):
        self.actual_life = self.life
        self.actual_strength = self.strength
        return

class Battlefield:
    def __init__ (self):
        self.manabase_j_left = {}
        self.manabase_j_right = {}
        self.board_j_left = []
        self.board_j_right = []
        self.creature_j_left = []
        self.creature_j_right = []
    def new_creature (self, left, crea):
        if left:
            self.creature_j_left.append(crea)
            return
        self.creature_j_right.append(crea)
        return
    