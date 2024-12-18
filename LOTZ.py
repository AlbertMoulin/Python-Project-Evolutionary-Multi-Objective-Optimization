from Individual import Individual
from Value import Value
from Sample import Sample

class LOTZ:
    
    # Define LOTZ 
    def LOTZdeux(Individu : Individual) -> Value:
        n = len(Individu.individual)
        i = 0
        j = n -1
        #Count number of 1
        while (i< n and Individu.individual[i] == 1):
            i +=1
        
        #Count number of 0 
        while (j>-1 and Individu.individual[j] == 0):
            j -= 1
            
        return Value([i,n-1-j])
    
    def LOTZm(m: int, Individu : Individual) -> Value:
        n = len(Individu.individual)
        
        # Verify that m verifies all conditions
        if m%2 != 0 or (2*n)%m != 0:
            return ValueError("m is not adapted")
        
        np = (2*n)//m
        
        List = [0 for k in range(m)]
        
        # Calculates LOTZ function for every section of length np of the list
        for k in range(0,m//2):
            listK = Individu.individual[np*k: np*(k+1) ]
            
            lotzK = LOTZ.LOTZdeux( Individual( listK )) 
            
            List[2*k], List[2*k+1] = lotzK.value
            
        return Value(List)
    
    def GenerateOptimalFrontLOTZ(n : int):
        optimalFront = []
        for k in range(n+1):
            optimalSolutionk = []
            for i in range(k):
                optimalSolutionk.append(1)
            for i in range(k, n):
                optimalSolutionk.append(0)
            optimalFront.append(Individual(optimalSolutionk))
        return optimalFront 
    
    def GOFLOTZmAux(m2 , optimalFrontnp):
        if m2 == 1:
            return optimalFrontnp
        optimalFrontm2 = []
        for i in LOTZ.GOFLOTZmAux(m2-1, optimalFrontnp):
            for j in optimalFrontnp:
                optimalFrontm2.append(i+j)
        return optimalFrontm2
    
    def GenerateOptimalFrontLOTZm(n : int, m : int):

        if m%2 != 0 or (2*n)%m != 0:
            return ValueError("m is not adapted")
        
        np = (2*n)//m
        
        optimalFrontnp = LOTZ.GenerateOptimalFrontLOTZ(np)

        return LOTZ.GOFLOTZmAux(m//2 , optimalFrontnp)
    
    


if __name__ == "__main__":
        
        
    indiv1 =  Individual([1,1,1,0,0,1,0,1,0,1,0,0])
    print( LOTZ.LOTZm(6,indiv1))
        
    indivRandom = Sample.GenerateIndividual(24, 1)[0]
    print(indivRandom)


    print(LOTZ.GenerateOptimalFrontLOTZm(12,4))
    