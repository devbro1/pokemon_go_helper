from screen_controller import ScreenController
#from pokemon_database import PokemonDatabase


def main():
    screen_reader = ScreenController()
    pokemon = {}
    pokemon['name'] = screen_reader.readName()
    pokemon['cp'] = screen_reader.readCP()
    pokemon['hp'] = screen_reader.readHP()
    pokemon['ivs'] = screen_reader.readIVs()


    #pokemon_details = PokemonDatabase.findPokemon(name:pokemon.name)
    #pokemon.family = pokemon_details.family

    print(pokemon)


main()