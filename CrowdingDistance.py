from Individual import Individual
from Value import Value
from typing import Callable
from Sample import Sample
from LOTZ import LOTZ

class CD:
    
    ListF : list
    f : Callable
    ListV : list
    m : int
    N : int

    def __init__(self, f, ListF):
        self.f = f
        self.ListF = ListF
        self.m = len(f(self.ListF[0]).value)
        self.N = len(ListF)

    def CD(self):
        MatrixCD = [[0 for i in range(self.N)] for k in range(self.m)]
        for k in range(self.m):
            def fk(x):
                return self.f(x).value[k]
            IndiciesSortedByK = sorted(range(self.N), key=lambda index: fk(self.ListF[index]) )
            def xi(i):
                return self.ListF[IndiciesSortedByK[i]]
            MatrixCD[k][IndiciesSortedByK[0]] = float('inf')
            MatrixCD[k][IndiciesSortedByK[-1]] = float('inf')
            for i in range(1,self.N-1):
                di = fk(xi(i+1))- fk(xi(i-1))
                qi = fk(xi(-1))- fk(xi(0))
                MatrixCD[k][IndiciesSortedByK[i]] = di/qi
        Final_List = [0 for i in range(self.N)]
        print(MatrixCD)
        for i in range(self.N):
            for k in range(self.m):
                Final_List[i] += MatrixCD[k][i]
        return Final_List

if __name__ == "__main__":

    def f(x):
        return LOTZ.LOTZm(4,x)
    
    CD1 = CD(f,Sample.GenerateIndividual(12,19))
    print(CD.CD(CD1))


 
    