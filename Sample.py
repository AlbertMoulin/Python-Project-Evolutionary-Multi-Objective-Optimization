import random 
from Individual import Individual
from Value import Value

class Sample:
    
    def GenerateValue(m : int, N : int) -> list[Value]:
        SampleList = []
        for k in range(N):
            SampleK = [ random.gauss(0,1) for i in range(m) ]
            SampleList.append(Value(SampleK))
        return SampleList
    
    def GenerateIndividual(n : int, N : int) -> list[Individual]:
        SampleList = []
        for k in range(N):
            SampleK = [ random.choice([0,1]) for i in range(n) ]
            SampleList.append(Individual(SampleK))
        return SampleList
    
if __name__ == "__main__":
    print(Sample.GenerateIndividual(4,10))
    
