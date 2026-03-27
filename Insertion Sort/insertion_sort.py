"""
Insertion Sort Algorithm

Time Complexity: O(n²) - average and worst case, O(n) - best case
Space Complexity: O(1)

Description:
Insertion Sort builds the sorted array one item at a time by inserting each element
into its correct position among the already sorted elements.

Use Cases:
- Small arrays or nearly sorted data
- Online sorting (can sort as data arrives)
- Adaptive sorting (efficient on nearly sorted data)
"""

def insertion_sort(arr):
    """
    Sorts an array using insertion sort algorithm.
    
    Args:
        arr: List of elements to sort
    
    Returns:
        Sorted list
    """
    # Traverse through 1 to len(arr)
    for i in range(1, len(arr)):
        key = arr[i]
        j = i - 1
        
        # Move elements greater than key one position ahead
        while j >= 0 and arr[j] > key:
            arr[j + 1] = arr[j]
            j -= 1
        
        # Insert the key at its correct position
        arr[j + 1] = key
    
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
        sorted_arr = insertion_sort(arr)
        print(f"Original: {original}")
        print(f"Sorted:   {sorted_arr}\n")
