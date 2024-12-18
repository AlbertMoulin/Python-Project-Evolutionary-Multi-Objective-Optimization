from LOTZ import LOTZ
from Individual import Individual
from Sample import Sample
from NDS import Nds
from CrowdingDistance import CD
import random


class NSGA:

    def NSGA(f,n,m, N):
        P = Sample.GenerateIndividual(n,N)
        OptFront = LOTZ.GenerateOptimalFrontLOTZm(n,m)
        t=0
        while not NSGA.AinB(P,OptFront) and t< 9*n**2:
            for k in range(N):
                Lk = random.choice(P).individual.copy()
                for i in range(n):
                    if random.uniform(0,1) < 1/n :
                        Lk[i] = 1-Lk[i]
                P.append(Individual(Lk))
            F = Nds.NdSorting(P,f)
            P = []
            i = 0
            while (len(P) + len(F[i]) < N):
                P = P + F[i]
            while(len(P)<N):
                FiCD = CD(f,F[i])
                CrowdingDistance = FiCD.CD()
                SortedIndex = sorted(range(len(F[i])),key=lambda index: CrowdingDistance[index])
                P.append(F[i][SortedIndex.pop()])
            t +=1
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

    n = 60
    m = 6
    N = 4*m
    def f(x):
        return LOTZ.LOTZm(m,x)
    
    print(NSGA.NSGA(f,n,m,N))