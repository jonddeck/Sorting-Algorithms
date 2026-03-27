"""
Spreadsort Algorithm (Non-Comparison Sort)

Time Complexity: O(n log n) - average case, O(n) - best case
Space Complexity: O(n)

Description:
Spreadsort is a high-performance hybrid sorting algorithm that combines the idea of
bucket sorting with a sorting algorithm to achieve better performance on real data.

Note: This is a simplified educational version of the actual Spreadsort algorithm.
"""

def spreadsort(arr):
    """
    Sorts an array using spreadsort algorithm (simplified version).
    
    Args:
        arr: List of elements to sort
    
    Returns:
        Sorted list
    """
    if len(arr) <= 1:
        return arr
    
    # Detect data type and characteristics
    return spreadsort_recursive(arr, 0)


def spreadsort_recursive(arr, depth=0):
    """
    Recursive helper for spreadsort.
    
    Args:
        arr: Array to sort
        depth: Current recursion depth
    
    Returns:
        Sorted array
    """
    if len(arr) <= 1:
        return arr
    
    if len(arr) < 16 or depth > 20:
        # Use insertion sort for small arrays or deep recursion
        return insertion_sort(arr.copy())
    
    # Use bucket-based approach
    max_val = max(arr)
    min_val = min(arr)
    
    if max_val == min_val:
        return arr
    
    # Calculate number of buckets
    range_size = max_val - min_val
    bucket_count = min(len(arr), max(1, int((range_size / len(arr)) ** 0.5)))
    
    # Create buckets
    buckets = [[] for _ in range(bucket_count)]
    
    # Distribute elements into buckets
    for num in arr:
        if bucket_count == 1:
            bucket_idx = 0
        else:
            bucket_idx = int((num - min_val) * (bucket_count - 1) / range_size)
        buckets[bucket_idx].append(num)
    
    # Sort each bucket recursively
    result = []
    for bucket in buckets:
        result.extend(spreadsort_recursive(bucket, depth + 1))
    
    return result


def insertion_sort(arr):
    """Performs insertion sort on array."""
    for i in range(1, len(arr)):
        key = arr[i]
        j = i - 1
        while j >= 0 and arr[j] > key:
            arr[j + 1] = arr[j]
            j -= 1
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
        [],                # Empty array
    ]
    
    for arr in test_cases:
        if arr:
            original = arr.copy()
            sorted_arr = spreadsort(arr)
            print(f"Original: {original}")
            print(f"Sorted:   {sorted_arr}\n")
