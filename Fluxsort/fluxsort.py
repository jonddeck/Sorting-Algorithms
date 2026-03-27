"""
Fluxsort Algorithm

Time Complexity: O(n log n) - average case
Space Complexity: O(n)

Description:
Fluxsort is a modern sorting algorithm that aims to be cache-efficient and
adaptive to different data distributions and memory characteristics.

Note: This is a simplified educational version. The actual algorithm is more complex.
"""

def fluxsort(arr):
    """
    Sorts an array using fluxsort algorithm (simplified version).
    
    Args:
        arr: List of elements to sort
    
    Returns:
        Sorted list
    """
    if len(arr) <= 1:
        return arr
    
    # Simplified version: use hybrid approach similar to timsort
    min_run = calculate_min_run(len(arr))
    
    # Sort runs with insertion sort
    runs = []
    for start in range(0, len(arr), min_run):
        end = min(start + min_run, len(arr))
        run = arr[start:end]
        insertion_sort(run)
        runs.append(run)
    
    # Merge runs
    while len(runs) > 1:
        merged_runs = []
        for i in range(0, len(runs), 2):
            if i + 1 < len(runs):
                merged = merge(runs[i], runs[i + 1])
                merged_runs.append(merged)
            else:
                merged_runs.append(runs[i])
        runs = merged_runs
    
    return runs[0] if runs else []


def calculate_min_run(n):
    """Calculates minimum run length based on array size."""
    r = 0
    while n >= 64:
        r |= n & 1
        n >>= 1
    return n + r


def insertion_sort(arr):
    """Sorts array in-place using insertion sort."""
    for i in range(1, len(arr)):
        key = arr[i]
        j = i - 1
        while j >= 0 and arr[j] > key:
            arr[j + 1] = arr[j]
            j -= 1
        arr[j + 1] = key


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
        sorted_arr = fluxsort(arr)
        print(f"Original: {original}")
        print(f"Sorted:   {sorted_arr}\n")
