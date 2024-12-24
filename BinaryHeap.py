from Individual import Individual
from Sample import Sample
from CrowdingDistance import CD
from LOTZ import LOTZ

class BinaryHeap:

    heap : list[Individual]
    FiCD : CD

    def insert(self, x: Individual):
        self.heap.append(x)
        self.bubbleup(len(self.heap)-1)

    def bubbleup(self, index):
        while index > 0:
            parent_index = (index - 1) // 2
            if self.heap[parent_index].CrowdingDistance < self.heap[index].CrowdingDistance:
                self.heap[index], self.heap[parent_index] = self.heap[parent_index], self.heap[index]
                index = parent_index
            else:
                break


    def __init__(self, FiCD : CD):
        self.heap = []
        self.FiCD = FiCD
        for k in FiCD.ListF:
            self.insert(k)

    def extract_max(self):
        if not self.heap:
            raise IndexError("Heap is empty")
        
        max_element = self.heap[0]

        # Replacing first element by last
        self.heap[0] = self.heap[-1]
        self.heap.pop()

        # Recalculating the crowding distances
        self.FiCD.update(max_element)
        
        if self.heap:
            self._bubble_down(0)

        return max_element

    def _bubble_down(self, index):

        size = len(self.heap)

        while True:
            highest = index
            left_child = 2 * index + 1
            right_child = 2 * index + 2

            if left_child < size and self.heap[left_child].CrowdingDistance > self.heap[highest].CrowdingDistance:
                highest = left_child

            if right_child < size and self.heap[right_child].CrowdingDistance > self.heap[highest].CrowdingDistance:
                highest = right_child

            # Si l'index actuel n'est pas le plus petit, échanger
            if highest != index:
                self.heap[index], self.heap[highest] = self.heap[highest], self.heap[index]
                index = highest
            else:
                break

if __name__ == "__main__":
    # Générer des données pour tester le BinaryHeap
    ListF = Sample.GenerateIndividual(3, 10)
    FiCD = CD(LOTZ.LOTZdeux, ListF)
    FiCD.CD()
    print("Liste générée :", ListF)
    for k in ListF:
        print(k.CrowdingDistance)
    heap = BinaryHeap(FiCD)

    print("BinaryHeap initial :", heap.heap)

    # Extraire les éléments minimaux
    print("Extraction des éléments dans l'ordre croissant :")
    while heap.heap:
        min_element = heap.extract_max()
        print(f"Élément extrait : {min_element}, BinaryHeap après extraction : {heap.heap}")