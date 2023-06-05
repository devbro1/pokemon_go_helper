import csv
from pokemon import Pokemon
from Pokedex import Pokedex

def read_csv_to_array(file_path):
    data = []
    with open(file_path, 'r') as file:
        reader = csv.reader(file)
        keys = next(reader)
        for row in reader:
            pokemon = {k: v for k, v in zip(keys, row)}
            pokemon['attack'] = int(pokemon['attack'])
            pokemon['defense'] = int(pokemon['defense'])
            pokemon['health'] = int(pokemon['health'])
            data.append(pokemon)
    return data

pokemon_data = read_csv_to_array('pokemons.csv')
pokedex = Pokedex()
pokemons = []

for pokemon in pokemon_data:
    pokedex_find = pokedex.findPokemon(pokemon['name'])
    if(pokedex_find):
        pokemon_obj = Pokemon(pokemon)
        pokemons.append(pokemon_obj)
    else:
        print(pokemon['name'])

    # pokemon['stat_prod'] = {}
    # pokemon['stat_prod']['little'] = ???
    # pokemon['stat_prod']['great'] = ???
    # pokemon['stat_prod']['ultra'] = ???
    

print(pokemons[0])
#print(pokedex[0])