from screen_controller import ScreenController
#from pokemon_database import PokemonDatabase
import json
import csv
import time


def getPokemon(screen_reader):
    pokemon = {}
    pokemon['name'] = screen_reader.readName()
    pokemon['cp'] = screen_reader.readCP()
    pokemon['hp'] = screen_reader.readHP()
    (pokemon['attack'],pokemon['defense'],pokemon['stamina']) = screen_reader.readIVs()

    #pokemon_details = PokemonDatabase.findPokemon(name:pokemon.name)
    #pokemon.family = pokemon_details.family

    return pokemon


def main():
    screen_reader = ScreenController()
    for i in range(1900):
        #current_time = time.time()
        file = open('pokemons.csv', 'a', newline='')
        writer = csv.writer(file)
        #print("Time passed:", time.time() - current_time, "seconds")
        screen_reader.takeScreenshot()
        pokemon = getPokemon(screen_reader)
        print(pokemon)
        #name,cp,hp,attack,defense,stamina
        writer.writerow((pokemon['name'],pokemon['cp'],pokemon['hp'],pokemon['attack'],pokemon['defense'],pokemon['stamina']))
        screen_reader.gotoNext()

        file.close()



main()