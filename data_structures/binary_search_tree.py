class BSTNode:
    """Binary Search Tree Node"""
    
    def __init__(self, key, value=None):
        """Initialize BST node"""
        self.key = key          # Key (price or other parameter)
        self.value = value if value else []  # Value list (properties with this key)
        self.left = None        # Left subtree (smaller values)
        self.right = None       # Right subtree (larger values)
    
    def add_value(self, value):
        """Add value to node"""
        if value not in self.value:  # Avoid duplicates
            self.value.append(value)


class BinarySearchTree:
    """Binary Search Tree for property indexing"""
    
    def __init__(self):
        """Initialize empty BST"""
        self.root = None
        self.size = 0  # Tree size for analysis
    
    def insert(self, key, value):
        """Insert new key and value into tree"""
        if self.root is None:
            self.root = BSTNode(key, [value])
            self.size += 1
            return
        
        current = self.root
        while True:
            if key == current.key:
                # If key already exists, add new value
                current.add_value(value)
                return
            elif key < current.key:
                # If smaller, go left
                if current.left is None:
                    current.left = BSTNode(key, [value])
                    self.size += 1
                    return
                current = current.left
            else:
                # If larger, go right
                if current.right is None:
                    current.right = BSTNode(key, [value])
                    self.size += 1
                    return
                current = current.right
    
    def find(self, key):
        """Find values with the specified key"""
        current = self.root
        while current is not None:
            if key == current.key:
                return current.value
            elif key < current.key:
                current = current.left
            else:
                current = current.right
        return None  # Not found
    
    def in_order_traversal(self, node=None, result=None):
        """Traverse tree in order (in-order traversal), sorting by key"""
        if node is None:
            node = self.root
        if result is None:
            result = []
        
        if node is None:
            return result
        
        # First left subtree
        self.in_order_traversal(node.left, result)
        
        # Current node
        for value in node.value:
            result.append(value)
        
        # Then right subtree
        self.in_order_traversal(node.right, result)
        
        return result
    
    def find_range(self, min_key, max_key):
        """Find all properties in the specified price range"""
        result = []
        self._find_range_helper(self.root, min_key, max_key, result)
        return result
    
    def _find_range_helper(self, node, min_key, max_key, result):
        """Helper function for range search"""
        if node is None:
            return
        
        # If current node is in range, check left subtree
        if min_key < node.key:
            self._find_range_helper(node.left, min_key, max_key, result)
        
        # Add current node if it's in range
        if min_key <= node.key <= max_key:
            result.extend(node.value)
        
        # If current node is in range, check right subtree
        if node.key < max_key:
            self._find_range_helper(node.right, min_key, max_key, result)