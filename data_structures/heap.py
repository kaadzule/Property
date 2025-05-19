class MinHeap:
    """Min-Heap data structure for sorting properties by minimum price"""
    
    def __init__(self):
        """Initialize empty Min-Heap"""
        self.heap = []
        self.size = 0
    
    def parent(self, i):
        """Return parent index"""
        return (i - 1) // 2
    
    def left_child(self, i):
        """Return left child index"""
        return 2 * i + 1
    
    def right_child(self, i):
        """Return right child index"""
        return 2 * i + 2
    
    def get_min(self):
        """Return minimum element without removing it"""
        if self.size <= 0:
            return None
        return self.heap[0]
    
    def extract_min(self):
        """Remove and return minimum element"""
        if self.size <= 0:
            return None
        
        min_item = self.heap[0]
        self.heap[0] = self.heap[self.size - 1]
        self.size -= 1
        self.heap.pop()
        
        if self.size > 0:
            self._heapify_down(0)
        
        return min_item
    
    def insert(self, item):
        """Insert new element into heap"""
        self.heap.append(item)
        self.size += 1
        self._heapify_up(self.size - 1)
    
    def _heapify_up(self, i):
        """Move element up to maintain heap property"""
        parent_idx = self.parent(i)
        
        # If we're at root node or element is already in correct position
        if i == 0 or self.heap[parent_idx].price <= self.heap[i].price:
            return
        
        # Swap with parent and continue
        self.heap[i], self.heap[parent_idx] = self.heap[parent_idx], self.heap[i]
        self._heapify_up(parent_idx)
    
    def _heapify_down(self, i):
        """Move element down to maintain heap property"""
        min_idx = i
        left_idx = self.left_child(i)
        right_idx = self.right_child(i)
        
        # Check if left child is smaller
        if left_idx < self.size and self.heap[left_idx].price < self.heap[min_idx].price:
            min_idx = left_idx
        
        # Check if right child is smaller
        if right_idx < self.size and self.heap[right_idx].price < self.heap[min_idx].price:
            min_idx = right_idx
        
        # If minimum is not current, swap and continue
        if min_idx != i:
            self.heap[i], self.heap[min_idx] = self.heap[min_idx], self.heap[i]
            self._heapify_down(min_idx)


class MaxHeap:
    """Max-Heap data structure for sorting properties by maximum price"""
    
    def __init__(self):
        """Initialize empty Max-Heap"""
        self.heap = []
        self.size = 0
    
    def parent(self, i):
        """Return parent index"""
        return (i - 1) // 2
    
    def left_child(self, i):
        """Return left child index"""
        return 2 * i + 1
    
    def right_child(self, i):
        """Return right child index"""
        return 2 * i + 2
    
    def get_max(self):
        """Return maximum element without removing it"""
        if self.size <= 0:
            return None
        return self.heap[0]
    
    def extract_max(self):
        """Remove and return maximum element"""
        if self.size <= 0:
            return None
        
        max_item = self.heap[0]
        self.heap[0] = self.heap[self.size - 1]
        self.size -= 1
        self.heap.pop()
        
        if self.size > 0:
            self._heapify_down(0)
        
        return max_item
    
    def insert(self, item):
        """Insert new element into heap"""
        self.heap.append(item)
        self.size += 1
        self._heapify_up(self.size - 1)
    
    def _heapify_up(self, i):
        """Move element up to maintain heap property"""
        parent_idx = self.parent(i)
        
        # If we're at root node or element is already in correct position
        if i == 0 or self.heap[parent_idx].price >= self.heap[i].price:
            return
        
        # Swap with parent and continue
        self.heap[i], self.heap[parent_idx] = self.heap[parent_idx], self.heap[i]
        self._heapify_up(parent_idx)
    
    def _heapify_down(self, i):
        """Move element down to maintain heap property"""
        max_idx = i
        left_idx = self.left_child(i)
        right_idx = self.right_child(i)
        
        # Check if left child is larger
        if left_idx < self.size and self.heap[left_idx].price > self.heap[max_idx].price:
            max_idx = left_idx
        
        # Check if right child is larger
        if right_idx < self.size and self.heap[right_idx].price > self.heap[max_idx].price:
            max_idx = right_idx
        
        # If maximum is not current, swap and continue
        if max_idx != i:
            self.heap[i], self.heap[max_idx] = self.heap[max_idx], self.heap[i]
            self._heapify_down(max_idx)