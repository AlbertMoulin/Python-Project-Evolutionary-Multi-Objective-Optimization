from Individual import Individual
from Value import Value
from typing import Callable
from Sample import Sample
from LOTZ import LOTZ

class CD:
    
    ListF : list
    # List of Individuals
    f : Callable
    # function taking an individual and giving it's value for every objective k
    m : int
    # number of objectives
    N : int
    # number of individuals
    CDList : list
    # crowding distance list
    MatrixCD : list
    #Matrix of crowding distance of an individual i for the objective k
    AdjacentsInfo : list
    #Lists of sorted indicies for every objective k
    ListQk : list
    # List of the denominators for every objective

    def CalculateCDList(self):
        self.CDList = [0 for i in range(self.N)]
        for i in range(self.N):
            for k in range(self.m):
                self.CDList[i] += self.MatrixCD[k][i]/self.ListQk[k]
        
    def fk(self,k,x):
        return self.f(x).value[k]
    
    def xki(self,k,i):
        return self.ListF[self.AdjacentsInfo[k][i]]
    
    def fkxi(self,k,i):
        return self.fk(k,self.xki(k,i))

    # Initialisation
    def __init__(self, f, ListF):
        self.f = f
        self.ListF = ListF
        self.m = len(f(self.ListF[0]).value)
        self.N = len(ListF)
        # Creating a matrix giving the crowding distance of an individual i for the objective k 
        MatrixCD = [[0 for i in range(self.N)] for k in range(self.m)]
        self.AdjacentsInfo = []
        self.ListQk = []
        # Loop on all objectives
        for k in range(self.m):
            # define the function giving the value on said k of individual x
            
            
            # Sorting the indicies by the value on objective k
            IndiciesSortedByK = sorted(range(self.N), key=lambda index: self.fk(k,self.ListF[index]) )
            self.AdjacentsInfo.append(IndiciesSortedByK)
            self.ListQk.append( self.fkxi(k,-1)- self.fkxi(k,0) )
            if self.ListQk[-1] != 0:
                for i in range(1,self.N-1):
                    # using the formula for the crowding distance we have :
                    di = self.fkxi(k,i+1)- self.fkxi(k,i-1)
                    MatrixCD[k][IndiciesSortedByK[i]] = di
                MatrixCD[k][IndiciesSortedByK[0]] = float('inf')
                MatrixCD[k][IndiciesSortedByK[-1]] = float('inf')
            
        self.MatrixCD = MatrixCD   
        # Giving the final distance for every individual by summing on all objectives
        self.CalculateCDList()

    def removed(self, index):
        self.ListF.pop(index)
        self.N = self.N-1
        if self.CDList.pop(index) != float('inf'):
            for k in range(self.m):
                print(f'for index {index}')
                self.MatrixCD[k].pop(index)
                self.MatrixCD[k][self.AdjacentsInfo[k][index-1]] +=  self.fkxi(k,index+1) - self.fkxi(k,index)
                self.MatrixCD[k][self.AdjacentsInfo[k][index+1]] +=  self.fkxi(k,index) - self.fkxi(k,index-1)
        self.CalculateCDList

        
        

# tests
if __name__ == "__main__":

    def f(x):
        return LOTZ.LOTZm(4,x)
    A = Sample.GenerateIndividual(12,19)
    CD1 = CD(f,A)
    for k in A:
        print(k)
        print(LOTZ.LOTZm(4,k))
    print(CD1.CDList)



 
    