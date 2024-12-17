import random 
from Individual import Individual
from Value import Value
from LOTZ import LOTZ

class Sample:
    
    def GenerateValue(m, N):
        SampleList = []
        for k in range(N):
            SampleK = [ random.gauss(0,1) for i in range(m) ]
            SampleList.append(Value(SampleK))
        return SampleList
    
    def GenerateIndividual(n, N):
        SampleList = []
        for k in range(N):
            SampleK = [ random.choice([0,1]) for i in range(n) ]
            SampleList.append(Individual(SampleK))
        return SampleList
    
    if __name__ == "__main__":
        
        #Testing the comparisons
        #value1 = Value([0,1,2])
        #value2 = Value([0,1,2])
        #value3 = Value([1,2,3])
        #value4 = Value([0,0,3])
        #print(value1 < value4)
        
        #indiv1 =  Individual([1,1,1,0,0,1,0,1,0,1,0,0])
        #print( LOTZ.LOTZm(6,indiv1))
        
        #indivRandom = GenerateIndividual(24, 1)[0]
        #print(indivRandom)
        #print(LOTZ.LOTZm(6,indivRandom))
        print()