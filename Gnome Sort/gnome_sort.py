"""
Gnome Sort Algorithm

Time Complexity: O(n²) - average and worst case, O(n) - best case
Space Complexity: O(1)

Description:
Gnome Sort (stupid sort) is similar to insertion sort but with a different approach.
It compares an element with the previous one and swaps if needed, then moves back to check.

Use Cases:
- Educational purposes
- Small datasets
- Simple to understand and implement
"""

def gnome_sort(arr):
    """
    Sorts an array using gnome sort algorithm.
    
    Args:
        arr: List of elements to sort
    
    Returns:
        Sorted list
    """
    n = len(arr)
    i = 0
    
    while i < n:
        # If current element is already in correct position or is first element
        if i == 0 or arr[i] >= arr[i - 1]:
            i += 1
        else:
            # Swap with previous element and move back
            arr[i], arr[i - 1] = arr[i - 1], arr[i]
            i -= 1
    
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
        sorted_arr = gnome_sort(arr)
        print(f"Original: {original}")
        print(f"Sorted:   {sorted_arr}\n")
