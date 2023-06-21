from screen_controller import ScreenController
#from pokemon_database import PokemonDatabase
import json
import csv
import time
import sqlite3


def getPokemon(screen_reader):
    pokemon = {}
    pokemon['name'] = screen_reader.readName()
    pokemon['cp'] = screen_reader.readCP()
    pokemon['hp'] = screen_reader.readHP()
    (pokemon['attack'],pokemon['defense'],pokemon['health']) = screen_reader.readIVs()

    #pokemon_details = PokemonDatabase.findPokemon(name:pokemon.name)
    #pokemon.family = pokemon_details.family

    return pokemon


def main():
    screen_reader = ScreenController()
    conn = sqlite3.connect('db.db')
    cursor = conn.cursor()
    cursor.execute('''DELETE FROM pokemons;''')


    last = {}
    last_count = 0
    for i in range(3000):
        #current_time = time.time()
        file = open('pokemons.csv', 'w', newline='')
        writer = csv.writer(file)
        #print("Time passed:", time.time() - current_time, "seconds")
        screen_reader.takeScreenshot()
        pokemon = getPokemon(screen_reader)
        print(pokemon)
        #name,cp,hp,attack,defense,health
        writer.writerow((pokemon['name'],pokemon['cp'],pokemon['hp'],pokemon['attack'],pokemon['defense'],pokemon['health']))
        cursor.execute("INSERT INTO pokemons (name, cp, hp, attack, defense, health) VALUES (?, ?, ?, ?, ?, ?)", (pokemon['name'],pokemon['cp'],pokemon['hp'],pokemon['attack'],pokemon['defense'],pokemon['health']))
        if(last == pokemon): ???
            last_count += 1
            if last_count > 10:
                break
        else:
            last_count = 0

        screen_reader.gotoNext()

        file.close()





main()