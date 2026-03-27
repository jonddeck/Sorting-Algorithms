"""
Comb Sort Algorithm

Time Complexity: O(n log n) - average case, O(n²) - worst case
Space Complexity: O(1)

Description:
Comb Sort is an improvement over Bubble Sort that uses a gap sequence to compare
and swap elements that are far apart, reducing the number of turtles (small values at end).

Use Cases:
- Simple improvement over bubble sort
- Educational purposes
- When a simple in-place algorithm is needed
"""

def comb_sort(arr):
    """
    Sorts an array using comb sort algorithm.
    
    Args:
        arr: List of elements to sort
    
    Returns:
        Sorted list
    """
    n = len(arr)
    gap = n
    swapped = True
    
    while gap > 1 or swapped:
        # Calculate gap
        gap = int(gap / 1.3)
        if gap < 1:
            gap = 1
        
        swapped = False
        
        # Perform comparisons and swaps with the current gap
        for i in range(n - gap):
            if arr[i] > arr[i + gap]:
                arr[i], arr[i + gap] = arr[i + gap], arr[i]
                swapped = True
    
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
        sorted_arr = comb_sort(arr)
        print(f"Original: {original}")
        print(f"Sorted:   {sorted_arr}\n")
