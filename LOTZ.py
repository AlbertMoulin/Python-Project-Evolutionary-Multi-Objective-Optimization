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
    
if __name__ == "__main__":
        
        
    indiv1 =  Individual([1,1,1,0,0,1,0,1,0,1,0,0])
    print( LOTZ.LOTZm(6,indiv1))
        
    indivRandom = Sample.GenerateIndividual(24, 1)[0]
    print(indivRandom)
    print(LOTZ.LOTZm(6,indivRandom))
    