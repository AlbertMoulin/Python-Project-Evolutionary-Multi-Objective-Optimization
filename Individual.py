import random

class Individual:
    
    individual : list[int]
    CrowdingDistance : float
    CrowdingDistanceListK : list[float]
    NextList : list["Individual"]
    PreviousList : list["Individual"]
    
    def __init__(self, individual : list[int]):
        self.individual = individual
        self.CrowdingDistance = 0
        self.CrowdingDistanceListK = []
        self.NextList = []
        self.PreviousList = []
    
    def __str__(self):
        return self.individual.__str__()
    
    def __repr__(self):
        return self.individual.__str__()
    
    def __add__(self, other):

        if not isinstance(other, Individual):
            return ValueError("You are trying to add an Individual with some other type")
        return Individual(self.individual + other.individual)
    
    def mutate(self):
        n = len(self.individual)
        Lk = self.individual.copy()
        # Mutate individual's list
        for i in range(n):
            if random.uniform(0,1) < 1/n :
                Lk[i] = 1-Lk[i]
        return Individual(Lk)

    def CalculateCrowdingDistance(self) -> None:
        self.CrowdingDistance = sum(self.CrowdingDistanceListK)


    
if __name__ == "__main__":
    indiv1 = Individual([0,1])
    indiv2 = Individual([0,1,2,84])
    indiv1.CrowdingDistanceListK = [1,1,1]
    for k in range(5):
        print(indiv1.mutate())
    indiv1.CalculateCrowdingDistance()
    print(indiv1.CrowdingDistance)