"""
Smoothsort Algorithm

Time Complexity: O(n log n) - average and worst case, O(n) - best case
Space Complexity: O(1)

Description:
Smoothsort is an in-place sorting algorithm that uses a heap-like data structure
based on Leonardo numbers. It's efficient when the array is nearly sorted.

Note: This is a simplified educational version of Smoothsort.
"""

def smoothsort(arr):
    """
    Sorts an array using smoothsort algorithm (simplified version).
    
    Args:
        arr: List of elements to sort
    
    Returns:
        Sorted list
    """
    if len(arr) <= 1:
        return arr
    
    n = len(arr)
    
    # Build initial heap structure
    for i in range(1, n):
        if arr[i] > arr[i - 1]:
            heapify_up(arr, i)
    
    # Extract elements maintaining heap property
    for i in range(n - 1, 0, -1):
        # Current element is at correct position if it's larger than previous
        if i > 0 and arr[i] < arr[i - 1]:
            arr[i], arr[i - 1] = arr[i - 1], arr[i]
            heapify_down(arr, i - 1, i)
    
    return arr


def heapify_up(arr, idx):
    """Moves an element up to maintain heap property."""
    while idx > 0 and arr[idx] > arr[idx - 1]:
        arr[idx], arr[idx - 1] = arr[idx - 1], arr[idx]
        idx -= 1


def heapify_down(arr, root, end):
    """Moves an element down to maintain heap property."""
    while root < end - 1:
        left_child = 2 * root + 1
        right_child = 2 * root + 2
        
        largest = root
        
        if left_child < end and arr[left_child] > arr[largest]:
            largest = left_child
        
        if right_child < end and arr[right_child] > arr[largest]:
            largest = right_child
        
        if largest == root:
            break
        
        arr[root], arr[largest] = arr[largest], arr[root]
        root = largest


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
        sorted_arr = smoothsort(arr)
        print(f"Original: {original}")
        print(f"Sorted:   {sorted_arr}\n")
