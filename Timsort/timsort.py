"""
Timsort Algorithm (Hybrid Sort)

Time Complexity: O(n log n) - all cases
Space Complexity: O(n)

Description:
Timsort is a hybrid stable sorting algorithm derived from merge sort and insertion sort.
It divides the array into small runs, sorts them with insertion sort, then merges them.

Use Cases:
- Default sorting in Python and Java
- Large real-world datasets
- When stable sorting is required
- Mixed data with different distributions

Note: This is a simplified version. The actual implementation is more complex.
"""

def timsort(arr, min_run=None):
    """
    Sorts an array using timsort algorithm.
    
    Args:
        arr: List of elements to sort
        min_run: Minimum run length (calculated if not provided)
    
    Returns:
        Sorted list
    """
    n = len(arr)
    
    if n <= 1:
        return arr
    
    # Calculate minimum run length
    if min_run is None:
        min_run = calculate_min_run(n)
    
    # Sort individual runs using insertion sort
    runs = []
    for start in range(0, n, min_run):
        end = min(start + min_run, n)
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
    """
    Calculates the minimum run length for timsort.
    
    Args:
        n: Size of array
    
    Returns:
        Minimum run length
    """
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
        sorted_arr = timsort(arr)
        print(f"Original: {original}")
        print(f"Sorted:   {sorted_arr}\n")
