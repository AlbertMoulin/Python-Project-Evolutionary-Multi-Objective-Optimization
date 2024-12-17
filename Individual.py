from typing import List, Dict

class Individual:
    
    individual : List[int]
    
    def __init__(self, individual : List[int]):
        self.individual = individual
    
    def __str__(self):
        return self.individual.__str__()
    
    def __repr__(self):
        return self.individual.__str__()
    