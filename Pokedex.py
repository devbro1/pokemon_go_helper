import json
import math
    
class Pokedex:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        with open('pokedex.json', 'r') as file:
            self.data = json.load(file)

        with open('multiplier.json', 'r') as file:
            self.multiplier = json.load(file)
            
        self.prodstats = {}

    def findPokemon(self,name):
        for p in self.data:
            if p['name'] == name:
                return p
            elif 'alternative_names' in p and name in p['alternative_names']:
                return p
        return None

    def getMultiplier(self,level):
        for multiplier in self.multiplier:
            if(multiplier['level'] == level):
                return multiplier['multiplier']
        return 'AAA'
        

    def calculateCP(self,attack,defense,health,level):
        multiplier = self.getMultiplier(level)
        cp = (pow(attack, 1) * pow(defense, 0.5) * pow(health, 0.5) * pow(multiplier, 2)) / 10
        return cp

    def getProdStats(self,name,maxCP):
        rc = []
        if(name in self.prodstats and maxCP in self.prodstats[name]):
            return self.prodstats[name][maxCP]
        p1 = self.findPokemon(name)

        for attack in range(16):
            for defense in range(16):
                for health in range(16):
                    best = self.getBest(name,maxCP,attack,defense,health)
                    rc.append(best)
        
        if(not name in self.prodstats):
            self.prodstats[name] = {}
        self.prodstats[name][maxCP] = rc
        return rc
    
    def getProdStatMax(self,name,maxCP):
        rc = self.getProdStats(name,maxCP)
        rc = sorted(rc,key=lambda x: -x['stat_prod'])
        return rc
    
    def getFamilyMembers(self,name):
        pokemon = None
        rc = []
        for p in self.data:
            if(p['name'] == name or p['id'] == name):
                pokemon = p
                break
            
        if pokemon != None:
            for p in self.data:
                if(p['family']['id'] == pokemon['family']['id']):
                    rc.append(p)
        
        return rc
    
    def getBest(self,name,maxCP,attack,defense,health):
        family_members = self.getFamilyMembers(name)
        rc = {'stat_prod':0}
        
        for member in family_members:
            for l in range(2,100):
                level = l / 2.0
                multiplier = self.getMultiplier(level)
                
                ind_attack = member['stats']['atk'] + attack
                ind_defense = member['stats']['def'] + defense
                ind_health = member['stats']['sta'] + health
                
                cp = self.calculateCP(ind_attack,ind_defense,ind_health,level)
                
                if(maxCP < cp):
                    break
                
                stat_prod = (ind_attack * multiplier) * (ind_defense * multiplier)  * (ind_health * multiplier)

                if(stat_prod > rc['stat_prod']):
                    rc = {'stat_prod': stat_prod, 'level': level, 'family_member': member, 'cp': cp, 'attack':attack,'defense':defense,'health': health}
        
        return rc
        



