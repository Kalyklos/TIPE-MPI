from battle import *
from random import *

class S_algo_att:
    def __init__ (self, left, battlefield_play):
        """
        Init of the S_algo_att class
        Args:
            left (bool): The player who use this algorithm (True -> left)
            battlefield_play (Battlefield): The battlefield of the game
        """
        self.left = left
        self.battlefield_play = battlefield_play
    def can_play (self, have_play_land):
        if not have_play_land:
            self.battlefield_play.play_land(self.left)
        if self.left:
            n = len (self.battlefield_play.hand_j_left)
            if n > 0:
                alea = randint(0, n-1)
                if self.battlefield_play.is_playable(self.left, self.battlefield_play.hand_j_left[alea]):
                    self.battlefield_play.play_a_card(self.battlefield_play.hand_j_left[alea], self.left)
                    return
                return
            return
        n = len (self.battlefield_play.hand_j_right)
        if n > 0:
            alea = randint(0, n-1)
            if self.battlefield_play.is_playable(self.left, self.battlefield_play.hand_j_right[alea]):
                self.battlefield_play.play_a_card(self.battlefield_play.hand_j_right[alea], self.left)
                return
            return
        return
    def combat (self):
        """
    Execute the combat phase.
    """
        com = Combat_phase (self.battlefield_play)
        com.reset()
        com.attack_phase(self.battlefield_play.possible_attacking_creature(self.left))
        com.assign_damage()
        com.finish()
        com.died_effect()
        com.finish()
        return
    def boost_target_crea (self, strength, life):
        """
        Boost a random creature in the board of the player who is playing,
        by adding the given strength and life.
        """
        if self.left:
            if len(self.battlefield_play.board_j_left) > 0:
                random.shuffle(self.battlefield_play.board_j_left)
                c = self.battlefield_play.board_j_left[0]
                c.strength += strength
                c.actual_strength += strength
                c.actual_life += life
                c.life += life
            return
        if len(self.battlefield_play.board_j_right) > 0:
            random.shuffle(self.battlefield_play.board_j_right)
            c = self.battlefield_play.board_j_right[0]
            c.strength += strength
            c.actual_strength += strength
            c.actual_life += life
            c.life += life
        return
class Random_algo_att:
    def __init__ (self, left, battlefield_play):
        """
        Init of the Random_algo_att class

        Args:
            left (bool): The player who use this algorithm (True -> left)
            battlefield_play (Battlefield): The battlefield of the game
        """
        self.left = left
        self.battlefield_play = battlefield_play
    def can_play (self, have_play_land):
        """
    Determines the playable cards for the current player and plays them.

    This function attempts to play all possible cards from the player's hand.
    It first plays a land card, then checks which cards are playable based on
    the available mana and adds them to the playable_card list. The function
    then shuffles the playable cards and plays each card, updating the list 
    of playable cards after each play. The process repeats until no more cards
    can be played.

    Returns:
        None
    """
        if not have_play_land:
            self.battlefield_play.play_land(self.left)
        playable_card = []
        if self.left:
            for c in self.battlefield_play.hand_j_left:
                if self.battlefield_play.is_playable(self.left, c):
                    playable_card.append(c)
        else:
            for c in self.battlefield_play.hand_j_right:
                if self.battlefield_play.is_playable(self.left, c):
                    playable_card.append(c)
        if len(playable_card) > 0:
            shuffle(playable_card)
            self.battlefield_play.play_a_card(playable_card.pop(), self.left)
            self.can_play(True)
        return
    def combat (self):
        """
    Execute the combat phase.
    """
        com = Combat_phase (self.battlefield_play)
        com.reset()
        com.attack_phase(self.battlefield_play.possible_attacking_creature(self.left))
        com.assign_damage()
        com.finish()
        com.died_effect()
        com.finish()
        return
    def boost_target_crea (self, strength, life):
        """
        Boost a random creature in the board of the player who is playing,
        by adding the given strength and life.
        """
        if self.left:
            if len(self.battlefield_play.board_j_left) > 0:
                random.shuffle(self.battlefield_play.board_j_left)
                c = self.battlefield_play.board_j_left[0]
                c.strength += strength
                c.actual_strength += strength
                c.actual_life += life
                c.life += life
            return
        if len(self.battlefield_play.board_j_right) > 0:
            random.shuffle(self.battlefield_play.board_j_right)
            c = self.battlefield_play.board_j_right[0]
            c.strength += strength
            c.actual_strength += strength
            c.actual_life += life
            c.life += life
        return
class Opti_algo_att:
    def __init__ (self, left, battlefield_play):
        """
        Init of the Random_algo_att class

        Args:
            left (bool): The player who use this algorithm (True -> left)
            battlefield_play (Battlefield): The battlefield of the game
        """
        self.left = left
        self.battlefield_play = battlefield_play
    def can_play (self, have_play_land):
        
        if not have_play_land:
            self.battlefield_play.play_land(self.left)
        fake_battlefield = copy_battlefield(self.battlefield_play)
        cards = []
        playable = False
        if self.left:
            for c in self.battlefield_play.hand_j_left:
                if self.battlefield_play.is_playable(self.left, c):
                    playable = True
                    fake_battlefield.play_a_card(c, self.left)
                    cards.append(fake_battlefield.nb_land_in_play_left - fake_battlefield.mana_used_left - c.cost)
                    fake_battlefield = copy_battlefield(self.battlefield_play)
                else:
                    cards.append(1000)
            if playable:
                min_card = min(cards)
                index = cards.index(min_card)
                self.battlefield_play.play_a_card(self.battlefield_play.hand_j_left[index], self.left)
        else:
            mana_creature = []
            for crea in self.battlefield_play.creature_j_right:
                        if crea.mana_producers > 0 and not crea.summoning_sickness and not crea.is_tap:
                            mana_creature.append(crea)
            for c in self.battlefield_play.hand_j_right:
                if self.battlefield_play.is_playable(self.left, c):
                    playable = True
                    fake_battlefield.play_a_card(c, self.left)
                    cards.append(len(mana_creature) + fake_battlefield.nb_land_in_play_right - fake_battlefield.mana_used_right - c.cost)
                    fake_battlefield = copy_battlefield(self.battlefield_play)
                else:
                    cards.append(1000)
            if playable:
                min_card = min(cards)
                index = cards.index(min_card)
                self.battlefield_play.play_a_card(self.battlefield_play.hand_j_right[index], self.left)
        if playable:
            return self.can_play(True)
        return
    def combat (self):
        """
    Execute the combat phase.
    """
        com = Combat_phase (self.battlefield_play)
        com.reset()
        com.attack_phase(self.battlefield_play.possible_attacking_creature(self.left))
        com.assign_damage()
        com.finish()
        com.died_effect()
        com.finish()
        return
    def boost_target_crea (self, strength, life):
        """
        Boost a random creature in the board of the player who is playing,
        by adding the given strength and life.
        """
        if self.left:
            if len(self.battlefield_play.board_j_left) > 0:
                random.shuffle(self.battlefield_play.board_j_left)
                c = self.battlefield_play.board_j_left[0]
                c.strength += strength
                c.actual_strength += strength
                c.actual_life += life
                c.life += life
            return
        if len(self.battlefield_play.board_j_right) > 0:
            random.shuffle(self.battlefield_play.board_j_right)
            c = self.battlefield_play.board_j_right[0]
            c.strength += strength
            c.actual_strength += strength
            c.actual_life += life
            c.life += life
        return
    
class Multi_battlefield:
    def __init__ (self, deck_couple, algo_indice_couple, nb_sim):
        """
        Init of the Multi_battlefield class

        Args:
            deck_couple (tuple): a tuple of two decks
            algo_indice_couple (tuple): a tuple of two indices, the first one for the first deck and the second for the second deck
            nb_sim (int): the number of simulations
        """
        self.deck_1, self.deck_2 = deck_couple
        self.nb_sim = nb_sim
        self.algo_indice_1 = algo_indice_couple[0]
        self.algo_indice_2 = algo_indice_couple[1]
    def one_dual (self, left):
        """ Simulates a single duel between two decks using specified algorithms.
    This function initializes a battlefield with the given decks and assigns
    algorithms to the left and right players based on their indices. The duel
    proceeds with alternating turns until a winner is determined. The win count
    for the victorious player is updated accordingly.

    The left player always starts first, and the game continues until one of
    the player wins.
    """
        self.left = left
        current_battlefield = Battlefield (self.deck_1.copy(), self.deck_2.copy())
        if self.algo_indice_1 == 0:
            self.algo_1 = Random_algo_att (True, current_battlefield)
        elif self.algo_indice_1 == 1:
            self.algo_1 = Opti_algo_att (True, current_battlefield)
        elif self.algo_indice_1 == 2:
            self.algo_1 = S_algo_att (True, current_battlefield)
        if self.algo_indice_2 == 0:
            self.algo_2 = Random_algo_att (False, current_battlefield)
        elif self.algo_indice_2 == 1:
            self.algo_2 = Opti_algo_att (False, current_battlefield)
        elif self.algo_indice_2 == 2:
            self.algo_2 = S_algo_att (False, current_battlefield)
        current_battlefield.game_begin()
        while current_battlefield.winner == -1:
            current_battlefield.upkeep(self.left)
            if self.left:
                self.algo_1.can_play(False)
                self.algo_1.combat()
            else:
                self.algo_2.can_play(False)
                self.algo_2.combat()
            self.left = not self.left
        return current_battlefield.winner
    def multi_dual (self):
        
        self.nb_victory_algo_1_start = self.nb_victory_algo_2_start = self.nb_victory_algo_1_2nd = self.nb_victory_algo_2_2nd = 0
        for i in range (self.nb_sim):
            if self.one_dual (True) == 1:
                self.nb_victory_algo_1_start += 1
            else:
                self.nb_victory_algo_2_2nd += 1
        for i in range (self.nb_sim):
            if self.one_dual (False) == 0:
                self.nb_victory_algo_2_start += 1
            else:
                self.nb_victory_algo_1_2nd += 1
        return f"L'algo 1 a gagné {self.nb_victory_algo_1_start} fois en commençant et {self.nb_victory_algo_1_2nd} fois en jouant en 2ème avec le deck mono-green. L'algo 2 a gagné {self.nb_victory_algo_2_start} fois en commençant et {self.nb_victory_algo_2_2nd} fois en jouant en 2ème avec le deck mono-green."

# PHASE DE TEST :
multi = Multi_battlefield ((mono_green, mono_green),(0,2),10000)
print(multi.multi_dual())