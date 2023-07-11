from screen_controller import ScreenController
import time
import sqlite3

def getPokemon(screen_reader):
    pokemon = {}
    pokemon['name'] = screen_reader.readName()
    pokemon['cp'] = screen_reader.readCP()
    pokemon['hp'] = screen_reader.readHP()
    (pokemon['attack'],pokemon['defense'],pokemon['health']) = screen_reader.readIVs()

    return pokemon

def main():
    screen_reader = ScreenController()
    for i in range(0,2350):
        screen_reader.takeScreenshot( 'screenshots\\pokemon_' + str(i) + '.png')
        print("current index: " + str(i))
        screen_reader.gotoNext(100)
        time.sleep(2)

main()
