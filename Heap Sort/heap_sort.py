"""
Heap Sort Algorithm

Time Complexity: O(n log n) - all cases
Space Complexity: O(1)

Description:
Heap Sort builds a max heap from the array, then repeatedly extracts the maximum
element and places it at the end of the sorted portion.

Use Cases:
- When guaranteed O(n log n) is required
- Systems with memory constraints (in-place sorting)
- Priority queue implementation
"""

def heap_sort(arr):
    """
    Sorts an array using heap sort algorithm.
    
    Args:
        arr: List of elements to sort
    
    Returns:
        Sorted list
    """
    n = len(arr)
    
    # Build a max heap
    for i in range(n // 2 - 1, -1, -1):
        heapify(arr, n, i)
    
    # Extract elements from heap one by one
    for i in range(n - 1, 0, -1):
        # Move current root (maximum) to end
        arr[0], arr[i] = arr[i], arr[0]
        
        # Heapify the reduced heap
        heapify(arr, i, 0)
    
    return arr


def heapify(arr, n, i):
    """
    Maintains the heap property for a subtree rooted at index i.
    
    Args:
        arr: Array representing the heap
        n: Size of the heap
        i: Index of the root of the subtree
    """
    largest = i
    left = 2 * i + 1
    right = 2 * i + 2
    
    # Compare with left child
    if left < n and arr[left] > arr[largest]:
        largest = left
    
    # Compare with right child
    if right < n and arr[right] > arr[largest]:
        largest = right
    
    # If largest is not root, swap and heapify
    if largest != i:
        arr[i], arr[largest] = arr[largest], arr[i]
        heapify(arr, n, largest)


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
        sorted_arr = heap_sort(arr)
        print(f"Original: {original}")
        print(f"Sorted:   {sorted_arr}\n")
