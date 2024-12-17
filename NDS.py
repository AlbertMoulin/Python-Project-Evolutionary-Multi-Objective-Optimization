from typing import List, Dict
from Value import Value
from Individual import Individual
from collections import deque

class Nds:
    def NdSorting(Q : List[Individual], f) -> List[List[Individual]]:
        # Dictionary that will contain the number of individuals who dominate current individual 
        # and a list of all individual who are dominated by current 
        D = {}
        
        for x in Q:
            D[x] = (0,[])
            for y in Q :
                if x> y:
                    D[x][1].append(y)
                if x<y : 
                    D[x][0] +=1
            