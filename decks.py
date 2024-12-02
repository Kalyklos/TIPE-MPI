from stack_v import *
from battle import *

data_base = {}
data_base ["Gigantosorus"] = Creature(10,10,[],[],{"green" : 5})
data_base ["Forest"] = Land("green")
data_base ["Island"] = Land("blue")
data_base ["Mountain"] = Land("red")
data_base ["Swamp"] = Land("black")
data_base ["Plain"] = Land("white")
mono_green = {} #32 cards remaining
mono_green ["Gigantosorus"] = 4
mono_green ["Forest"] = 24
# deck list mono-green :
# forest * 25
# Stony Strength *2 (inst, +1/+1 counter, untap, 1 mana)
# Jungle delver *3 (1/1, pay 4 to get a +1/+1 counter, 1 mana)
# Woodland Mystic *2 (1/1, tap for a mana, 2 mana)
# Rabid Bite *3 (inst, deal damage, 2 mana)
# Ilysian Caryatid *4 (1/1, tap for 1 mana, 2 if crea power >= 4, 2 mana)
# Colossal Majesty *2 (enchant, upkeep draw if crea power >= 4, 3 mana)
# Wildwood Patrol *2 (4/2 trample, 3 mana)
# Baloth Packhunter *4 (3/3 trample, enter 2 +1/+1 counter onto other crea with the same name, 4 mana)
# Umbling Baloth *2 (4/4, 4 mana)
# Gigantosaurus *4 (10/10, 5 mana)
# Sentinel Spider *2 (4/4 vigilance reach, 5 mana)
# Affectionate Indrik *2 (4/4, enter may fight, 6 mana)
# Epic Proportions *1 (enchant a crea +5/+5 trample, 6 mana)
# Rampaging Brontodon *2 (7/7 trample, attack +X/+X X is nb of land, 7 mana)