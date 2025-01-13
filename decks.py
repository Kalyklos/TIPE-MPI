from stack_v import *
from battle import *

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
data_base ["Stony Strength"] = Instant(true, 1, False, {"green" : 1})
data_base ["Rabid Bite"] = Instant(false, 0, False, {"green" : 2})
data_base ["Epic Proportions"] = Instant(false, 5, True, {"green" : 6})
data_base ["Wildwood Patrol"] = Creature(4,2,["trample"], [], {"green" : 3})
data_base ["Affectionate Indrik"] = Creature(4,4,[], [Effect([],[],[True],[],[])], {"green" : 6})
data_base ["Rampaging Brontodon"] = Creature(7,7, ["trample"], [Effect([],[],[],[],[True])], {"green" : 7})
data_base ["Colossal Majesty"] = Enchantment([Effect([True],[],[],[],[])], {"green" : 3})
data_base ["Baloth Packhunter"] = Creature(3,3,["trample"],[Effect([],[],[False, True],[],[])], {"green" : 4})
data_base ["Baloth Packhunter"].baloth = True
data_base ["Jungle Delver"] = Creature(1,1,[],[Effect([],[True],[],[],[])],{"green" : 1})

""" Création du deck mono-vert.
"""
mono_green = {}
mono_green ["Gigantosorus"] = 4
mono_green ["Umbling Baloth"] = 2
mono_green ["Forest"] = 25
mono_green ["Woodland Mystic"] = 2
mono_green ["Sentinel Spider"] = 2
mono_green ["Stony Strength"] = 2
mono_green ["Ilysian Caryatid"] = 4
mono_green ["Rabid Bite"] = 3
mono_green ["Epic Proportions"] = 1
mono_green ["Wildwood Patrol"] = 2
mono_green ["Affectionate Indrik"] = 2
mono_green ["Rampaging Brontodon"] = 1
mono_green ["Colossal Majesty"] = 2
mono_green ["Baloth Packhunter"] = 4