"""
Odd-Even Sort Algorithm (Brick Sort)

Time Complexity: O(n²) - average and worst case, O(n) - best case
Space Complexity: O(1)

Description:
Odd-Even Sort is a variation of bubble sort that compares and swaps all odd/even
indexed pairs of adjacent elements, then even/odd indexed pairs, alternating.

Use Cases:
- Small datasets
- Parallel sorting (odd and even phases can be parallelized)
- Educational purposes
"""

def odd_even_sort(arr):
    """
    Sorts an array using odd-even sort algorithm.
    
    Args:
        arr: List of elements to sort
    
    Returns:
        Sorted list
    """
    n = len(arr)
    sorted_flag = False
    
    while not sorted_flag:
        sorted_flag = True
        
        # Odd phase: compare all odd/even indexed pairs
        for i in range(1, n - 1, 2):
            if arr[i] > arr[i + 1]:
                arr[i], arr[i + 1] = arr[i + 1], arr[i]
                sorted_flag = False
        
        # Even phase: compare all even/odd indexed pairs
        for i in range(0, n - 1, 2):
            if arr[i] > arr[i + 1]:
                arr[i], arr[i + 1] = arr[i + 1], arr[i]
                sorted_flag = False
    
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
        sorted_arr = odd_even_sort(arr)
        print(f"Original: {original}")
        print(f"Sorted:   {sorted_arr}\n")
