"""In this module, all int are positive. The goal of this module is to implement function to create and administrate a battlefield.  """

from random import *
seed() #to give something that seem more random to use than only the random function (cause the random is hardcode)
colors = ["green", "red", "blue", "white", "black", "colorless"]
types = ["creature","artifact", "land", "enchantement", "instant", "sorcery"]
keywords = ["vigilance", "trample", "reach", "flying", "deathtouch", "unblockable"] #actually there are 173 so... it can be long

class Effect:
    def __init__ (self, upkeep_t, endstep_t, entering, dying, attacking):
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
        self.attacking = attacking
        self.target = None
    def execute_enter (self):
        pass
    def execute_end (self):
        pass
    def execute_dying (self):
        pass
    def execute_up (self):
        pass
    def execute_att (self, crea, actual_battlefield):
        for b in self.attacking:
            if b:
                land_boost (self, crea, actual_battlefield)
        return
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
    def delver_pay (self, left, actual_battlefield):
        if left:
            mana_remaining = actual_battlefield.nb_land_in_play_left - actual_battlefield.mana_used_left #au pire 25 donc 6 tour de boucle while
            if mana_remaining > 3:
                l_delver = [] #au maximum de taille 3
                for crea in actual_battlefield.creature_j_left:
                    if crea.delver:
                        l_delver.append (crea)
                cpt = 0
                while mana_remaining > 3:
                    add_counter_crea (l_delver[cpt])
                    cpt = (cpt + 1) % len (l_delver)
                    mana_remaining -= 4
            return
        mana_remaining = actual_battlefield.nb_land_in_play_right - actual_battlefield.mana_used_right #au pire 25 donc 6 tour de boucle while
        if mana_remaining > 3:
            l_delver = [] #au maximum de taille 3
            for crea in actual_battlefield.creature_j_right:
                if crea.delver:
                    l_delver.append (crea)
            cpt = 0
            while mana_remaining > 3:
                add_counter_crea (l_delver[cpt])
                cpt = (cpt + 1) % len (l_delver)
                mana_remaining -= 4
        return
    def damage (self, target, ennemy):
        ennemy.actual_life -= target.actual_strength
        return
    def add_baloth (self, crea_entering, left, actual_battlefield):
        crea_entering.baloth = False
        if left:
            for crea in actual_battlefield.creature_j_left:
                if crea.baloth:
                    add_counter_crea(crea, 2)
        else:
            for crea in actual_battlefield.creature_j_left:
                if crea.baloth:
                    add_counter_crea(crea, 2)
        crea_entering.baloth = True
        return
    def draw_by_enchant (self, actual_battlefield, left):
        possede_prerequis = False
        if left:
            for crea in actual_battlefield.creature_j_left:
                if crea.actual_strength >= 4:
                    possede_prerequis = True
        else:
            for crea in actual_battlefield.creature_j_right:
                if crea.actual_strength >= 4:
                    possede_prerequis = True
        if possede_prerequis:
            actual_battlefield.draw(left, 1)
        return
    def land_boost (self, crea, actual_battlefield):
        if crea.owner:
            crea.actual_life += actual_battlefield.nb_land_in_play_left
            crea.actual_strength += actual_battlefield.nb_land_in_play_left
        else:
            crea.actual_life += actual_battlefield.nb_land_in_play_right
            crea.actual_strength += actual_battlefield.nb_land_in_play_right
class Enchantment:
    def __init__ (self, effect, cost):
        self.effect = effect
        self.actual_battlefield = None
        self.cost = cost
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
        self.baloth = False
        self.delver = False

class Land:
    def __init__ (self, color):
        """init of the Land class

        Args:
            color (str): The color of mana that produce the land
        """
        self.color = color
        self.cost = {}
class Instant:
    def __init__(self, untap, nb_counter, trample, cost):
        """Init of the instant function

        Args:
            untap (bool): To know if the instant untap the target(s) (True -> Yes)
            nb_counter_plus (int): The number of counter +1/+1 to put on the target(s)
            cost (dict): dictionnaire of colors and the nombers of mana of that type in their cost (ex : "Green" : 5)
        """
        self.untap = untap
        self.nb_counter = nb_counter
        self.target = None
        self.cost = cost
        self.trample = trample
    def execute (self, target, target_to_damage):
        """A function to do the effect of an instant
    
        Args:
            target (Creature) : The creature that's the main target of the spell
            target_to_damage (Creature) : The creature to deals damage (if the spell said that else None)
        """
        if self.untap:
            target.is_tap = False
        target.actual_life += self.nb_counter
        target.actual_strength += self.nb_counter
        target.strength += self.nb_counter
        target.life += self.nb_counter
        if self.trample:
            if not ("trample" in target.keywords):
                target.keywords.append("trample")
        if target_to_damage != None:
            target_to_damage.actual_life -= target.actual_strength


class Battlefield:
    def __init__ (self, deck_j_left, deck_j_right):
        """Init of the Battlefield class

        Args:
            deck_j_left (dict): a magic deck
            deck_j_right (dict): a magic deck
        """
        self.end = False
        self.winner = -1
        self.life_j_left = self.life_j_right = 20
        self.can_cast_sorcery_left = self.can_cast_sorcery_right = False
        self.mana_by_crea_left = self.mana_by_crea_right = 0
        self.mana_used_left = 0
        self.mana_used_rights = 0
        self.creature_j_left = []
        self.creature_j_right = []
        self.enchant_j_right = []
        self.enchant_j_left = []
        self.deck_j_left = deck_j_left
        self.deck_j_right = deck_j_right
        self.hand_j_left = []
        self.hand_j_right = []
        self.gravyard_j_left = []
        self.gravyard_j_right = []
        self.nb_land_in_play_left = self.nb_land_in_play_right = 0
        self.hand_size_left = self.hand_size_right = 7
        self.upkeep_left =[]
        self.upkeep_right = []
        self.combat_left =[]
        self.combat_right = []
        self.step = ["attack", "main", "block", "damage", "end step", "upkeep"]
        self.trigger_effect_attack_left = []
        self.trigger_effect_attack_right = []
        self.trigger_effect_damage_left = []
        self.trigger_effect_damage_right = []
        self.trigger_effect_upkeep_left = []
        self.trigger_effect_upkeep_right = []
        self.trigger_effect_end_step_left = []
        self.trigger_effect_end_step_right = []
    def is_playable (self, left, card):
        """A function to calcul if the card card is actually playable or not.

        Args:
            left (bool): To know which player want to play (True -> left)
            card (Card): The card to know if it playable

        Returns:
            bool : If the card is playable : True
        """
        if left:
            for symbol in data_base[card.name].cost:
                if (self.mana_by_crea_left + self.nb_land_in_play_left - self.mana_used_left) <= data_base[card.name].cost[symbol]:
                    return False
                else:
                    return True
        for symbol in data_base[card.name].cost: #here, this isn't the left player who want to play (python indentation)
            if (self.mana_by_crea_left + self.nb_land_in_play_left - self.mana_used_left) <= data_base[card.name].cost[symbol]:
                return False
            else:
                return True
        return False
        
    def draw (self, left, n):
        """A function to draw n card.

        Args:
            left (bool): the player who need to draw (True -> left)
            n (int)): the number of card to draw
        """
        if left:
            if (len(self.deck_j_left) < n): #to check if the player can draw (if not he loses the game)
                self.winner = 0
            for i in range (n):
                self.hand_j_left.append(self.deck_j_left.pop())
            return
        if (len(self.deck_j_right) < n): #to check if the player can draw (if not he loses the game)
                self.winner = 1
        for i in range (n):
            self.hand_j_right.append(self.deck_j_right.pop())
        return
    def untap_step (self, left):
        """a function to do the untap step

    Args:
            left (bool): to know which player in his untap_step (True -> left)
        """
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
        
    def upkeep (self, left):
        """a function to do the upkeep step (untap, upkeep triggers, draw)

        Args:
            left (bool): the player who is in upkeep phase (True -> left)
        """
        self.untap_step (left)
        if left:
            for eff in self.trigger_effect_upkeep_left:
                eff.trigger()
        else:
            for eff in self.trigger_effect_upkeep_right:
                eff.trigger()
        self.draw (left, 1)

    def clean_step (self):
        """a function tu od the clean_step (end of the endstep)
        """
        for crea in creature_j_left:
            crea.actual_life = crea.life
            crea.actual_strength = crea.strength
        for crea in creature_j_right:
            crea.actual_life = crea.life
            crea.actual_strength = crea.strength
        return

    def discard (self, left, n):
        """a function to discard cards (use in the end_step function)

        Args:
            left (bool): the player who need to discard (True -> left)
            n (int): the number of card to discard
        """
        if left:
            shuffle (self.hand_j_left)
            for i in range (n):
                hand_j_left.pop()
            return
        shuffle (self.hand_j_right)
        for i in range (n):
            hand_j_right.pop()

    def end_step (self, left):
        """a function to do the end step phase, whoes need the discard and clean_step functions

        Args:
            left (bool): the player who is in his end step (True -> left)

        Returns:
            None: the function doesn't return anything, the return is here only to stop the function
        """
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

    def play_land (self, left):
        """a function to play a single land

        Args:
            left (_type_): the player who want to play a land (True -> left)
        """
        if left:
            for c in self.hand_j_left:
                if c.c_type == "land":
                    self.nb_land_in_play_left +=1
                    self.hand_j_left.remove(c)
                    return                       #the return stop the funtcion in order to not play another land
        for c in self.hand_j_right:
            if c.c_type == "land":
                self.nb_land_in_play_right +=1
                self.hand_j_right.remove(c)
                return                           #the return stop the funtcion in order to not play another land
    def possible_attacking_creature(self, left):
        """a function to know which creature are able to attack

        Args:
            left (bool): the player who want to attack (True -> left)

        Returns:
            tab: a python array with the creature ble to attack for the chosen player
        """
        tab = []
        if left:
            for crea in self.creature_j_left:
                if not(crea.summoning_sickness or crea.is_tap):
                    tab.append(crea)
        else:
            for crea in self.creature_j_right:
                if not(crea.summoning_sickness or crea.is_tap):
                    tab.append(crea)
        return tab
    def is_finish (self):
        """a function to know if the game is finished

        Returns:
            int: 0 if the right player have win, 1 if the right player have win, else -1
        """
        if self.life_j_left < 1:
            return 0
        if self.life_j_right < 1:
            return 1
        return -1
    def main_phase (self, left):
        """a function to do a main phase

        Args:
            left (bool): to know which player is in his main phase (True -> left)
        """
        if left:
            self.can_cast_sorcery_left = True
        else:
            self.can_cast_sorcery_right = True
    def new_creature (self, left, crea):
        """a function to add a creature to a board

        Args:
            left (bool): the player who want to add a creature (True -> left)
            crea (Creature): the creature to add
        """
        if left:
            self.creature_j_left.append(crea)
            return
        self.creature_j_right.append(crea)
        return
    def play_a_card (self, card, left):
        """a function to play the card card, the card to play is supposed playable

        Args:
            card (Card): a magic card from the Card class
            left (bool): to know which player want to play (True -> left)
        """
        mana_needed = 0
        for symbol in card.cost:
            mana_needed += card.cost[symbol]
        if left:
            remaining_by_land = self.nb_land_in_play_left - mana_needed
            if remaining_by_land < 0:
                mana_creature = []
                for crea in self.creature_j_left:
                    if crea.mana_producers > 0 and not crea.summoning_sickness and not crea.is_tap:
                        mana_creature.append[crea]
                for i in range (-remaining_by_land):
                    mana_creature[i].is_tap = True
            hand_j_left.remove(card)
            eff_etb (card, left)
            return                
        remaining_by_land = self.nb_land_in_play_right - mana_needed
        if remaining_by_land < 0:
            mana_creature = []
            for crea in self.creature_j_right:
                if crea.mana_producers > 0 and not crea.summoning_sickness and not crea.is_tap:
                    mana_creature.append[crea]
            for i in range (-remaining_by_land):
                mana_creature[i].is_tap = True
        hand_j_right.remove(card)
        eff_etb (card, left)
        return
    
    def game_begin (self):
        """a function to init the game
        """
        shuffle(self.deck_j_left)
        shuffle(self.deck_j_right)
        self.draw (True, 7)
        self.draw (False, 7)
        return
    def new_turn (self, left):
        """a function to begin a new turn

        Args: 
            left (bool): to know which player is begining his turn (True -> left)
        """
        if left:
            for i in self.upkeep_left:
                eff_card(i, left)
        else:
            for i in self.upkeep_right:
                eff_card(i, left)
        draw(left, 1)
        untap (left)
        return
    def dying_creature (self):
        """a function to update the python list tab, adding the died creature

        Args:
            tab_left (tab): a python list initially empty
            tab_right (tab): a python list initially empty
        """
        for i in range (len(self.creature_j_left)):
            if self.creature_j_left[i].actual_life < 1:
                self.creature_j_left.pop([i])
        for i in range (len(self.creature_j_right)):
            if self.creature_j_right[i].actual_life < 1:
                self.creature_j_right.pop([i])
        return

class Combat_phase:
    def __init__ (self, actual_battlefield):
        """the init of the Combat_phase class

        Args:
            actual_battlefield (Battlefield): the battlefield to manage the combat phase
        """
        self.actual_battlefield = actual_battlefield
        self.attacking_creature = {}
        self.died_creature_left = []
        self.died_creature_right = []
    def reset (self):
        """a function to reset the combat phase
        """
        self.attacking_creature = {}
        self.died_creature = []
    def attack_phase (self, attacking_creature_tab):
        """a function to declare the attacking creature

        Args:
            attacking_creature_tab (tab): a python tab to declare the attacking creature
        """
        for crea in attacking_creature_tab:
            self.attacking_creature[crea] = []
    def assign_damage (self):
        """a function to assign the damage after the block phase
        """
        for crea in self.attacking_creature.keys():
            if attacking_creature[crea] == []:
                if crea.owner:
                    self.actual_battlefield.life_j_right -= crea.actual_strength
                else:
                    self.actual_battlefield.life_j_right -= crea.actual_strength
            else:
                crea.actual_life -= self.attacking_creature[crea].actual_strength
                self.attacking_creature[crea].actual_life -= crea.actual_strength
        self.actual_battlefield.dying_creature ()
    def died_effect (self):
        """a function to execute the died effect
        """
        for crea in self.died_creature_left:
            c = self.died_creature.pop()
            self.actual_battlefield.creature_j_left.remove(c)
            c.died_effect()
        for crea in self.died_creature_right:
            c = self.died_creature.pop()
            self.actual_battlefield.creature_j_right.remove(c)
            c.died_effect()
        
    def finish (self):
        """a function to actualise if wheather or not the duel is finished
        """
        if self.actual_battlefield.is_finish == -1:
            self.actual_battlefield.end = True

""" Définition de toutes les cartes utilisé.
"""
data_base = {}
data_base ["Forest"] = Land("green")
data_base ["Island"] = Land("blue")
data_base ["Mountain"] = Land("red")
data_base ["Swamp"] = Land("black")
data_base ["Plain"] = Land("white")
data_base ["Gigantosorus"] = Creature(10,10,[],[],{"green" : 5})
data_base ["Umbling Baloth"] = Creature(4,4,[],[],{"green" : 4})
data_base ["Sentinel Spider"] = Creature(4,4,["vigilance", "reach"],[],{"green" : 5})
data_base ["Woodland Mystic"] = Creature(1,1,[],[],{"green" : 2})
data_base ["Woodland Mystic"].mana_producers = 1
data_base ["Ilysian Caryatid"] = Creature(1,1,[],[],{"green" : 2})
data_base ["Ilysian Caryatid"].mana_producers = 1
data_base ["Stony Strength"] = Instant(True, 1, False, {"green" : 1})
data_base ["Rabid Bite"] = Instant(False, 0, False, {"green" : 2})
data_base ["Epic Proportions"] = Instant(False, 5, True, {"green" : 6})
data_base ["Wildwood Patrol"] = Creature(4,2,["trample"], [], {"green" : 3})
data_base ["Affectionate Indrik"] = Creature(4,4,[], [Effect([],[],[True],[],[])], {"green" : 6})
data_base ["Rampaging Brontodon"] = Creature(7,7, ["trample"], [Effect([],[],[],[],[True])], {"green" : 7})
data_base ["Colossal Majesty"] = Enchantment([Effect([True],[],[],[],[])], {"green" : 3})
data_base ["Baloth Packhunter"] = Creature(3,3,["trample"],[Effect([],[],[False, True],[],[])], {"green" : 4})
data_base ["Baloth Packhunter"].baloth = True
data_base ["Jungle Delver"] = Creature(1,1,[],[Effect([],[True],[],[],[])],{"green" : 1})