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
        self.owner = True

    def clean_phase (self):
        self.actual_life = self.life
        self.actual_strength = self.strength
        return

class Card:
    def __init__ (self, cost, legendary, c_type, card_from_class):
        self.cost = cost
        self.legendary = legendary
        self.c_type = c_type
        self.card_from_class = card_from_class
        self.inst = True
class Land:
    def __init__ (self, color):
        self.color = color
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
        if tot_mana < 0:
            return False
        return True
    return False

class Effect:
    def add_counter_crea(crea, nb_l, nb_s):
        crea.life += nb_l
        crea.strength += nb_s
        crea.actual_life += nb_l
        crea.actual_strength += nb_s
        return

def effect (left, effect_add):
    if perma_boost in effect_add.key:
        add_counter_crea(effect_add[perma_boost[0]], effect_add[perma_boost[1]], effect_add[perma_boost[2]])
    return

class Battlefield:
    def __init__ (self, deck_j_left, deck_j_right):
        self.end = False
        self.winner = 0
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
        self.nb_land_play_left, self.nb_land_play_right = 1
        self.hand_size_left, self.hand_size_right = 7
        self.upkeep_left, self.upkeep_right = []
        self.combat_left, self.combat_right = []
        self.step = ["attack", "main", "block", "damage", "end step", "upkeep"]
        self.trigger_effect_attack_left, self.trigger_effect_attack_right = []
        self.trigger_effect_damage_left, self.trigger_effect_damage_right = []
        self.trigger_effect_upkeep_left, self.trigger_effect_upkeep_right = []
        self.trigger_effect_end_step_left, self.trigger_effect_end_step_right = []
        
    def draw (self, left, n):
        if left:
            if len(deck_j_left < n):
                win_the_game(False)
            for i in range (n):
                hand_j_left.append(deck_j_left.pop())
            return
        if len(deck_j_right < n):
                win_the_game(True)
        for i in range (n):
            hand_j_right.append(deck_j_right.pop())
        return

    def upkeep (self, left):
        untap_step (self, left)
        if left:
            for eff in self.trigger_effect_upkeep_left:
                eff.trigger()
        else:
            for eff in self.trigger_effect_upkeep_right:
                eff.trigger()
        draw (self, left, 1)

    def clean_step (self):
        for crea in creature_j_left:
            crea.actual_life = crea.life
            crea.actual_strength = crea.strength
        for crea in creature_j_right:
            crea.actual_life = crea.life
            crea.actual_strength = crea.strength
        return

    def discard (self, left, n):
        if left:
            shuffle (self.hand_j_left)
            for i in range (n):
                hand_j_left.pop()
            return
        shuffle (self.hand_j_right)
        for i in range (n):
            hand_j_right.pop()

    def end_step (self, left):
        if left:
            for eff in trigger_effect_end_step_left:
                eff.trigger ()
            if (self.hand_size_left - len(self.hand_j_left)) < 0:
                discard (self, left, (len(self.hand_j_left) - self.hand_size_left))
            return clean_step ()
        for eff in trigger_effect_end_step_right:
            eff.trigger ()
        if (self.hand_size_right - len(self.hand_j_right)) < 0:
            discard (self, left, (len(self.hand_j_right) - self.hand_size_right))
        return clean_step ()      

    def play_land (self, left, n):
        land_in_hand = []
        if left:
            for c in self.hand_j_left:
                if c.c_type == "land":
                    land_in_hand.append(c)
            for i in range (n):
                self.manabase_j_left[land_in_hand.pop().card_from_class.color] += 1
            return
        for c in self.hand_j_right:
            if c.c_type == "land":
                land_in_hand.append(c)
        for i in range (n):
            if len(land_in_hand) > 0:
                self.manabase_j_right[land_in_hand.pop().card_from_class.color] += 1
        return
    def possible_attacking_creature(self, left):
        tab = []
        if left:
            for crea in board_j_left:
                if crea.can_attack and not (crea.is_tap):
                    tab.append(crea)
        else:
            for crea in board_j_right:
                if crea.can_attack and not (crea.is_tap):
                    tab.append(crea)
        return tab
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
    def dying_creature (self, tab):
        for i in range (len(self.creature_j_left) -1):
            if self.creature_j_left[i].actual_life < 1:
                tab.append(self.creature_j_left.pop([i]))
        for i in range (len(self.creature_j_right) -1):
            if self.creature_j_right[i].actual_life < 1:
                tab.append(self.creature_j_right.pop([i]))
        return

class Combat_phase:
    def __init__ (self, actual_battlefield):
        self.actual_battlefield = actual_battlefield
        self.attacking_creature = {}
        self.died_creature = []
    def reset (self):
        self.attacking_creature = {}
        self.died_creature = []
    def attack_phase (self, attacking_creature_tab):
        for crea in attacking_creature_tab:
            self.attacking_creature[crea] = []
    def assign_damage (self):
        for crea in self.attacking_creature.keys:
            if attacking_creature[crea] == []:
                if crea.owner:
                    self.actual_battlefield.life_j_right -= crea.actual_strength
                else:
                    self.actual_battlefield.life_j_right -= crea.actual_strength
            else:
                crea.actual_life -= self.attacking_creature[crea].actual_strength
                self.attacking_creature[crea].actual_life -= crea.actual_strength
        dying_creature (self.died_creature)
    def died_effect (self):
        for crea in died_creature:
            c = died_creature.pop()
            c.died_effect()
    def finish (self):
        if actual_battlefield.is_finish == -1:
            actual_battlefield.end = True


Gigantosaurus_creature = Creature(10, 10, [], {})
Gigantosaurus = Card(["green","green","green","green","green"], False, "creature",{})
Test1_creature = Creature(1, 1, [], {"perma_boost" : (None, 1,1)})