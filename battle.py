from stack_v import *
import random
random.seed() #to give something that seem more random to use the random function (cause the random is hardcode)
class Effect:
    def __init__ (self, upkeep_t, endstep_t, entering, dying):
        """init of the effect class

        Args:
            upkeep_t (tab): _description_
            endstep_t (tab): _description_
            entering (tab): _description_
            dying (tab): _description_
        """
        self.upkeep_t = upkeep_t
        self.endstep_t = endstep_t
        self.entering = entering
        self.dying = dying
    def add_counter_crea(crea, nb):
        """Put nb +1/+1 counter onto the creature crea

        Args:
            crea (Creature): The creature to put counter on it
            nb (int): the number of counter
        """
        crea.life += nb
        crea.strength += nb
        crea.actual_life += nb
        crea.actual_strength += nb
        return
    def 

def effect (left, effect_add):
    if perma_boost in effect_add.key:
        add_counter_crea(effect_add[perma_boost[0]], effect_add[perma_boost[1]], effect_add[perma_boost[2]])
    return

class Creature:
    def __init__ (self, strength, life, keywords, effect, cost):
        """Init of the creature class

        Args:
            strength (int): strength of the creature
            life (int): toughness of the creature
            keywords (tab of str): keywords of the creature (like Trample, Flying...)
            effect (Effect): effect of the creature (upkeep, endstep, entering, dying)
            cost (dict): dictionnaire of colors and the nombers of mana of that type in their cost (ex : "Green" : 5)
        """
        self.strength = strength
        self.life = life
        self.keywords = keywords
        self.effect = effect
        self.actual_life = self.life
        self.actual_strength = self.strength
        self.is_tap = False
        self.can_untap = True
        self.owner = True
        self.cost = cost
        self.summoning_sickness = True
        self.mana_producers = 0

class Land:
    def __init__ (self, color):
        """init of the Land class

        Args:
            color (str): The color of mana that produce the land
        """
        self.color = color

class Card:
    def __init__ (self, c_type, name):
        """init of the Card class

        Args:
            c_type (str): The type of the card (like "Creature", "Instant"...)
            name (str): The name of the card
        """
        self.c_type = c_type
        self.name = name

class Battlefield:
    def __init__ (self, deck_j_left, deck_j_right):
        self.end = False
        self.winner = -1
        self.life_j_left, self.life_j_right = 20
        self.can_cast_sorcery_left, self.can_cast_sorcery_right = False
        self.mana_by_crea_left, self.mana_by_crea_right = 0
        self.mana_used_left = 0
        self.mana_used_rights = 0
        self.board_j_left = []
        self.board_j_right = []
        self.creature_j_left = []
        self.creature_j_right = []
        self.deck_j_left = deck_j_left
        self.deck_j_right = deck_j_right
        self.hand_j_left, self.hand_j_right = []
        self.gravyard_j_left, self.gravyard_j_right = []
        self.nb_land_in_play_left, self.nb_land_in_play_right = 0
        self.hand_size_left, self.hand_size_right = 7
        self.upkeep_left, self.upkeep_right = []
        self.combat_left, self.combat_right = []
        self.step = ["attack", "main", "block", "damage", "end step", "upkeep"]
        self.trigger_effect_attack_left, self.trigger_effect_attack_right = []
        self.trigger_effect_damage_left, self.trigger_effect_damage_right = []
        self.trigger_effect_upkeep_left, self.trigger_effect_upkeep_right = []
        self.trigger_effect_end_step_left, self.trigger_effect_end_step_right = []
    def is_playable (self, left, card):
    """A function to calcul if the card card is actually playable or not.

    Args:
        left (bool): To know which player want to play (True = left)
        card (Card): The card to know if it playable

    Returns:
        bool : If the card is playable then True
    """
        if left:
            for symbol in card.cost:
                if (self.mana_by_crea_left + self.nb_land_in_play_left - self.mana_used_left) <= card.cost[symbol]:
                    return False
                else:
                    return True
        for symbol in card.cost: #here, this isn't the left player who want to play
            if (self.mana_by_crea_left + self.nb_land_in_play_left - self.mana_used_left) <= card.cost[symbol]:
                return False
            else:
                return True
        return False
        
    def draw (self, left, n):
        """A function to draw n card.

        Args:
            left (bool): if it's the left player who need to draw then True
            n (int)): the number of card to draw
        """
        if left:
            if len(deck_j_left < n): #to check if the player can draw (if not he loses the game)
                win_the_game(False)
            for i in range (n):
                hand_j_left.append(deck_j_left.pop())
            return
        if len(deck_j_right < n): #to check if the player can draw (if not he loses the game)
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
                    self.nb_land_in_play_left +=1
                    self.hand_j_left.remove(c)
                    return
        for c in self.hand_j_right:
            if c.c_type == "land":
                self.nb_land_in_play_right +=1
                self.hand_j_right.remove(c)
                return
    def possible_attacking_creature(self, left):
        tab = []
        if left:
            for crea in board_j_left:
                if not(crea.summoning_sickness or crea.is_tap):
                    tab.append(crea)
        else:
            for crea in board_j_right:
                if not(crea.summoning_sickness or crea.is_tap):
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
            self.mana_used_left = 0
            for crea in self.creature_j_left:
                if len(crea.mana_producers) > 0:
                    if crea.summoning_sickness:
                        self.mana_by_crea_left += 1
                crea.summoning_sickness = False
                if crea.can_untap:
                    crea.is_tap = False
            return
        self.mana_used_right = 0
        for crea in self.creature_j_right:
            if len(crea.mana_producers) > 0:
                if crea.summoning_sickness:
                    self.mana_by_crea_right += 1
            crea.summoning_sickness = False
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
    def play_a_card (self, card, left):
        mana_needed = 0
        for symbol in card.cost:
            mana_needed += card.cost[symbol]
        if left:
            self.mana_used_left += mana_needed
            hand_j_left.remove(card)
            if self.mana_used_left > self.nb_land_in_play_left:
                #to do
                pass
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

