from carte import *
""" Création du deck mono-vert.
"""
mono_green = []
for i in range (4):
    mono_green.append(Card("Creature","Gigantosorus"))
    mono_green.append(Card("Creature","Baloth Packhunter"))
    mono_green.append(Card("Creature","Ilysian Caryatid"))
for i in range (2):
    mono_green.append(Card("Creature","Umbling Baloth"))
    mono_green.append(Card("Creature","Woodland Mystic"))
    mono_green.append(Card("Creature","Sentinel Spider"))
    mono_green.append(Card("Creature","Wildwood Patrol"))
    mono_green.append(Card("Creature","Affectionate Indrik"))
    mono_green.append(Card("Enchantement","Colossal Majesty"))
    mono_green.append(Card("Instant","Stony Strength"))
for i in range (25):
    mono_green.append(Card("Land","Forest"))
for i in range (3):
    mono_green.append(Card("Instant","Rabid Bite"))
mono_green.append(Card("Instant","Epic Proportions"))
mono_green.append(Card("Creature","Rampaging Brontodon"))