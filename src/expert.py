# -*- coding: utf-8 -*-
from collections import OrderedDict

class ExpertSystem:
    def __init__(self):
        #self.rules = {}
        #self.facts = {}
        self.rules = OrderedDict()
        self.facts = OrderedDict()
        self.cats = ('ScottishFold', 'PersianCat', 'Ragdoll', 'AmericanShorthair', 'Siamese', 'DragonLi', 'BritishShorthair', 'Chinchilla', 'TurkishAngora', 'NorwegianForestCat')

    def readRule(self, filename):
        with open(filename, 'r') as f:
            while True:
                line = f.readline()
                if not line:
                    break
                
                line = line.strip()
                if line == '':
                    line = f.readline()
                    line = line.strip()

                arg = line.split(' ')
                con = [' '.join(arg[1:])]
                isAnd = True
                while True:
                    line = f.readline()
                    arg = line.strip().split(' ')
                    if arg[0] == 'THEN':
                        self.rules[tuple(['AND' if isAnd else 'OR'] + con)] = arg[1]
                        break
                    if arg[0] == 'OR':
                        isAnd = False
                    con.append(' '.join(arg[1:]))
    
    def engineWork(self, conditions):
        
        self.facts = OrderedDict()
        for s in conditions:
            print(s)
            arg = s.split(' ')
            if len(arg) == 1: # A
                self.facts[arg[0]] = True
            if len(arg) == 3: # A is B
                self.facts[arg[0]] = arg[2]

        while True:
            hasNewFact = False
            for (cons, fact) in self.rules.items():
                if fact in self.facts.keys():
                    continue
                isMatch = True if cons[0] == 'AND' else False
                for con in cons[1:]:
                    arg = con.split(' ')
                    success = False
                    if len(arg) == 1:
                        success = True if (arg[0] in self.facts.keys()) else False
                    
                    if len(arg) == 3:
                        success = True if (arg[0] in self.facts.keys() and self.facts[arg[0]] == arg[2]) else False
                    
                    if success is False and cons[0] == 'AND':
                        isMatch = False
                        break
                    if success is True and cons[0] == 'OR':
                        isMatch = True
                        break
                if isMatch is True:
                    hasNewFact = True
                    self.facts[fact] = True
                    if fact in self.cats:
                        return fact
                    break
            if hasNewFact is False:
                break
        return None
        

if __name__ == '__main__':
    es = ExpertSystem()
    es.readRule('src/rule.txt')
    conditions = (
        'head_shape is round',
        'head_size is big',
        'body_size is mid',
        'fat is false',
        'legs is short',
        'hair_length is long',  
        'tail_length is short',
        'eyes_shape is round',
        'ears_size is small',
        'ears_shape is round',
        'temperament is sensitive',
    )
    print(es.engineWork(conditions))
