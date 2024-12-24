from typing import List, Dict
import random

class Individual:
    
    individual : List[int]
    
    def __init__(self, individual : List[int]):
        self.individual = individual
        self.ValueNext = []
        self.ValuePrevious = []
        self.IndexNext = None
        self.IndexPrevious = None
    
    def __str__(self):
        return self.individual.__str__()
    
    def __repr__(self):
        return self.individual.__str__()
    
    def __add__(self, other):

        if not isinstance(other, Individual):
            return ValueError("You are trying to add an Individual with some other type")
        return Individual(self.individual + other.individual)
    
    def mutate(self):
        n = len(self.individual)
        Lk = self.individual.copy()
        # Mutate individual's list
        for i in range(n):
            if random.uniform(0,1) < 1/n :
                Lk[i] = 1-Lk[i]
        return Individual(Lk)


    
if __name__ == "__main__":
    indiv1 = Individual([0,1])
    indiv2 = Individual([0,1,2,84])
    for k in range(5):
        print(indiv1.mutate())