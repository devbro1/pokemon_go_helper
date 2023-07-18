from screen_controller import ScreenController
import time
from PIL import Image

# files = ['pokemon_9.png','pokemon_12.png','pokemon_14.png']
screen_reader = ScreenController()

# for file in files:
#     screen_reader.setScreenshot(Image.open('screenshots\\' + file))
#     print(screen_reader.getPokemon().toArray())

screen_reader.setScreenshot(Image.open('screen_list.png'))
print(screen_reader.readSelectCount())
