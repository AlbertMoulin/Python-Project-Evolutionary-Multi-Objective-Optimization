from Individual import Individual
from Value import Value
from typing import Callable
from Sample import Sample
from LOTZ import LOTZ
import random

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
        self.ListQ = [0]*self.m
        for i in ListF:
            i.CrowdingDistanceListK = [0]*self.m
            i.PreviousList = [0]*self.m
            i.NextList = [0]*self.m

    def fk(self, k : int, x : Individual) -> float:
        return self.f(x).value[k]
    
    def CalculateCrowdingDistanceK(self, k : int):
        IndiciesSortedByK = sorted(range(self.N), key=lambda index: self.fk(k, self.ListF[index]) )

        def xi(i : int) -> Individual:
                return self.ListF[IndiciesSortedByK[i]]
        
        q = self.fk(k,xi(-1))- self.fk(k,xi(0))

        self.ListQ[k] = q

        if q == 0:
            self.CDKallequal(k)
        else:
            self.CDKnotequal(k, xi)



    def CDKallequal(self, k : int):

        for i in self.ListF:
            i.PreviousList[k] = " "
            i.NextList[k] = " "



    def CDKnotequal(self, k : int , xi : Callable[[int],Individual]):
        
        xi(0).CrowdingDistanceListK[k] = float('inf')
        xi(0).PreviousList[k] = "NoPrevious"
        xi(0).NextList[k] = xi(1)
        xi(self.N-1).CrowdingDistanceListK[k] = float('inf')
        xi(self.N-1).NextList[k] = "NoNext"
        xi(self.N-1).PreviousList[k] = xi(self.N-2)
        for i in range(1,self.N-1):
            di = self.fk(k,xi(i+1))- self.fk(k,xi(i-1))
            xi(i).CrowdingDistanceListK[k] = di / self.ListQ[k]
            xi(i).NextList[k] = xi(i+1)
            xi(i).PreviousList[k] = xi(i-1)
            

    # Crowding distance function
    def CalculateCrowdingDistance(self) -> None:
        # Loop on all objectives
        for k in range(self.m):
            self.CalculateCrowdingDistanceK(k)
        # Giving the final distance for every individual by summing on all objectives
        for i in range(self.N):
            self.ListF[i].CalculateCrowdingDistance()

    # def update(self, x : Individual):
    #     for k in range(self.m):
    #         if x.state == 1:
    #             self.updateINF(k , x)
    #             x.PreviousList[k].CalculateCrowdingDistance
    #             x.NextList[k].CalculateCrowdingDistance
    #         if x.state == 0:
    #             self.updatenotINF(k , x)
    #             x.PreviousList[k].CalculateCrowdingDistance
    #             x.NextList[k].CalculateCrowdingDistance
    #     self.ListF.remove(x)
    #     self.N += -1

    # def updateINF(self, k : int , x : Individual):
    #     q = self.fk(k,x.PreviousList[k]) - self.fk(k,x.NextList[k])
    #     self.ListQ[k] = q 
    #     if q == 0:
    #         x.NextList[k].PreviousList[k] = x.PreviousList[k]
    #         x.PreviousList[k].NextList[k] = x.NextList[k]
    #         xi = x
    #         while xi.state[k] != 3 :
    #             xi.CrowdingDistanceListK[k] = 0
    #             xi.state[k] = 3
    #             xi = xi.NextList[k]
    #     else : 
    #         x.NextList[k].PreviousList[k] = x.PreviousList[k]
    #         x.PreviousList[k].NextList[k] = x.NextList[k]
    #         xi = x.NextList[k]
    #         for i in range(1,self.N-2):
    #             xi.CrowdingDistanceListK[k] = ( self.fk(k,xi.NextList[k])- self.fk(k,xi.PreviousList[k]) ) / q
    #             xi = xi.NextList[k]
    #         x.NextList[k].CrowdingDistanceListK[k] = float('inf')
    #         x.PreviousList[k].CrowdingDistanceListK[k] = float('inf')


    # def updatenotINF(self, k : int , x : Individual):
    #     x.NextList[k].PreviousList[k] = x.PreviousList[k]
    #     x.PreviousList[k].NextList[k] = x.NextList[k]
    #     x.NextList[k].CrowdingDistanceListK[k] += ( self.fk(k,x) - self.fk(k,x.PreviousList[k]) )/self.ListQ[k]
    #     x.PreviousList[k].CrowdingDistanceListK[k] += ( -self.fk(k,x) + self.fk(k,x.NextList[k]) )/self.ListQ[k]

            

# tests
if __name__ == "__main__":
    random.seed(8)

    def f(x):
        return LOTZ.LOTZm(2,x)
    A : list[Individual] = Sample.GenerateIndividual(4,18) 
    B = [Individual([0,1,1,0]) for k in range(5)]
    CD1 = CD(f,A)
    print(A)
    CD1.CalculateCrowdingDistance()

    for i in A:
        print(i)
        print(i.CrowdingDistanceListK)
        print(i.PreviousList)
        print(i.NextList)
        print(i.CrowdingDistance)
    


 
    