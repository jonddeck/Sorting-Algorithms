"""
Statsort Algorithm (Non-Comparison Sort)

Time Complexity: O(n) - in expectation
Space Complexity: O(n)

Description:
Statsort is a distribution-based sorting algorithm that uses statistical information
about the data to guide the sorting process. It's particularly efficient for real-world data.

Note: This is a simplified educational version focusing on the core concept.
"""

def statsort(arr):
    """
    Sorts an array using statsort algorithm (simplified version).
    
    Args:
        arr: List of elements to sort
    
    Returns:
        Sorted list
    """
    if len(arr) <= 1:
        return arr
    
    # Gather statistics
    min_val = min(arr)
    max_val = max(arr)
    
    if min_val == max_val:
        return arr
    
    # Use distribution information to guide bucket creation
    n = len(arr)
    sample_size = min(n, 1000)
    
    # Sample to estimate distribution
    sample = arr[:sample_size] if n >= sample_size else arr
    
    # Estimate range and number of buckets
    estimated_buckets = estimate_optimal_buckets(sample, n)
    
    # Create buckets based on distribution
    buckets = [[] for _ in range(estimated_buckets)]
    
    # Distribute elements
    for num in arr:
        if estimated_buckets == 1:
            bucket_idx = 0
        else:
            bucket_idx = min(estimated_buckets - 1, 
                           int((num - min_val) * (estimated_buckets - 1) / (max_val - min_val + 1)))
        buckets[bucket_idx].append(num)
    
    # Sort individual buckets
    result = []
    for bucket in buckets:
        insertion_sort(bucket)
        result.extend(bucket)
    
    return result


def estimate_optimal_buckets(sample, total_size):
    """
    Estimates optimal number of buckets based on sample statistics.
    
    Args:
        sample: Sample of data
        total_size: Total size of data
    
    Returns:
        Estimated optimal bucket count
    """
    if len(sample) <= 1:
        return 1
    
    # Calculate coefficient of variation as a measure of dispersion
    mean = sum(sample) / len(sample)
    variance = sum((x - mean) ** 2 for x in sample) / len(sample)
    std_dev = variance ** 0.5
    
    if mean == 0:
        cv = 0
    else:
        cv = std_dev / abs(mean)
    
    # Use CV to estimate bucket count
    # Higher CV means more spread, suggesting more buckets
    bucket_count = max(1, int(0.45 * total_size * (1 + cv / 2)))
    
    return bucket_count


def insertion_sort(arr):
    """Insertion sort on array."""
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
        [100, 10, 50, 25, 75, 30, 80],  # Different range
    ]
    
    for arr in test_cases:
        if arr:
            original = arr.copy()
            sorted_arr = statsort(arr)
            print(f"Original: {original}")
            print(f"Sorted:   {sorted_arr}\n")
