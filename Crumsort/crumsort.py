"""
Crumsort Algorithm

Time Complexity: O(n log n) - average case
Space Complexity: O(n)

Description:
Crumsort (Crash Resistant Unstable MergeSort) is an optimization of merge sort
that handles certain edge cases efficiently and minimizes cache misses.

Note: This is a simplified educational version.
"""

def crumsort(arr):
    """
    Sorts an array using crumsort algorithm (simplified version).
    
    Args:
        arr: List of elements to sort
    
    Returns:
        Sorted list
    """
    if len(arr) <= 1:
        return arr
    
    # Use adaptive strategy based on array characteristics
    if is_nearly_sorted(arr):
        # For nearly sorted arrays, use insertion sort
        return insertion_sort(arr.copy())
    else:
        # For general arrays, use merge sort
        return merge_sort(arr)


def is_nearly_sorted(arr):
    """Checks if array is nearly sorted (heuristic)."""
    if len(arr) < 2:
        return True
    
    sorted_pairs = 0
    for i in range(len(arr) - 1):
        if arr[i] <= arr[i + 1]:
            sorted_pairs += 1
    
    return sorted_pairs > len(arr) * 0.8


def insertion_sort(arr):
    """Sorts array using insertion sort."""
    for i in range(1, len(arr)):
        key = arr[i]
        j = i - 1
        while j >= 0 and arr[j] > key:
            arr[j + 1] = arr[j]
            j -= 1
        arr[j + 1] = key
    return arr


def merge_sort(arr):
    """Sorts array using merge sort."""
    if len(arr) <= 1:
        return arr
    
    mid = len(arr) // 2
    left = merge_sort(arr[:mid])
    right = merge_sort(arr[mid:])
    
    return merge(left, right)


def merge(left, right):
    """Merges two sorted arrays."""
    result = []
    i = j = 0
    
    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1
    
    result.extend(left[i:])
    result.extend(right[j:])
    
    return result


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
        sorted_arr = crumsort(arr)
        print(f"Original: {original}")
        print(f"Sorted:   {sorted_arr}\n")
