from typing import List, Dict

class Individual:
    
    individual : List[int]

    IndexNext : int
    IndexPrevious : int
    
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


    
if __name__ == "__main__":
    indiv1 = Individual([0,1,2,84])
    indiv2 = Individual([0,1,2,84])