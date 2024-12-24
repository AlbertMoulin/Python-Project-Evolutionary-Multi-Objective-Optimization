from Individual import Individual
from Value import Value
from typing import Callable
from Sample import Sample
from LOTZ import LOTZ

class CD:
    
    ListF : list[Individual]
    # List of Individuals
    f : Callable[[Individual],Value]
    # function taking an individual and giving it's value for every objective k
    m : int
    # number of objectives
    N : int
    # number of individuals
    ListQ : list[float]

    # Initialisation
    def __init__(self, f : Callable, ListF : list[Individual]):
        self.f = f
        self.ListF = ListF
        self.m = len(f(self.ListF[0]).value)
        self.N = len(ListF)
        self.ListQ = []

    def fk(self, k : int, x : Individual) -> float:
        return self.f(x).value[k]

    # Crowding distance function
    def CD(self) -> None:
        # Creating a matrix giving the crowding distance of an individual i for the objective k 
        # Loop on all objectives
        for k in range(self.m):
            # define the function giving the value on said k of individual x
            
            
            # Sorting the indicies by the value on objective k
            IndiciesSortedByK = sorted(range(self.N), key=lambda index: self.fk(k, self.ListF[index]) )

            # xi is the ith highest individual regarding values on objective k
            def xi(i : int) -> Individual:
                return self.ListF[IndiciesSortedByK[i]]
            
            q = self.fk(k,xi(-1))- self.fk(k,xi(0))
            self.ListQ.append(q)
            if q != 0:
                for i in range(1,self.N-1):
                    # using the formula for the crowding distance we have :
                    di = self.fk(k,xi(i+1))- self.fk(k,xi(i-1))
                    xi(i).CrowdingDistanceListK.append(di/q)
                    xi(i).PreviousList.append(xi(i-1))
                    xi(i).NextList.append(xi(i+1))
                xi(0).CrowdingDistanceListK.append(float('inf'))
                xi(0).NextList.append(xi(1))
                xi(0).PreviousList.append(xi(-1))
                xi(-1).CrowdingDistanceListK.append(float('inf'))
                xi(-1).NextList.append(xi(0))
                xi(-1).PreviousList.append(xi(-2))
            else:
                for i in range(0,self.N):
                    xi(i).PreviousList.append(-1)
                    xi(i).NextList.append(-1)
            
            
        # Giving the final distance for every individual by summing on all objectives
        for i in range(self.N):
            self.ListF[i].CalculateCrowdingDistance()

    def update(self, x : Individual):
        for k in range(self.m):
            if x.PreviousList[k] != -1:
                if x.CrowdingDistanceListK[k] == float('inf'):
                    self.updateINF(k , x)
                else:
                    self.updatenotINF(k , x)

    def updateINF(self, k : int , x : Individual):
        q = self.fk(k,x.PreviousList[k]) - self.fk(k,x.NextList[k])
        print(f'')
        self.ListQ[k] = q 
        x.NextList[k].PreviousList[k] = x.PreviousList[k]
        x.PreviousList[k].NextList[k] = x.NextList[k]
        xi = x.NextList[k]
        for i in range(1,self.N-1):
            xi.CrowdingDistanceListK[k] = ( self.fk(k,xi.NextList[k])- self.fk(k,xi.PreviousList[k]) ) / q
            xi = xi.NextList[k]
        x.NextList[k].CrowdingDistanceListK[k] = float('inf')
        x.PreviousList[k].CrowdingDistanceListK[k] = float('inf')


    def updatenotINF(self, k : int , x : Individual):
        x.NextList[k].PreviousList[k] = x.PreviousList[k]
        x.PreviousList[k].NextList[k] = x.NextList[k]
        x.NextList[k].CrowdingDistanceListK[k] += ( self.fk(k,x) - self.fk(k,x.PreviousList[k]) )/self.ListQ[k]
        x.PreviousList[k].CrowdingDistanceListK[k] += ( -self.fk(k,x) + self.fk(k,x.NextList[k]) )/self.ListQ[k]

            

# tests
if __name__ == "__main__":

    def f(x):
        return LOTZ.LOTZm(2,x)
    A : list[Individual] = Sample.GenerateIndividual(4,5) 
    B = [Individual([0,1,1,0]) for k in range(5)]
    CD1 = CD(f,A)
    CD1.CD()
    for k in A:
        print(k)
        print(k.CrowdingDistance)
        print(k.PreviousList)
        print(k.NextList)
    CD1.update(A[0])
    print( " HEYYY ")
    for k in A:
        print(k)
        print(k.CrowdingDistance)
        print(k.PreviousList)
        print(k.NextList)
    
    


 
    