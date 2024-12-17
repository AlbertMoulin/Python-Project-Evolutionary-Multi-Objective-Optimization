from typing import List, Dict
from Value import Value
from Individual import Individual
from collections import deque

class Nds:
    
    def NdSorting(Q : List[Individual], f) -> List[List[Individual]]:
        
        # Dictionary that will contain the number of individuals who dominate current individual 
        # and a list of all individual who are dominated by current 
        D = {}
        
        Fronts = [[]]
        
        for x in Q:
            D[x] = [0,[]]
            for y in Q:
                if f(x)> f(y):
                    D[x][1].append(y)
                if f(x)<f(y): 
                    D[x][0] +=1
            
            if D[x][0] == 0:
                Fronts[0].append(x)
        
        i = 0
        while (True):
            FrontIPlusOne = []
            for x in Fronts[i]:
                
                for y in D[x][1]:
                    D[y][0] -=1
                    
                    if D[y][0] == 0:
                        FrontIPlusOne.append(y)
            if len(FrontIPlusOne) == 0:
                return Fronts
            Fronts.append(FrontIPlusOne)
            i += 1
            
            
if __name__ == "__main__":
    from Sample import Sample
    from LOTZ import LOTZ
    
    F = Nds.NdSorting(Sample.GenerateIndividual(5,10), LOTZ.LOTZdeux )
    Q = []
    for f in F:
        Qi = []
        for fi in f:
            Qi.append(LOTZ.LOTZdeux(fi))
        Q.append(Qi)
    print( F )
    print(Q)
    