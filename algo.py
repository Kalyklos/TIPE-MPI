from battle import *
class Random_algo_att:
    def __init__ (self, left, battlefield_play):
        self.left = left
    def can_play (self):
        playable_card = []
        if self.left:
            battlefield_play.play_land(left, battlefield_play.nb_land_play_left)
            for c in battlefield_play.hand_j_left:
                if is_playable(battlefield_play.can_cast_sorcery_left, battlefield_play.remaining_mana_left, c):
                    playable_card.append(c)
        else:
            battlefield_play.play_land(left, battlefield_play.nb_land_play_right)
            for c in battlefield_play.hand_j_right:
                if is_playable(battlefield_play.can_cast_sorcery_right, battlefield_play.remaining_mana_right, c):
                    playable_card.append(c)
        while len(playable_card) > 0:
            random.shuffle(playable_card)
            if self.left:
                battlefield_play.play_a_card(battlefield_play.remaining_mana_left, playable_card.pop(), True)
            else:
                battlefield_play.play_a_card(battlefield_play.remaining_mana_right, playable_card.pop(), False)
            playable_card = []
            if self.left:
                for c in battlefield_play.hand_j_left:
                    if is_playable(battlefield_play.can_cast_sorcery_left, battlefield_play.remaining_mana_left, c):
                        playable_card.append(c)
            else:
                for c in battlefield_play.hand_j_right:
                    if is_playable(battlefield_play.can_cast_sorcery_right, battlefield_play.remaining_mana_right, c):
                        playable_card.append(c)
    def combat (self):
        com = Combat_phase (self.battlefield_play)
        com.reset()
        com.attack_phase(self.battlefield_play.possible_attacking_creature(left))
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
            