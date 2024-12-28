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

    # Defining the function returning only the k-th objective
    def fk(self, k : int, x : Individual) -> float:
        return self.f(x).value[k]
    
    def CalculateCrowdingDistanceK(self, k : int):
        # Sort the indicies by values on objective k
        IndiciesSortedByK = sorted(range(self.N), key=lambda index: self.fk(k, self.ListF[index]) )

        # function giving the i-th highest individual for objective k
        def xi(i : int) -> Individual:
                return self.ListF[IndiciesSortedByK[i]]
        
        # Calculate difference between the highest and lowest
        q = self.fk(k,xi(-1))- self.fk(k,xi(0))

        self.ListQ[k] = q

        # Verify if individuals are all equal on objective k
        if q == 0:
            self.CDKallequal(k)
        else:
            self.CDKnotequal(k, xi)



    def CDKallequal(self, k : int):
        # If they are all equal the crowding distance is 0 for every individual
        for i in self.ListF:
            i.CrowdingDistanceListK[k] = 0
            i.PreviousList[k] = " "
            i.NextList[k] = " "



    def CDKnotequal(self, k : int , xi : Callable[[int],Individual]):
        # Calculate crowding distance for the lowest individual
        xi(0).CrowdingDistanceListK[k] = float('inf')
        xi(0).PreviousList[k] = "NoPrevious"
        xi(0).NextList[k] = xi(1)
        # Calculate crowding distance for the highest individual
        xi(self.N-1).CrowdingDistanceListK[k] = float('inf')
        xi(self.N-1).NextList[k] = "NoNext"
        xi(self.N-1).PreviousList[k] = xi(self.N-2)
        # Calculate crowding distance for everyone in between
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

    def update(self, x : Individual):
        # Loop on all objectives
        for k in range(self.m):
            # Differenciate between if the individual is the highest lowest or in between
            if x.PreviousList[k] == ' ' and x.NextList[k] == ' ':
                continue
            elif x.PreviousList[k] == "NoPrevious":
                self.updatefirst(k, x)
            elif x.NextList[k] == "NoNext":
                self.updatelast(k,x)
            else:
                self.updatenormal(k, x)
        
        self.ListF.remove(x)
        self.N += -1

    # If the individual is the lowest for objective k we need to update every individual
    def updatefirst(self, k : int ,x0 : Individual ):
        # find the new lowest and highest value
        x1 = x0.NextList[k]
        xinf = x0
        while(xinf.NextList[k] != "NoNext"):
            xinf = xinf.NextList[k]
        #Update lowest value
        x1.CrowdingDistanceListK[k] = float('inf')
        x1.PreviousList[k] = "NoPrevious"
        # Calculate crowding distance
        q = self.fk(k,xinf) - self.fk(k,x1)
        if q == 0:
            self.CDKallequal(k)
            for i in self.ListF:
                i.CalculateCrowdingDistance()
        else:
            self.ListQ[k] = q
            self.updateCDnotequal(k,x1)
        
            while (x1.NextList[k] != "NoNext"):
                x1.CalculateCrowdingDistance()
                x1 = x1.NextList[k]
        
        x0.CrowdingDistanceListK[k] = 'Updated out'
        x0.NextList[k] = 'Updated out'
        x0.PreviousList[k] = 'Updated out'
    
    # Same for updating highest value
    def updatelast(self, k : int ,xinf : Individual ):

        xinfnv = xinf.PreviousList[k]
        x0 = xinf
        while(x0.PreviousList[k] != "NoPrevious"):
            x0 = x0.PreviousList[k]
        #Update xinfnv
        xinfnv.CrowdingDistanceListK[k] = float('inf')
        xinfnv.NextList[k] = "NoNext"
        #Update x0

        q = self.fk(k,xinfnv) - self.fk(k,x0)
        if q == 0:
            self.CDKallequal(k)
            for i in self.ListF:
                i.CalculateCrowdingDistance()
        else:
            self.ListQ[k] = q
            self.updateCDnotequal(k,x0)
            while (x0.NextList[k] != "NoNext"):
                x0.CalculateCrowdingDistance()
                x0 = x0.NextList[k]
        
        xinf.CrowdingDistanceListK[k] = 'Updated out'
        xinf.NextList[k] = 'Updated out'
        xinf.PreviousList[k] = 'Updated out'
    
    # If they are now all equal
    def updateCDnotequal(self, k : int,x1 : Individual):
        if x1.PreviousList[k] == "NoPrevious":
            x1 = x1.NextList[k]
        while(x1.NextList[k] != "NoNext"):

            dx = self.fk(k,x1.NextList[k]) - self.fk(k,x1.PreviousList[k])

            x1.CrowdingDistanceListK[k] = dx / self.ListQ[k]

            x1 = x1.NextList[k]

    # If the value is in between we just need to update two values
    def updatenormal(self, k : int , x : Individual):
        xN = x.NextList[k]
        xP = x.PreviousList[k]
        x.NextList[k] = 'Updated out'
        x.PreviousList[k] = 'Updated out'
        x.CrowdingDistanceListK[k] = 'Updated out'
        #Update the next element
        xN.PreviousList[k] = xP
        if xN.CrowdingDistanceListK[k] != float('inf'):
            dxN = self.fk(k,xN.NextList[k]) - self.fk(k,xN.PreviousList[k])
            xN.CrowdingDistanceListK[k] = dxN/self.ListQ[k]
            xN.CalculateCrowdingDistance()
        #Update the previous element
        xP.NextList[k] = xN
        if xP.CrowdingDistanceListK[k] != float('inf'):
            dxP = self.fk(k,xP.NextList[k]) - self.fk(k,xP.PreviousList[k])
            xP.CrowdingDistanceListK[k] = dxP/self.ListQ[k]
            xP.CalculateCrowdingDistance()
            

# Testing the functions
if __name__ == "__main__":
    random.seed(8)

    # Verify crowding distance for random set
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



    # Verify the updating
    for i in range(18):
        CD1.update(A[0])
    print("    heyyyyyyyy    ")
    for i in A:
        print(i)
        print(i.CrowdingDistanceListK)
        print(i.PreviousList)
        print(i.NextList)
        print(i.CrowdingDistance)

    
    


 
    