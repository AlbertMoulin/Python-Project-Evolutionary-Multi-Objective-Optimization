from Individual import Individual
from CrowdingDistanceMod import CD
from Sample import Sample
from LOTZ import LOTZ

class BinaryHeap:
    heap : list
    FiCD : CD

    def insert(self, i):
        self.heap.append(i)
        self._bubble_up(len(self.heap) - 1)

    def _bubble_up(self, index):
        while index > 0:
            parent_index = (index - 1) // 2
            if self.FiCD.CDList[self.heap[index]] < self.FiCD.CDList[self.heap[parent_index]]:
                self.heap[index], self.heap[parent_index] = self.heap[parent_index], self.heap[index]
                index = parent_index
            else:
                break

    def __init__(self, FiCD : CD):
        self.heap = []
        self.FiCD = FiCD
        for k in range(self.FiCD.N):
            self.insert(k)
    
    def __repr__(self):
        return self.heap.__repr__()

    def extract_min(self):
        if len(self.heap) == 0:
            raise IndexError("Heap is empty")
        
        min_element = self.heap[0]

        self.heap[0] = self.heap[-1]
        self.heap.pop()

        if len(self.heap) > 0:
            self._bubble_down(0)

        self.FiCD.removed(min_element)
        return min_element
    
    def _bubble_down(self, index):
        size = len(self.heap)
        while True:
            smallest = index
            left_child = 2 * index + 1
            right_child = 2 * index + 2

            if left_child < size and self.FiCD.CDList[self.heap[left_child]] < self.FiCD.CDList[self.heap[smallest]]:
                smallest = left_child

            if right_child < size and self.FiCD.CDList[self.heap[right_child]] < self.FiCD.CDList[self.heap[smallest]]:
                smallest = right_child

            if smallest != index:
                self.heap[index], self.heap[smallest] = self.heap[smallest], self.heap[index]
                index = smallest
            else:
                break

if __name__ == "__main__":
    ListF = Sample.GenerateIndividual(3,10)
    FiCD = CD(LOTZ.LOTZdeux, ListF)
    print(f'ListF : {ListF}')
    print(f'Liste des distances : {FiCD.CDList}')
    heap = BinaryHeap(FiCD)
    print(f'heap : {heap}')
    while heap.heap:
        min_element = heap.extract_min()
        print(min_element)
        print(heap)
        print(FiCD.CDList)
