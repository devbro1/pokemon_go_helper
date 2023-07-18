from Pokedex import Pokedex

pokedex = Pokedex()


class Pokemon:
    def __init__(self, details):

        self.name = details['name']
        self.cp = int(details['cp'])
        self.attack = details['attack']
        self.defense = details['defense']
        self.health = details['health']
        self.hp = details['hp']

        family_details = pokedex.findPokemon(self.name)
        if (family_details):
            self.family = family_details
            self.ind_attack = family_details['stats']['atk'] + details['attack']
            self.ind_defense = family_details['stats']['def'] + details['defense']
            self.ind_health = family_details['stats']['sta'] + details['health']
        else:
            print("family not found: " + self.name)
        self.stat_prod = self.calculateStatProd()
        self.iv_percentage = self.calculateIVPercentage()
        # self.level = False
        
        self.sp_little = self.getBestLittleLeagueStatProd()['stat_prod']
        self.sp_great = self.getBestGreatLeagueStatProd()['stat_prod']
        self.sp_ultra = self.getBestUltraLeagueStatProd()['stat_prod']
        
        try:
            self.cp = int(self.cp)
        except:
            self.cp = 0
            
    def toArray(self):
        return (self.name, self.cp, self.attack, self.defense, self.health, self.iv_percentage, self.stat_prod, self.sp_little, self.sp_great, self.sp_ultra)

    def calculateIVPercentage(self):
        return (self.attack + self.defense + self.health) / 45.0

    def calculateStatProd(self):
        return self.ind_attack * self.ind_defense * self.ind_health

    def getBestLittleLeagueStatProd(self):
        return self.getBestLeagueStatProd(500)
        
    def getBestGreatLeagueStatProd(self):
        return self.getBestLeagueStatProd(1500)
        
    def getBestUltraLeagueStatProd(self):
        return self.getBestLeagueStatProd(2500)
        
    def getBestLeagueStatProd(self,maxCP):
        if(self.cp > maxCP):
            return {'stat_prod': -1}
        
        rc = pokedex.getBest(self.name,maxCP,self.attack,self.defense,self.health)
        if rc == None:
            return rc

        matrix = pokedex.getProdStatMax(self.name,maxCP)
        index=0
        c = len(matrix)
        for m in matrix:
            if(m['attack']==self.attack and m['defense'] == self.defense and m['health'] == self.health):
                rc['percentile'] = (c - index) / c
                rc['rank'] = index
                rc['count'] = c
                break
            index += 1
        
        return rc
                
                
        
        
