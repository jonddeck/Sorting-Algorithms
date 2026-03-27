"""
Pigeonhole Sort Algorithm (Non-Comparison Sort)

Time Complexity: O(n + k) - where k is range of input
Space Complexity: O(k)

Description:
Pigeonhole Sort is a sorting algorithm that works well when the range of possible
values is not significantly larger than the number of items being sorted.

Use Cases:
- Small range of input values
- Integer sorting with limited range
- When input values are known to be bounded
"""

def pigeonhole_sort(arr):
    """
    Sorts an array using pigeonhole sort algorithm.
    
    Args:
        arr: List of non-negative integers with bounded range
    
    Returns:
        Sorted list
    """
    if len(arr) <= 1:
        return arr
    
    # Find the range of input
    min_val = min(arr)
    max_val = max(arr)
    range_size = max_val - min_val + 1
    
    # Create pigeonholes (buckets)
    pigeonholes = [[] for _ in range(range_size)]
    
    # Put elements into pigeonholes
    for num in arr:
        pigeonholes[num - min_val].append(num)
    
    # Extract sorted elements
    result = []
    for hole in pigeonholes:
        result.extend(hole)
    
    return result


def pigeonhole_sort_stable(arr):
    """
    Stable version of pigeonhole sort (maintains relative order of duplicates).
    
    Args:
        arr: List of non-negative integers
    
    Returns:
        Sorted list
    """
    if len(arr) <= 1:
        return arr
    
    min_val = min(arr)
    max_val = max(arr)
    range_size = max_val - min_val + 1
    
    # Create pigeonholes
    pigeonholes = [0] * range_size
    
    # Count occurrences
    for num in arr:
        pigeonholes[num - min_val] += 1
    
    # Change counts to actual positions
    for i in range(1, range_size):
        pigeonholes[i] += pigeonholes[i - 1]
    
    # Build output array
    output = [0] * len(arr)
    
    for i in range(len(arr) - 1, -1, -1):
        index = pigeonholes[arr[i] - min_val] - 1
        output[index] = arr[i]
        pigeonholes[arr[i] - min_val] -= 1
    
    return output


# Example usage
if __name__ == "__main__":
    # Test with various arrays
    test_cases = [
        [64, 34, 25, 12, 22, 11, 90],
        [5, 2, 8, 1, 9],
        [1, 2, 3, 4, 5],  # Already sorted
        [5, 4, 3, 2, 1],  # Reverse sorted
        [10, 10, 10, 1, 2, 2],  # Duplicates
        [8, 3, 2, 7, 4, 6, 8, 5, 2],  # More duplicates
    ]
    
    for arr in test_cases:
        if arr:
            original = arr.copy()
            sorted_arr = pigeonhole_sort(arr)
            sorted_stable = pigeonhole_sort_stable(arr)
            print(f"Original: {original}")
            print(f"Sorted:   {sorted_arr}")
            print(f"Stable:   {sorted_stable}\n")
