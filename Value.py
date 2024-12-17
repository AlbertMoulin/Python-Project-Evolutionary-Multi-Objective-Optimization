from typing import List, Dict

class Value:
    
    value : List[float]
    
    def __init__(self, value : List[float]):
        self.value = value
    
    def __str__(self):
        return self.value.__str__()
    
    def __repr__(self):
        return self.value.__str__()
    
    # define strictly dominates
    def __gt__(self, other : object) -> bool:
        
        # verify that self and other have same type
        if not isinstance(other, Value):
            return NotImplemented
        n : int = len(self.value)
        
        # verify that self and other have same list length
        if n != len(other.value):
            return ValueError("Cannot compare lists of different lengths")
        
        i=0
        # verify that self weakly dominates other and counts the number of strict domination
        for k in range(n):
            if self.value[k] < other.value[k]:
                return False
            if self.value[k] > other.value[k]:
                i+=1
        
        return i>0
    
    # define weakly dominates
    def __ge__(self, other : object) -> bool:
        
        if not isinstance(other, Value):
            return NotImplemented
        n : int = len(self.value)
        
        if n != len(other.value):
            return ValueError("Cannot compare lists of different lengths")
        
        for k in range(n):
            if self.value[k] < other.value[k]:
                return False
        
        return True
    
if __name__ == "__main__":
        
    #Testing the comparisons
    value1 = Value([0,1,2])
    value2 = Value([0,1,2])
    value3 = Value([1,2,3])
    value4 = Value([0,0,3])
    print(value1 < value4)