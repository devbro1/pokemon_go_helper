# purpose: to extract data from the game one screenshot at a time and/or through auto-swipes plus pokegenie
from screen_controller import ScreenController
import time

def getPokemon(screen_reader):
    pokemon = {}
    pokemon['name'] = screen_reader.readName()
    pokemon['cp'] = screen_reader.readCP()
    pokemon['hp'] = screen_reader.readHP()
    (pokemon['attack'],pokemon['defense'],pokemon['health']) = screen_reader.readIVs()

    return pokemon

def main():
    screen_reader = ScreenController()
    for i in range(1500,2350):
        screen_reader.takeScreenshot( 'screenshots\\pokemon_' + str(i) + '.png')
        print("current index: " + str(i))
        screen_reader.gotoNext()
        time.sleep(5) # use less time if you do not want to pokegenie

main()
