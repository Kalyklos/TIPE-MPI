from stack_v import *
import random
random.seed()
class Creature:
    def __init__ (self, strength, life, keywords, effect):
        self.strength = strength
        self.life = life
        self.keywords = keywords
        self.effect = effect
        self.actual_life = self.life
        self.actual_strength = self.strength
        self.can_attack = False
        self.is_tap = False
        self.can_untap = True

    def clean_phase (self):
        self.actual_life = self.life
        self.actual_strength = self.strength
        return

class Card:
    def __init__ (self, cost, legendary, c_type, effect):
        self.cost = cost
        self.legendary = legendary
        self.c_type = c_type
        self.effect = effect
        self.inst = True

def opti_spend_colorless (mana, card):
    pass #to do but later

def is_playable (can_cast_sorcery, mana, card):
    mana_cp = mana.copy()
    tot_mana = 0
    for l in mana:
        tot_mana += mana[l]
    if (card.inst or can_cast_sorcery):
        for symbol in cost:
            if (mana[symbol] <= card.cost[symbol]) and (symbol != "colorless"):
                return (False, mana)
            else:
                tot_mana -= card.cost[symbol]
                mana_cp[symbol] = mana_cp[symbol] - card.cost[symbol]
        tot_mana -= card.cost["colorless"]

        if tot_mana >= 0:
            return False
        opti_spend_colorless (mana_cp, card)
        return (True, mana_cp)
    return (False, mana)

class Battlefield:
    def __init__ (self, deck_j_left, deck_j_right):
        self.life_j_left, self.life_j_right = 20
        self.can_cast_sorcery_left, self.can_cast_sorcery_right = False
        self.manabase_j_left = {}
        self.remaining_mana_left = {}
        self.remaining_mana_rights = {}
        self.manabase_j_right = {}
        self.board_j_left = []
        self.board_j_right = []
        self.creature_j_left = []
        self.creature_j_right = []
        self.deck_j_left = deck_j_left
        self.deck_j_right = deck_j_right
        self.hand_j_left, self.hand_j_right = []
        self.gravyard_j_left, self.gravyard_j_right = []
        self.upkeep_left, self.upkeep_right = []
        self.combat_left, self.combat_right = []
    def is_finish (self):
        if self.life_j_left < 1:
            return 0
        if self.life_j_right < 1:
            return 1
        return -1
    def win_the_game (self, left):
        return left
    def untap_step (self, left):
        if left:
            self.remaining_mana_left = manabase_j_left.copy()
            for crea in self.creature_j_left:
                if crea.can_untap:
                    crea.is_tap = False
            return
        self.remaining_mana_right = manabase_j_right.copy()
        for crea in self.creature_j_right:
            if crea.can_untap:
                crea.is_tap = False
        return
    def main_phase (self, left, eff):
        if left:
            self.can_cast_sorcery_left = True
        else:
            self.can_cast_sorcery_right = True
    def new_creature (self, left, crea):
        if left:
            self.creature_j_left.append(crea)
            return
        self.creature_j_right.append(crea)
        return
    def play_a_card (mana, card, left):
        for symbol in cost:
            mana[symbol] = mana[symbol] - card.cost[symbol]
        opti_spend_colorless (mana_cp, card)
        if left:
            hand_j_left.remove(card)
        else:
            hand_j_right.remove(card)
        eff_etb (card, left)
        return
    def draw (self, left, n):
        if left:
            if len(deck_j_left < n):
                win_the_game(False)
            for i in range (n):
                hand_j_left.append(pop(deck_j_left))
            return
        if len(deck_j_right < n):
                win_the_game(True)
        for i in range (n):
            hand_j_right.append(pop(deck_j_right))
        return
    def game_begin (self):
        random.shuffle(self.deck_j_left)
        random.shuffle(self.deck_j_right)
        draw (True, 7)
        draw (False, 7)
        return randint(1, 2) == 1
    def new_turn (self, first, left):
        if left:
            for i in self.upkeep_left:
                eff_card(i, left)
        else:
            for i in self.upkeep_right:
                eff_card(i, left)
        draw(left, 1)
        untap (left)
        return
def add_counter_crea(crea, nb_l, nb_s):
    crea.life += nb_l
    crea.strength += nb_s
    crea.actual_life += nb_l
    crea.actual_strength += nb_s
    return

def Effect (left, effect_add):
    if perma_boost in effect_add.key:
        add_counter_crea(effect_add[perma_boost[0]], effect_add[perma_boost[1]], effect_add[perma_boost[2]])
    return
    


Gigantosaurus_creature = Creature(10, 10, [], {})
Gigantosaurus = Card(["green","green","green","green","green"], False, "creature",{})
Test1_creature = Creature(1, 1, [], {"perma_boost" : (None, 1,1)})