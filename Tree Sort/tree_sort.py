"""
Tree Sort Algorithm

Time Complexity: O(n log n) - average case, O(n²) - worst case (unbalanced)
Space Complexity: O(n)

Description:
Tree Sort uses a Binary Search Tree (BST) to sort elements. Elements are inserted
into a BST and then an in-order traversal yields sorted elements.

Use Cases:
- When a balanced BST is available
- Need for both sorting and maintaining sorted data
- Educational purposes

Note: Performance depends on tree balance. A self-balancing tree (AVL, Red-Black)
ensures O(n log n) time complexity.
"""

class TreeNode:
    """Node in the BST."""
    def __init__(self, value):
        self.value = value
        self.left = None
        self.right = None


class BinarySearchTree:
    """Binary Search Tree implementation."""
    def __init__(self):
        self.root = None
    
    def insert(self, value):
        """Inserts a value into the BST."""
        if self.root is None:
            self.root = TreeNode(value)
        else:
            self._insert_recursive(self.root, value)
    
    def _insert_recursive(self, node, value):
        """Helper method to recursively insert a value."""
        if value < node.value:
            if node.left is None:
                node.left = TreeNode(value)
            else:
                self._insert_recursive(node.left, value)
        else:
            if node.right is None:
                node.right = TreeNode(value)
            else:
                self._insert_recursive(node.right, value)
    
    def inorder_traversal(self, node=None):
        """Performs in-order traversal to get sorted elements."""
        if node is None:
            node = self.root
        
        result = []
        if node:
            result.extend(self.inorder_traversal(node.left))
            result.append(node.value)
            result.extend(self.inorder_traversal(node.right))
        
        return result


def tree_sort(arr):
    """
    Sorts an array using tree sort algorithm.
    
    Args:
        arr: List of elements to sort
    
    Returns:
        Sorted list
    """
    if len(arr) <= 1:
        return arr
    
    # Create a BST and insert all elements
    bst = BinarySearchTree()
    for element in arr:
        bst.insert(element)
    
    # Perform in-order traversal to get sorted array
    return bst.inorder_traversal()


# Example usage
if __name__ == "__main__":
    # Test with various arrays
    test_cases = [
        [64, 34, 25, 12, 22, 11, 90],
        [5, 2, 8, 1, 9],
        [1, 2, 3, 4, 5],  # Already sorted
        [5, 4, 3, 2, 1],  # Reverse sorted
        [3],               # Single element
        []                 # Empty array
    ]
    
    for arr in test_cases:
        original = arr.copy()
        sorted_arr = tree_sort(arr)
        print(f"Original: {original}")
        print(f"Sorted:   {sorted_arr}\n")
