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

        with open('multiplier.json', 'r') as file:
            self.multiplier = json.load(file)

    def findPokemon(self,name):
        for p in self.data:
            if p['name'] == name:
                return p
        return None

    def getMultiplier(self,level):
        for multiplier in self.multiplier:
            if(multiplier['level'] == level):
                return multiplier['multiplier']
        return 0
        

    def calculateCP(self,attack,defense,health,level):
        multiplier = self.getMultiplier(level)
        cp = (pow(attack, 1) * pow(defense, 0.5) * pow(health, 0.5) * pow(multiplier, 2)) / 10
        return cp

    def getProdStats(self,name):
        rc = []
        p1 = self.findPokemon(name)

        for level_index in range(100):
            level = level_index / 2.0
            for attack in range(16):
                for defense in range(16):
                    for health in range(16):
                        cp = self.calculateCP(attack,defense,health,level)
                        
                        ind_attack = p1['stat']['atk'] + attack
                        ind_defense = p1['stat']['def'] + defense
                        ind_health = p1['stat']['sta'] + health
                        
                        stat_prod = ind_attack * ind_defense * ind_health
                        rc.append({'name': name ,'level':level,'attack':attack,'defense': defense, 'health':health,'stat_prod': stat_prod})
        return rc
    
    def getProdStatMax(self,name,maxCP):
        matrix = self.getProdStats(name)
        rc = matrix[0]
        
        for m in matrix:
            if(m['stat_prod'] > rc['stat_prod']):
                rc = m
        
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
            for l in range(100):
                level = l / 2.0
                cp = self.calculateCP(attack,defense,health,level)
                
                if(maxCP < cp):
                    break
                
                ind_attack = member['stat']['atk'] + attack
                ind_defense = member['stat']['def'] + defense
                ind_health = member['stat']['sta'] + health
                
                stat_prod = ind_attack * ind_defense * ind_health
                if(stat_prod > rc['stat_prod']):
                    rc = {'stat_prod': stat_prod, 'level': level, 'family_member': member}
        
        return rc
        



