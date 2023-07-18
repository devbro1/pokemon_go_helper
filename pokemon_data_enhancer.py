# purpose: to read screenshots and extract dat as needed
from pokemon import Pokemon
from Pokedex import Pokedex
from screen_controller import  ScreenController
from PIL import Image
import os

screen_reader = ScreenController()
for filename in os.scandir('screenshots'):
    screen_reader.setScreenshot(Image.open(filename.path))
    pokemon: Pokemon = screen_reader.getPokemon()
    
    print(pokemon.toArray())
