from battle import *
from decks import *
from carte import *

list_algo = ["rdm_att"]

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
    def can_play (self):
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

        playable_card = []
        if self.left:
            self.battlefield_play.play_land(self.left)
            for c in self.battlefield_play.hand_j_left:
                if self.battlefield_play.is_playable(self.left, c):
                    playable_card.append(c)
        else:
            self.battlefield_play.play_land(self.left)
            for c in self.battlefield_play.hand_j_right:
                if is_playable(self.left, c):
                    playable_card.append(c)
        while len(playable_card) > 0:
            shuffle(playable_card)
            if self.left:
                self.battlefield_play.play_a_card(self.battlefield_play.remaining_mana_left, playable_card.pop(), True)
            else:
                self.battlefield_play.play_a_card(self.battlefield_play.remaining_mana_right, playable_card.pop(), False)
            playable_card = []
            if self.left:
                for c in self.battlefield_play.hand_j_left:
                    if is_playable(self.battlefield_play.can_cast_sorcery_left, self.battlefield_play.remaining_mana_left, c):
                        playable_card.append(c)
            else:
                for c in self.battlefield_play.hand_j_right:
                    if is_playable(self.battlefield_play.can_cast_sorcery_right, self.battlefield_play.remaining_mana_right, c):
                        playable_card.append(c)
        return
    def combat (self):
        """
    Executes the combat phase.
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
        if left:
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
        self.algo_indice_1, self.algo_indice_2 = algo_indice_couple
        self.victory = [0, 0] #victory[0] = nb de combat gagné par algo_1 et inversement
    def one_dual (self):
        """ Simulates a single duel between two decks using specified algorithms.
    This function initializes a battlefield with the given decks and assigns
    algorithms to the left and right players based on their indices. The duel
    proceeds with alternating turns until a winner is determined. The win count
    for the victorious player is updated accordingly.

    The left player always starts first, and the game continues until one of
    the player wins.
    """

        current_battlefield = Battlefield (self.deck_1, self.deck_2)
        if self.algo_indice_1 == 0:
            self.algo_1 = Random_algo_att (True, current_battlefield)
        if self.algo_indice_2 == 0:
            self.algo_2 = Random_algo_att (False, current_battlefield)
        current_battlefield.game_begin()
        left = True       #l'algo_1 sera considéré comme joueur de gauche et commencera
        while current_battlefield.winner == -1:
            current_battlefield.upkeep(left)
            if left:
                self.algo_1.can_play()
                self.algo_1.combat()
            else:
                self.algo_2.can_play()
                self.algo_2.combat()
        self.victory[current_battlefield.winner] += 1
        return
    def multi_dual (self):
        """
        Simulates multiple duels between two decks using specified algorithms.

        This function initializes the number of victories for each deck to 0 and
        then runs the one_dual function nb_sim times. After each duel, the
        number of victories for the winner is incremented. The decks and algorithms are then
        swapped to change the starting player and the same process is repeated. The final number of victories
        for each deck is returned as a list of lists. The outer list has two
        elements, the first one being the number of victories for deck 1 and the
        second one being the number of victories for deck 2. The inner lists have
        two elements each, the first one being the number of victories when the
        deck starts and the second one being the number of victories when the
        deck does not start.

        Args:
            None

        Returns:
            A list of lists containing the number of victories for each deck.

        """
        self.win_deck = [[0,0],[0,0]]  #win (deck 1 (beginer (y, n)), deck 2 (beginer (y, n)))
        for i in range (self.nb_sim):
            self.one_dual()
        self.win_deck[0][0] = self.victory[0]
        self.win_deck[1][0] = self.victory[1]
        self.victory = [0, 0]
        self.deck_1, self.deck_2 = self.deck_2, self.deck_1
        self.algo_1, self.algo_2 = self.algo_2, self.algo_1
        for i in range (self.nb_sim):
            self.one_dual()
        self.win_deck[0][1] = self.victory[1]
        self.win_deck[1][1] = self.victory[0]
        return self.win_deck

# PHASE DE TEST :
multi = Multi_battlefield ((mono_green, mono_green.copy()),(0,0),500)
print(multi.multi_dual())