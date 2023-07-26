from screen_controller import ScreenController
import time
import sqlite3
import os

def getPokemon(screen_reader):
    pokemon = {}
    pokemon['name'] = screen_reader.readName()
    pokemon['cp'] = screen_reader.readCP()
    pokemon['hp'] = screen_reader.readHP()
    (pokemon['attack'],pokemon['defense'],pokemon['health']) = screen_reader.readIVs()

    return pokemon

def main():
    screen_reader = ScreenController()
    for i in range(0,1600):
        current_name =  'screenshots\\pokemon_' + str(i) + '.png'
        screen_reader.takeScreenshot(current_name)
        ivs = screen_reader.readIVs()
        if(ivs == (-1,-1,-1)):
            break
        # pokemon = screen_reader.getPokemon()
        # new_name = 'screenshots\\' + pokemon['name'] + '_' + pokemon['cp'] + '.png'
        # os.rename(current_name, new_name)
        print("current index: " + str(i))
        screen_reader.gotoNext(100)
        time.sleep(2)

main()
