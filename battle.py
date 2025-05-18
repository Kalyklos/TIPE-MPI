"""In this module, all int are positive. The goal of this module is to implement function to create and administrate a battlefield.  """

from random import *
seed()

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
        """Executes the attack effects 'boost by the number of lands' for a creature on the battlefield.

    Args:
        crea (Creature): The creature that is attacking.
        actual_battlefield (Battlefield): The current state of the battlefield.
    """

        for b in self.attacking:
            if b:
                self.land_boost (self, crea, actual_battlefield)
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
        """Pay the Delver cost by distributing +1/+1 counters to Delver creatures based on available mana.

    Args:
        left (bool): Indicates which player's Delver creatures to affect (True for left player).
        actual_battlefield (Battlefield): The current state of the battlefield.

    The function cycles through Delver creatures, adding a +1/+1 counter for every 4 mana available,
    until less than 4 mana remains.
    """

        if left:
            mana_remaining = actual_battlefield.nb_land_in_play_left - actual_battlefield.mana_used_left #au pire 25 donc 6 tour de boucle while
            if mana_remaining > 3:
                l_delver = [] #au maximum de taille 3
                for crea in actual_battlefield.creature_j_left:
                    if crea.delver:
                        l_delver.append (crea)
                cpt = 0
                while mana_remaining > 3:
                    self.add_counter_crea (l_delver[cpt])
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
                self.add_counter_crea (l_delver[cpt])
                cpt = (cpt + 1) % len (l_delver)
                mana_remaining -= 4
        return
    def damage (self, target, ennemy):
        """Inflicts damage to the enemy creature by reducing its actual life based on the target's actual strength.

    Args:
        target (Creature): The creature dealing the damage.
        ennemy (Creature): The creature receiving the damage.
    """

        ennemy.actual_life -= target.actual_strength
        return
    def add_baloth (self, crea_entering, left, actual_battlefield):
        """Assigns the 'baloth' property to the entering creature and adds +2/+2 counters to existing Baloth creatures.

    Args:
        crea_entering (Creature): The creature entering the battlefield.
        left (bool): Indicates whether the creature belongs to the left player (True) or right player (False).
        actual_battlefield (Battlefield): The current state of the battlefield.
    """

        crea_entering.baloth = False
        if left:
            for crea in actual_battlefield.creature_j_left:
                if crea.baloth:
                    self.add_counter_crea(crea, 2)
        else:
            for crea in actual_battlefield.creature_j_left:
                if crea.baloth:
                    self.add_counter_crea(crea, 2)
        crea_entering.baloth = True
        return
    def draw_by_enchant (self, actual_battlefield, left):
        """Draw one card if the player has a creature with power 4 or more.

        Args:
            actual_battlefield (Battlefield): the battlefield to draw from
            left (bool): the player who want to draw (True -> left)
        """
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
        """Init of the Enchantment class

        Args:
            effect (Effect): effect of the enchantment (upkeep, endstep, entering, dying)
            cost (int): cost of the enchantment (in mana)
        """
        self.effect = effect
        self.actual_battlefield = None
        self.cost = cost
        self.type = "enchantment"
class Creature:
    def __init__ (self, strength, life, keywords, effect, cost):
        """Init of the creature class

        Args:
            strength (int): strength of the creature
            life (int): toughness of the creature
            keywords (tab of str): keywords of the creature (like Trample, Flying...)
            effect (Effect): effect of the creature (upkeep, endstep, entering, dying)
            cost (int): cost of the creature (in mana)   """
        self.type = "creature"
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
        self.type = "land"
        self.color = color
        self.cost = 1000 #to don't play a land as a spell
class Instant:
    def __init__(self, untap, nb_counter, trample, cost):
        """Init of the instant function

        Args:
            untap (bool): To know if the instant untap the target(s) (True -> Yes)
            nb_counter_plus (int): The number of counter +1/+1 to put on the target(s)
            cost (int): The cost of the instant (in mana)
            trample (bool): To know if the instant give the trample ability to the target(s) (True -> Yes)
        """
        self.effect = Effect([],[],[],[],[])
        self.type = "instant"
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
        self.winner = -1
        self.life_j_left = 20
        self.life_j_right = 20
        self.can_cast_sorcery_left = self.can_cast_sorcery_right = False
        self.mana_used_left = 0
        self.mana_used_right = 0
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
            mana_creature = []
            for crea in self.creature_j_left:
                    if crea.mana_producers > 0 and (not crea.summoning_sickness) and (not crea.is_tap):
                        mana_creature.append(crea)
            return len(mana_creature) + self.nb_land_in_play_left - self.mana_used_left - card.cost >= 0
        mana_creature = []
        for crea in self.creature_j_right:
                if crea.mana_producers > 0 and (not crea.summoning_sickness) and (not crea.is_tap):
                    mana_creature.append(crea)
        return len(mana_creature) + self.nb_land_in_play_right - self.mana_used_right - card.cost >= 0
        
    def draw (self, left, n):
        """A function to draw n card.

        Args:
            left (bool): the player who need to draw (True -> left)
            n (int)): the number of card to draw
        """
        if left:
            if (len(self.deck_j_left) < n): #to check if the player can draw (if not he loses the game)
                self.winner = 0
                return
            for i in range (n):
                self.hand_j_left.append(self.deck_j_left.pop())
            return
        if (len(self.deck_j_right) < n): #to check if the player can draw (if not he loses the game)
                self.winner = 1
                return
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
                crea.summoning_sickness = False
                if crea.can_untap:
                    crea.is_tap = False
            return
        self.mana_used_right = 0
        for crea in self.creature_j_right:
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
        for crea in self.creature_j_left:
            crea.actual_life = crea.life
            crea.actual_strength = crea.strength
        for crea in self.creature_j_right:
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
                self.hand_j_left.pop()
            return
        shuffle (self.hand_j_right)
        for i in range (n):
            self.hand_j_right.pop()

    def end_step (self, left):
        """a function to do the end step phase, whoes need the discard and clean_step functions

        Args:
            left (bool): the player who is in his end step (True -> left)

        Returns:
            None: the function doesn't return anything, the return is here only to stop the function
        """
        if left:
            for eff in self.trigger_effect_end_step_left:
                eff.trigger ()
            if (self.hand_size_left - len(self.hand_j_left)) < 0:
                self.discard (self, left, (len(self.hand_j_left) - self.hand_size_left))
            return self.clean_step ()
        for eff in self.trigger_effect_end_step_right:
            eff.trigger ()
        if (self.hand_size_right - len(self.hand_j_right)) < 0:
            self.discard (self, left, (len(self.hand_j_right) - self.hand_size_right))
        return self.clean_step ()      

    def play_land (self, left):
        """a function to play a single land

        Args:
            left (_type_): the player who want to play a land (True -> left)
        """
        if left:
            for c in self.hand_j_left:
                if c.type == "land":
                    self.nb_land_in_play_left +=1
                    self.hand_j_left.remove(c)
                    return                       #the return stop the function in order to not play another land
        for c in self.hand_j_right:
            if c.type == "land":
                self.nb_land_in_play_right +=1
                self.hand_j_right.remove(c)
                return                           #the return stop the function in order to not play another land
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
            self.winner = 0
            return 0
        if self.life_j_right < 1:
            self.winner = 1
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
        crea.owner = False
        self.creature_j_right.append(crea)
        return
    def play_a_card (self, card, left):
        """a function to play the card card, THE CARD MUST BE PLAYABLE

        Args:
            card : a magic card from a class
            left (bool): to know which player want to play (True -> left)
        """
        assert self.is_playable(left, card), "The card is not playable"
        if left:
            remaining = self.nb_land_in_play_left - self.mana_used_left - card.cost
            if remaining < 0:
                mana_creature = []
                for crea in self.creature_j_left:
                    if crea.mana_producers > 0 and not crea.summoning_sickness and not crea.is_tap:
                        mana_creature.append(crea)
                for i in range (-remaining):
                    mana_creature[i].is_tap = True
            self.hand_j_left.remove(card)
            if card.type == "creature":
                self.new_creature(left, card)
            elif card.type == "enchantment":
                self.enchant_j_left.append(card)
            card.effect.execute_enter()
            return                
        remaining = self.nb_land_in_play_right - self.mana_used_right - card.cost
        if remaining < 0:
            mana_creature = []
            for crea in self.creature_j_right:
                if crea.mana_producers > 0 and not crea.summoning_sickness and not crea.is_tap:
                    mana_creature.append(crea)
            for i in range (-remaining):
                mana_creature[i].is_tap = True
        self.hand_j_right.remove(card)
        if card.type == "creature":
                self.new_creature(left, card)
        elif card.type == "enchantment":
            self.enchant_j_left.append(card)
        card.effect.execute_enter()
        return 
    
    def game_begin (self):
        """a function to init the game
        """
        shuffle(self.deck_j_left)
        shuffle(self.deck_j_right)
        self.draw (True, 6)
        self.draw (False, 7)
        self.winner = -1
        return
    def new_turn (self, left):
        """a function to begin a new turn

        Args: 
            left (bool): to know which player is begining his turn (True -> left)
        """
        if left:
            for i in self.upkeep_left:
                self.eff_card(i, left)
        else:
            for i in self.upkeep_right:
                self.eff_card(i, left)
        self.draw(left, 1)
        self.untap (left)
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
            if self.attacking_creature[crea] == []:
                if crea.owner:
                    self.actual_battlefield.life_j_right -= crea.actual_strength
                else:
                    self.actual_battlefield.life_j_left -= crea.actual_strength
            else:
                crea.actual_life -= self.attacking_creature[crea].actual_strength
                self.attacking_creature[crea].actual_life -= crea.actual_strength
        self.actual_battlefield.is_finish ()
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
        self.actual_battlefield.is_finish ()
    def finish (self):
        self.actual_battlefield.is_finish()

def copy_battlefield (battlefield):
    """A function to copy a battlefield

    Args:
        battlefield (Battlefield): the battlefield to copy
    """
    new_battlefield = Battlefield(battlefield.deck_j_left.copy(), battlefield.deck_j_right.copy())
    new_battlefield.creature_j_left = []
    new_battlefield.creature_j_right = []
    new_battlefield.enchant_j_left = []
    new_battlefield.enchant_j_right = []
    new_battlefield.hand_j_left = battlefield.hand_j_left.copy()
    new_battlefield.hand_j_right = battlefield.hand_j_right.copy()
    new_battlefield.gravyard_j_left = battlefield.gravyard_j_left.copy()
    new_battlefield.gravyard_j_right = battlefield.gravyard_j_right.copy()
    new_battlefield.nb_land_in_play_left = battlefield.nb_land_in_play_left
    new_battlefield.nb_land_in_play_right = battlefield.nb_land_in_play_right
    new_battlefield.life_j_left = battlefield.life_j_left
    new_battlefield.life_j_right = battlefield.life_j_right
    new_battlefield.mana_used_left = battlefield.mana_used_left
    new_battlefield.mana_used_right = battlefield.mana_used_right
    new_battlefield.can_cast_sorcery_left = battlefield.can_cast_sorcery_left
    new_battlefield.can_cast_sorcery_right = battlefield.can_cast_sorcery_right
    new_battlefield.hand_size_left = battlefield.hand_size_left
    new_battlefield.hand_size_right = battlefield.hand_size_right
    new_battlefield.upkeep_left = battlefield.upkeep_left.copy()
    new_battlefield.upkeep_right = battlefield.upkeep_right.copy()
    new_battlefield.combat_left = battlefield.combat_left.copy()
    new_battlefield.combat_right = battlefield.combat_right.copy()
    new_battlefield.trigger_effect_attack_left = battlefield.trigger_effect_attack_left.copy()
    new_battlefield.trigger_effect_attack_right = battlefield.trigger_effect_attack_right.copy()
    new_battlefield.trigger_effect_damage_left = battlefield.trigger_effect_damage_left.copy()
    new_battlefield.trigger_effect_damage_right = battlefield.trigger_effect_damage_right.copy()
    new_battlefield.trigger_effect_upkeep_left = battlefield.trigger_effect_upkeep_left.copy()
    new_battlefield.trigger_effect_upkeep_right = battlefield.trigger_effect_upkeep_right.copy()
    new_battlefield.trigger_effect_end_step_left = battlefield.trigger_effect_end_step_left.copy()
    new_battlefield.trigger_effect_end_step_right = battlefield.trigger_effect_end_step_right.copy()
    for crea in battlefield.creature_j_left:
        new_crea = Creature(crea.strength, crea.life, crea.keywords.copy(), crea.effect, crea.cost)
        new_crea.actual_life = crea.actual_life
        new_crea.actual_strength = crea.actual_strength
        new_crea.is_tap = crea.is_tap
        new_crea.can_untap = crea.can_untap
        new_crea.owner = True
        new_crea.summoning_sickness = crea.summoning_sickness
        new_crea.mana_producers = crea.mana_producers
        new_battlefield.creature_j_left.append(new_crea)
    for crea in battlefield.creature_j_right:
        new_crea = Creature(crea.strength, crea.life, crea.keywords.copy(), crea.effect, crea.cost)
        new_crea.actual_life = crea.actual_life
        new_crea.actual_strength = crea.actual_strength
        new_crea.is_tap = crea.is_tap
        new_crea.can_untap = crea.can_untap
        new_crea.owner = False
        new_crea.summoning_sickness = crea.summoning_sickness
        new_crea.mana_producers = crea.mana_producers
        new_battlefield.creature_j_right.append(new_crea)
    for enchant in battlefield.enchant_j_left:
        new_enchant = Enchantment(enchant.effect, enchant.cost)
        new_enchant.actual_battlefield = new_battlefield
        new_battlefield.enchant_j_left.append(new_enchant)
    for enchant in battlefield.enchant_j_right:
        new_enchant = Enchantment(enchant.effect, enchant.cost)
        new_enchant.actual_battlefield = new_battlefield
        new_battlefield.enchant_j_right.append(new_enchant)
    return new_battlefield




""" Définition de toutes les cartes utilisés.
"""
data_base = {}
data_base ["Forest"] = Land("green")
data_base ["Island"] = Land("blue")
data_base ["Mountain"] = Land("red")
data_base ["Swamp"] = Land("black")
data_base ["Plain"] = Land("white")
data_base ["Gigantosorus"] = Creature(10,10,[],Effect([],[],[],[],[]),5)
data_base ["Umbling Baloth"] = Creature(4,4,[],Effect([],[],[],[],[]),4)
data_base ["Sentinel Spider"] = Creature(4,4,["vigilance", "reach"],Effect([],[],[],[],[]),5)
data_base ["Woodland Mystic"] = Creature(1,1,[],Effect([],[],[],[],[]),2)
data_base ["Woodland Mystic"].mana_producers = 1
data_base ["Ilysian Caryatid"] = Creature(1,1,[],Effect([],[],[],[],[]),2)
data_base ["Ilysian Caryatid"].mana_producers = 1
data_base ["Stony Strength"] = Instant(True, 1, False,1)
data_base ["Rabid Bite"] = Instant(False, 0, False,2)
data_base ["Epic Proportions"] = Instant(False, 5, True,6)
data_base ["Wildwood Patrol"] = Creature(4,2,["trample"], Effect([],[],[],[],[]),3)
data_base ["Affectionate Indrik"] = Creature(4,4,[], Effect([],[],[True],[],[]),6)
data_base ["Rampaging Brontodon"] = Creature(7,7, ["trample"], Effect([],[],[],[],[True]),7)
data_base ["Colossal Majesty"] = Enchantment(Effect([True],[],[],[],[]),3)
data_base ["Baloth Packhunter"] = Creature(3,3,["trample"],Effect([],[],[False, True],[],[]),4)
data_base ["Baloth Packhunter"].baloth = True
data_base ["Jungle Delver"] = Creature(1,1,[],Effect([],[True],[],[],[]),1)

mono_green = [] #check why their are only 56 cards in this deck
for i in range (4):
    mono_green.append(data_base["Gigantosorus"])
    mono_green.append(data_base["Baloth Packhunter"])
    mono_green.append(data_base["Ilysian Caryatid"])
for i in range (2):
    mono_green.append(data_base["Umbling Baloth"])
    mono_green.append(data_base["Woodland Mystic"])
    mono_green.append(data_base["Sentinel Spider"])
    mono_green.append(data_base["Wildwood Patrol"])
    mono_green.append(data_base["Affectionate Indrik"])
    mono_green.append(data_base["Colossal Majesty"])
    mono_green.append(data_base["Stony Strength"])
for i in range (25):
    mono_green.append(data_base["Forest"])
for i in range (3):
    mono_green.append(data_base["Rabid Bite"])
mono_green.append(data_base["Epic Proportions"])
mono_green.append(data_base["Rampaging Brontodon"])