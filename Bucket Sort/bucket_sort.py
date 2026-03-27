"""
Bucket Sort Algorithm (Non-Comparison Sort)

Time Complexity: O(n + k) - average case, O(n²) - worst case
Space Complexity: O(n + k)

Description:
Bucket Sort divides input into buckets, sorts them individually (often using
insertion sort or recursively), then concatenates them. Variants for uniform 
distribution and integer keys provided.

Use Cases:
- Uniformly distributed floating-point numbers
- Integer ranges
- Disk I/O optimization
"""

def bucket_sort_uniform(arr):
    """
    Sorts array using bucket sort for uniformly distributed floating-point numbers.
    
    Args:
        arr: List of numbers between 0 and 1
    
    Returns:
        Sorted list
    """
    if len(arr) <= 1:
        return arr
    
    n = len(arr)
    buckets = [[] for _ in range(n)]
    
    # Distribute elements into buckets
    for num in arr:
        # Ensure num is between 0 and 1
        if num == 1.0:
            index = n - 1
        else:
            index = int(n * num)
        buckets[index].append(num)
    
    # Sort individual buckets and concatenate
    sorted_arr = []
    for bucket in buckets:
        sorted_arr.extend(sorted(bucket))
    
    return sorted_arr


def bucket_sort_integers(arr, bucket_range=None):
    """
    Sorts array using bucket sort for integers within a range.
    
    Args:
        arr: List of integers
        bucket_range: Size of each bucket (default: optimal)
    
    Returns:
        Sorted list
    """
    if len(arr) <= 1:
        return arr
    
    min_val = min(arr)
    max_val = max(arr)
    
    if bucket_range is None:
        bucket_range = max(1, (max_val - min_val) // len(arr) + 1)
    
    num_buckets = (max_val - min_val) // bucket_range + 1
    buckets = [[] for _ in range(num_buckets)]
    
    # Distribute elements into buckets
    for num in arr:
        index = (num - min_val) // bucket_range
        buckets[index].append(num)
    
    # Sort individual buckets (using insertion sort)
    sorted_arr = []
    for bucket in buckets:
        insertion_sort(bucket)
        sorted_arr.extend(bucket)
    
    return sorted_arr


def insertion_sort(arr):
    """Performs insertion sort on array in-place."""
    for i in range(1, len(arr)):
        key = arr[i]
        j = i - 1
        while j >= 0 and arr[j] > key:
            arr[j + 1] = arr[j]
            j -= 1
        arr[j + 1] = key


# Example usage
if __name__ == "__main__":
    # Test uniform distribution
    print("=== Bucket Sort (Uniform Distribution) ===")
    test_uniform = [
        [0.897, 0.565, 0.656, 0.1234, 0.665, 0.3434],
        [0.1, 0.2, 0.3, 0.4, 0.5],
    ]
    
    for arr in test_uniform:
        original = arr.copy()
        sorted_arr = bucket_sort_uniform(arr)
        print(f"Original: {original}")
        print(f"Sorted:   {sorted_arr}\n")
    
    # Test integer keys
    print("\n=== Bucket Sort (Integer Keys) ===")
    test_integers = [
        [64, 34, 25, 12, 22, 11, 90],
        [5, 2, 8, 1, 9],
        [100, 50, 75, 25, 150],
    ]
    
    for arr in test_integers:
        original = arr.copy()
        sorted_arr = bucket_sort_integers(arr)
        print(f"Original: {original}")
        print(f"Sorted:   {sorted_arr}\n")
