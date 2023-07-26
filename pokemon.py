from Pokedex import Pokedex

pokedex = Pokedex()


class Pokemon:
    def __init__(self, name,attack,defense,stamina,cp=0):

        self.name = name
        self.cp = cp
        self.attack = attack
        self.defense = defense
        self.stamina = stamina

        family_details = pokedex.findPokemon(self.name)
        if (family_details):
            self.family = family_details
            self.ind_attack = family_details['stats']['atk'] + self.attack
            self.ind_defense = family_details['stats']['def'] + self.defense
            self.ind_stamina = family_details['stats']['sta'] + self.stamina
        else:
            raise LookupError('Family not found')
        self.stat_prod = self.calculateStatProd()
        self.iv_percentage = self.calculateIVPercentage()
        # self.level = False
        
        # self.sp_little = self.getBestLittleLeagueStatProd()['stat_prod']
        # self.sp_great = self.getBestGreatLeagueStatProd()['stat_prod']
        # self.sp_ultra = self.getBestUltraLeagueStatProd()['stat_prod']

            
    def toArray(self):
        return (self.name, self.cp, self.attack, self.defense, self.stamina, self.iv_percentage, self.stat_prod, self.sp_little, self.sp_great, self.sp_ultra)

    def calculateIVPercentage(self):
        return (self.attack + self.defense + self.stamina) / 45.0

    def calculateStatProd(self):
        return self.ind_attack * self.ind_defense * self.ind_stamina

    def getBestLittleLeagueStatProd(self):
        return self.getBestLeagueStatProd(500)
        
    def getBestGreatLeagueStatProd(self):
        return self.getBestLeagueStatProd(1500)
        
    def getBestUltraLeagueStatProd(self):
        return self.getBestLeagueStatProd(2500)
        
    def getBestLeagueStatProd(self,maxCP):
        if(self.cp > maxCP):
            return {'stat_prod': -1}

        matrix = pokedex.getProdStatMax(self.name,maxCP)
        
        rc={}
        index=0
        c = len(matrix)
        for m in matrix:
            if(m['attack']==self.attack and m['defense'] == self.defense and m['health'] == self.stamina):
                rc['percentile'] = (c - index) / c
                rc['rank'] = index
                rc['count'] = c
                break
            index += 1
        
        return rc
                
                
        
        
