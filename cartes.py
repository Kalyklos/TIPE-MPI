class Card:
    colors = ["green", "red", "blue", "white", "black", "colorless"]
    types = ["creatures","artifacts", "land"] #to complete
    def __init__ (self, cost, legendary, c_type, effect):
        self.cost = cost
        self.legendary = legendary
        self.c_type = c_type
        self.effect = effect
        self.inst = True

def opti_spend_colorless (mana, card):
    pass #to do but later

def is_playable (can_cast_sorcery, mana, card):
    mana_cp = mana
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

        if tot_mana >= 0:
            return False
        opti_spend_colorless (mana_cp, card)
        return (True, mana_cp)
    return (False, mana)
