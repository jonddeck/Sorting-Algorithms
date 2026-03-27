"""
Cocktail Shaker Sort Algorithm (Bidirectional Bubble Sort)

Time Complexity: O(n²) - average and worst case, O(n) - best case
Space Complexity: O(1)

Description:
Cocktail Shaker Sort is a variation of bubble sort that sorts in both directions
on each pass through the array, improving performance on certain datasets.

Use Cases:
- Small datasets
- Nearly sorted data
- Educational purposes
"""

def cocktail_shaker_sort(arr):
    """
    Sorts an array using cocktail shaker sort algorithm.
    
    Args:
        arr: List of elements to sort
    
    Returns:
        Sorted list
    """
    n = len(arr)
    swapped = True
    start = 0
    end = n - 1
    
    while swapped:
        swapped = False
        
        # Forward pass (left to right)
        for i in range(start, end):
            if arr[i] > arr[i + 1]:
                arr[i], arr[i + 1] = arr[i + 1], arr[i]
                swapped = True
        
        if not swapped:
            break
        
        end -= 1
        swapped = False
        
        # Backward pass (right to left)
        for i in range(end - 1, start - 1, -1):
            if arr[i] > arr[i + 1]:
                arr[i], arr[i + 1] = arr[i + 1], arr[i]
                swapped = True
        
        start += 1
    
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
        sorted_arr = cocktail_shaker_sort(arr)
        print(f"Original: {original}")
        print(f"Sorted:   {sorted_arr}\n")
