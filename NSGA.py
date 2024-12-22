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
            F = Nds.NdSorting(P,f)
            P = []
            i = 0
            while (i<len(F)) and (len(P) + len(F[i]) <= N):
                P = P + F[i]
                i = i+1
            FiCD = CD(f,F[i])
            CrowdingDistance = FiCD.CD()
            SortedIndex = sorted(range(len(F[i])),key=lambda index: CrowdingDistance[index])
            while(len(P)<N):
                P.append(F[i][SortedIndex.pop()])
            t +=1
            print(t)
        return P

    def AinB(A,B):
        for x in A:
            boolx = False
            for y in B:
                boolx = boolx or x.individual == y.individual
            if not boolx:
                return False
        return True
    
if __name__ == "__main__":

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

    