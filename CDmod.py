from Individual import Individual
from Value import Value
from typing import Callable
from Sample import Sample
from LOTZ import LOTZ

class CDmod:
    
    ListF : list
    # List of Individuals
    f : Callable
    # function taking an individual and giving it's value for every objective k
    m : int
    # number of objectives
    N : int
    # number of individuals

    # Initialisation
    def __init__(self, f, ListF):
        self.f = f
        self.ListF = ListF
        self.m = len(f(self.ListF[0]).value)
        self.N = len(ListF)

    # Crowding distance function
    def CDmod(self):
        # Creating a matrix giving the crowding distance of an individual i for the objective k 
        MatrixCD = [[0 for i in range(self.N)] for k in range(self.m)]
        # Loop on all objectives
        for k in range(self.m):
            # define the function giving the value on said k of individual x
            def fk(x):
                return self.f(x).value[k]
            
            # Sorting the indicies by the value on objective k
            IndiciesSortedByK = sorted(range(self.N), key=lambda index: fk(self.ListF[index]) )
            # xi is the ith highest individual regarding values on objective k
            def xi(i):
                return self.ListF[IndiciesSortedByK[i]]
            q = fk(xi(-1))- fk(xi(0))
            if q != 0:
                for i in range(1,self.N-1):
                    # using the formula for the crowding distance we have :
                    di = fk(xi(i+1))- fk(xi(i-1))
                    MatrixCD[k][IndiciesSortedByK[i]] = di/q
                MatrixCD[k][IndiciesSortedByK[0]] = float('inf')
                MatrixCD[k][IndiciesSortedByK[-1]] = float('inf')
            
            
        # Giving the final distance for every individual by summing on all objectives
        Final_List = [0 for i in range(self.N)]
        for i in range(self.N):
            for k in range(self.m):
                Final_List[i] += MatrixCD[k][i]
        return Final_List
    

    def CDupdate(self):
        return self

# tests
if __name__ == "__main__":
    print()