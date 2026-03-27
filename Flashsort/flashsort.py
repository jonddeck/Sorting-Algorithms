"""
Flashsort Algorithm (Non-Comparison Sort)

Time Complexity: O(n) - average case, O(n²) - worst case
Space Complexity: O(n)

Description:
Flashsort is an in-place sorting algorithm that uses the distribution of elements
to achieve near-linear average-case time complexity. It redistributes elements into
buckets, then performs insertion sort on each bucket.

Use Cases:
- Large datasets with known distributions
- When memory is limited (in-place sorting)
- Uniformly distributed data
"""

def flashsort(arr):
    """
    Sorts an array using flashsort algorithm.
    
    Args:
        arr: List of comparable elements
    
    Returns:
        Sorted list
    """
    if len(arr) <= 1:
        return arr
    
    n = len(arr)
    min_val = min(arr)
    max_val = max(arr)
    
    if min_val == max_val:
        return arr
    
    # Number of buckets
    m = int(0.45 * n)
    
    # Create classification array
    L = [0] * (m + 1)
    
    # Classification phase - count elements in each bucket
    for i in range(n):
        k = int(m * (arr[i] - min_val) / (max_val - min_val + 1))
        L[k] += 1
    
    # Transform L into bucket boundaries
    for i in range(1, m + 1):
        L[i] += L[i - 1]
    
    # Permutation phase - move elements to their buckets
    i = 0
    move_count = 0
    while move_count < n:
        while i < n and arr[i] != arr[i]:  # Dummy condition
            i += 1
        
        # Get the bucket index for arr[i]
        k = int(m * (arr[i] - min_val) / (max_val - min_val + 1))
        
        # Place element in correct bucket
        while i >= L[k]:
            i += 1
            if i >= n:
                break
            k = int(m * (arr[i] - min_val) / (max_val - min_val + 1))
        
        if i >= n:
            break
        
        j = i
        while i != j and i < n:
            k = int(m * (arr[i] - min_val) / (max_val - min_val + 1))
            arr[j] = arr[L[k] - 1]
            L[k] -= 1
            j = L[k]
            move_count += 1
        
        i += 1
    
    # Insertion sort on buckets
    insertion_sort_full(arr)
    
    return arr


def insertion_sort_full(arr):
    """Insertion sort on entire array."""
    for i in range(1, len(arr)):
        key = arr[i]
        j = i - 1
        while j >= 0 and arr[j] > key:
            arr[j + 1] = arr[j]
            j -= 1
        arr[j + 1] = key


# Simplified version (more educational)
def flashsort_simplified(arr):
    """
    Simplified flashsort for educational purposes.
    
    Args:
        arr: List of elements to sort
    
    Returns:
        Sorted list
    """
    if len(arr) <= 1:
        return arr
    
    n = len(arr)
    min_val = min(arr)
    max_val = max(arr)
    
    if min_val == max_val:
        return arr
    
    # Number of buckets
    m = max(1, int(0.45 * n))
    
    # Create buckets
    buckets = [[] for _ in range(m)]
    
    # Distribute elements into buckets
    for num in arr:
        if max_val == min_val:
            bucket_idx = 0
        else:
            bucket_idx = min(m - 1, int(m * (num - min_val) / (max_val - min_val + 1)))
        buckets[bucket_idx].append(num)
    
    # Sort each bucket with insertion sort
    result = []
    for bucket in buckets:
        insertion_sort_bucket(bucket)
        result.extend(bucket)
    
    return result


def insertion_sort_bucket(arr):
    """Insertion sort on array in-place."""
    for i in range(1, len(arr)):
        key = arr[i]
        j = i - 1
        while j >= 0 and arr[j] > key:
            arr[j + 1] = arr[j]
            j -= 1
        arr[j + 1] = key


# Example usage
if __name__ == "__main__":
    # Test with various arrays
    test_cases = [
        [64, 34, 25, 12, 22, 11, 90],
        [5, 2, 8, 1, 9],
        [1, 2, 3, 4, 5],  # Already sorted
        [5, 4, 3, 2, 1],  # Reverse sorted
        [3.5, 1.2, 5.1, 2.3, 4.1],  # Floats
    ]
    
    for arr in test_cases:
        if arr:
            original = arr.copy()
            sorted_arr = flashsort_simplified(arr)
            print(f"Original: {original}")
            print(f"Sorted:   {sorted_arr}\n")
