from LOTZ import LOTZ
from Individual import Individual
from Sample import Sample
from NDS import Nds
from CrowdingDistance import CD
import random


class NSGA:

    def NSGA(f,n):
        # Retrieving the value of m through the function f
        m = len(f(Sample.GenerateIndividual(n,1)[0]).value)
        # Generating optimal front for n and m
        OptFront = LOTZ.GenerateOptimalFrontLOTZm(n,m)
        # Defining the number of individual as 4 times the size of the optimal front
        N = len(OptFront)*4
        # Generating random individuals
        P = Sample.GenerateIndividual(n,N)
        # Initialize number of step
        t=0
        while not NSGA.AinB(OptFront,P) and t< 9*n**2:
            # Picked N individuals randomly and mutate them 
            for k in range(N):
                # Select an individual and copy it's list
                Lk = random.choice(P).individual.copy()
                #Mutate
                for i in range(n):
                    if random.uniform(0,1) < 1/n :
                        Lk[i] = 1-Lk[i]
                P.append(Individual(Lk))
            # Sort through non dominated sorting
            F = Nds.NdSorting(P,f)
            # Add fronts in increasing order until adding N individuals
            P = []
            i = 0
            while (i<len(F)) and (len(P) + len(F[i]) <= N):
                P = P + F[i]
                i = i+1
            # If we dont have N individuals we add individuals by decreasing order of crowding distance until reaching a size of N
            if len(P) < N:
                FiCD = CD(f,F[i])
                CrowdingDistance = FiCD.CD()
                SortedIndex = sorted(range(len(F[i])),key=lambda index: CrowdingDistance[index])
                for k in range(N-len(P)):
                    FiCD.update()
                    P.append(F[i][SortedIndex.pop()])
            t +=1
        return P

    def AinB(A,B):
        for x in A:
            boolx = True
            i=0
            while boolx and i< len(B):
                boolx = not x.individual == B[i].individual
                i = i+1
            if boolx:
                return False
        return True
    
if __name__ == "__main__":

    A = Sample.GenerateIndividual(2,3)
    B = Sample.GenerateIndividual(2,2)
    print(A)
    print(B)
    print(NSGA.AinB(A,B))

    random.seed(8)
    n = 6
    m = 2
    print(f'test with n = {n} and m = {m}')
    def f(x):
        return LOTZ.LOTZm(m,x)
    print(NSGA.NSGA(f,n))

    n = 6
    m = 6
    print(f'test with n = {n} and m = {m}')
    def f(x):
        return LOTZ.LOTZm(m,x)
    print(NSGA.NSGA(f,n))

    n = 9
    m = 2
    print(f'test with n = {n} and m = {m}')
    def f(x):
        return LOTZ.LOTZm(m,x)
    print(NSGA.NSGA(f,n))

    n = 9
    m = 6
    print(f'test with n = {n} and m = {m}')
    def f(x):
        return LOTZ.LOTZm(m,x)
    print(NSGA.NSGA(f,n))

    