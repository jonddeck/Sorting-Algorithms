"""
Counting Sort Algorithm (Non-Comparison Sort)

Time Complexity: O(n + k) - where n is number of elements, k is range of input
Space Complexity: O(k)

Description:
Counting Sort counts the occurrence of each value and reconstructs the sorted array
based on these counts. It's not a comparison-based algorithm.

Use Cases:
- Integers within a specific range
- Small integer values
- As a subroutine in Radix Sort
"""

def counting_sort(arr):
    """
    Sorts an array using counting sort algorithm.
    
    Args:
        arr: List of non-negative integers to sort
    
    Returns:
        Sorted list
    """
    if len(arr) <= 1:
        return arr
    
    # Find the range of input
    max_val = max(arr)
    min_val = min(arr)
    range_size = max_val - min_val + 1
    
    # Create count array
    count = [0] * range_size
    
    # Store count of each element
    for num in arr:
        count[num - min_val] += 1
    
    # Change count[i] so that it contains actual position
    for i in range(1, range_size):
        count[i] += count[i - 1]
    
    # Build output array
    output = [0] * len(arr)
    
    # Traverse array backwards to maintain stability
    for i in range(len(arr) - 1, -1, -1):
        index = count[arr[i] - min_val] - 1
        output[index] = arr[i]
        count[arr[i] - min_val] -= 1
    
    return output


# Example usage
if __name__ == "__main__":
    # Test with various arrays
    test_cases = [
        [64, 34, 25, 12, 22, 11, 90],
        [5, 2, 8, 1, 9],
        [1, 2, 3, 4, 5],  # Already sorted
        [5, 4, 3, 2, 1],  # Reverse sorted
        [3],               # Single element
        [10, 10, 10, 1, 2]  # Duplicates
    ]
    
    for arr in test_cases:
        if arr:  # Skip empty array test
            original = arr.copy()
            sorted_arr = counting_sort(arr)
            print(f"Original: {original}")
            print(f"Sorted:   {sorted_arr}\n")
