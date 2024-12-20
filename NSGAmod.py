from LOTZ import LOTZ
from Individual import Individual
from Sample import Sample
from NDS import Nds
from CDmod import CDmod
import random
from NSGA import NSGA


class NSGAmod:

    def NSGAmod(f,n):
        m = len(f(Sample.GenerateIndividual(n,1)[0]).value)
        OptFront = LOTZ.GenerateOptimalFrontLOTZm(n,m)
        N = len(OptFront)*4
        P = Sample.GenerateIndividual(n,N)
        t=0
        count1 = 0
        count2 = 0
        while not NSGA.AinB(OptFront,P) and t< 9*n**2:
            for k in range(N):
                Lk = random.choice(P).individual.copy()
                for i in range(n):
                    count1 +=1
                    if random.uniform(0,1) < 1/n :
                        count2+=1
                        Lk[i] = 1-Lk[i]
                P.append(Individual(Lk))
            F = Nds.NdSorting(P,f)
            P = []
            i = 0
            while (i<len(F)) and (len(P) + len(F[i]) < N):
                P = P + F[i]
                i = i+1
            i = i-1

            while(len(P)<N):
                FiCD = CDmod(f,F[i])
                CrowdingDistance = FiCD.CDmod()
                SortedIndex = sorted(range(len(F[i])),key=lambda index: CrowdingDistance[index])
                P.append(F[i][SortedIndex.pop()])
            t +=1
            print(t)
        return P

    
if __name__ == "__main__":
    print()