from battle import *
class random_algo:
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
                battlefield_play.play_a_card(battlefield_play.remaining_mana_left, pop(playable_card), True)
            else:
                battlefield_play.play_a_card(battlefield_play.remaining_mana_right, pop(playable_card), False)
            playable_card = []
            if self.left:
                for c in battlefield_play.hand_j_left:
                    if is_playable(battlefield_play.can_cast_sorcery_left, battlefield_play.remaining_mana_left, c):
                        playable_card.append(c)
            else:
                for c in battlefield_play.hand_j_right:
                    if is_playable(battlefield_play.can_cast_sorcery_right, battlefield_play.remaining_mana_right, c):
                        playable_card.append(c)
        