from pokemon import Pokemon
from Pokedex import Pokedex

pokedex = Pokedex()

for pokemon in pokedex.data:
    print(pokemon['id'] + "," + pokemon['family']['id'])