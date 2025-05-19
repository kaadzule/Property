class PriorityQueue:
    """Priority queue for sorting properties by multiple criteria"""
    
    def __init__(self, comparator=None):
        """Initialize empty priority queue"""
        self.queue = []
        self.size = 0
        
        # If comparator not specified, use default (lower price = higher priority)
        self.comparator = comparator if comparator else lambda x, y: x.price < y.price
    
    def parent(self, i):
        """Return parent index"""
        return (i - 1) // 2
    
    def left_child(self, i):
        """Return left child index"""
        return 2 * i + 1
    
    def right_child(self, i):
        """Return right child index"""
        return 2 * i + 2
    
    def get_top(self):
        """Return element with highest priority without removing it"""
        if self.size <= 0:
            return None
        return self.queue[0]
    
    def extract_top(self):
        """Remove and return element with highest priority"""
        if self.size <= 0:
            return None
        
        top_item = self.queue[0]
        self.queue[0] = self.queue[self.size - 1]
        self.size -= 1
        self.queue.pop()
        
        if self.size > 0:
            self._heapify_down(0)
        
        return top_item
    
    def insert(self, item):
        """Insert new element into queue"""
        self.queue.append(item)
        self.size += 1
        self._heapify_up(self.size - 1)
    
    def _heapify_up(self, i):
        """Move element up to maintain heap property"""
        parent_idx = self.parent(i)
        
        # If we're at root node or element is already in correct position
        if i == 0 or self.comparator(self.queue[parent_idx], self.queue[i]):
            return
        
        # Swap with parent and continue
        self.queue[i], self.queue[parent_idx] = self.queue[parent_idx], self.queue[i]
        self._heapify_up(parent_idx)
    
    def _heapify_down(self, i):
        """Move element down to maintain heap property"""
        top_idx = i
        left_idx = self.left_child(i)
        right_idx = self.right_child(i)
        
        # Check if left child has higher priority
        if left_idx < self.size and self.comparator(self.queue[left_idx], self.queue[top_idx]):
            top_idx = left_idx
        
        # Check if right child has higher priority
        if right_idx < self.size and self.comparator(self.queue[right_idx], self.queue[top_idx]):
            top_idx = right_idx
        
        # If highest priority is not current, swap and continue
        if top_idx != i:
            self.queue[i], self.queue[top_idx] = self.queue[top_idx], self.queue[i]
            self._heapify_down(top_idx)