from battle import *
class random_algo:
    def __init__ (self, left, battlefield_play):
        self.left = left
    def can_play (self):
        if left:
            random.shuffle(battlefield_play.hand_j_left)
            battlefield_play.play_land(left, battlefield_play.nb_land_play_left)
