"""
Shellsort Algorithm (Shell Sort)

Time Complexity: O(n log n) to O(n²) - depends on gap sequence
Space Complexity: O(1)

Description:
Shellsort is a generalization of insertion sort that allows the exchange of items
that are far apart. The algorithm uses a sequence of gaps that decrease to 1.

Use Cases:
- Medium-sized arrays
- When adaptive sorting is needed
- Simple implementation with good performance on most datasets
"""

def shellsort(arr):
    """
    Sorts an array using shellsort algorithm with Knuth's gap sequence.
    
    Args:
        arr: List of elements to sort
    
    Returns:
        Sorted list
    """
    n = len(arr)
    
    # Knuth's gap sequence: 1, 4, 13, 40, 121, ...
    # Start with a gap of 1 and keep multiplying by 3 + 1
    gap = 1
    while gap < n // 3:
        gap = gap * 3 + 1
    
    # Start with the largest gap and reduce by dividing by 3
    while gap > 0:
        # Perform insertion sort for elements at distance 'gap'
        for i in range(gap, n):
            temp = arr[i]
            j = i
            
            while j >= gap and arr[j - gap] > temp:
                arr[j] = arr[j - gap]
                j -= gap
            
            arr[j] = temp
        
        # Reduce the gap
        gap //= 3
    
    return arr


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
        sorted_arr = shellsort(arr)
        print(f"Original: {original}")
        print(f"Sorted:   {sorted_arr}\n")
