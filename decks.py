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