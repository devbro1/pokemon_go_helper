import json

class Pokedex:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        with open('pokedex.json', 'r') as file:
            self.data = json.load(file)

    def findPokemon(self,name):
        for p in self.data:
            if p['name'] == name:
                return p
        return None

    def getMultiplier(self,level):
        

    def calculateCP(self,attack,defense,health,level):
        multiplier = self.getMultiplier(level)

    def maxProdStat(self,name,maxCP):
        p1 = self.findPokemon(name)


        for level_index in range(100):
            level = level_index / 2.0
            for attack in range(16):
                for defense in range(16):
                    for health in range(16):
                        cp = self.calculateCP(attack,defense,health,level)



