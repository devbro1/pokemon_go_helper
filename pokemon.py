from Pokedex import Pokedex

pokedex = Pokedex()


class Pokemon:
    def __init__(self, details):

        self.name = details['name']
        self.cp = details['cp']
        self.attack = details['attack']
        self.defense = details['defense']
        self.health = details['health']
        self.hp = details['hp']

        family_details = pokedex.findPokemon(self.name)
        self.ind_attack = family_details['stats']['atk'] + details['attack']
        self.ind_defense = family_details['stats']['def'] + details['defense']
        self.ind_health = family_details['stats']['sta'] + details['health']
        self.stat_prod = self.calculateStatProd()
        self.iv_percentage = self.calculateIVPercentage()
        self.level = '???'

    def calculateIVPercentage(self):
        return (self.attack + self.defense + self.health) / 45.0

    def calculateStatProd(self):
        return self.ind_attack * self.ind_defense * self.ind_health

    def getBestLittleLeagueStatProd(self):
        if(self.cp > 500):
            return -1
        
        
