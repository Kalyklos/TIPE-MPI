from battle import *
from decks import *
from carte import *

list_algo = ["rdm_att"]

class Random_algo_att:
    def __init__ (self, left, battlefield_play):
        self.left = left
        self.battlefield_play = battlefield_play
    def can_play (self):
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
        com = Combat_phase (self.battlefield_play)
        com.reset()
        com.attack_phase(self.battlefield_play.possible_attacking_creature(self.left))
        com.assign_damage()
        com.finish()
        com.died_effect()
        com.finish()
        return
    def boost_target_crea (self, strength, life):
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
        self.deck_1, self.deck_2 = deck_couple
        self.nb_sim = nb_sim
        self.algo_indice_1, self.algo_indice_2 = algo_indice_couple
        self.victory = [0, 0] #victory[0] = nb de combat gagné par algo_1 et inversement
    def one_dual (self):
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