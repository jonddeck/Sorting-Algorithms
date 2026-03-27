"""
Quick Sort Algorithm

Time Complexity: O(n log n) - average case, O(n²) - worst case
Space Complexity: O(log n) - due to recursion stack

Description:
Quick Sort is a divide-and-conquer algorithm that selects a pivot element and
partitions the array around it, then recursively sorts the partitions.

Use Cases:
- General-purpose sorting for large datasets
- In-place sorting with low memory overhead
- Cache-friendly due to sequential access
"""

def quick_sort(arr, low=0, high=None):
    """
    Sorts an array using quick sort algorithm.
    
    Args:
        arr: List of elements to sort
        low: Starting index
        high: Ending index
    
    Returns:
        Sorted list
    """
    if high is None:
        high = len(arr) - 1
    
    if low < high:
        # Partition the array and get the pivot index
        pivot_index = partition(arr, low, high)
        
        # Recursively sort the left partition
        quick_sort(arr, low, pivot_index - 1)
        
        # Recursively sort the right partition
        quick_sort(arr, pivot_index + 1, high)
    
    return arr


def partition(arr, low, high):
    """
    Partitions the array around a pivot element.
    
    Args:
        arr: Array to partition
        low: Starting index
        high: Ending index
    
    Returns:
        Index of the pivot element
    """
    pivot = arr[high]
    i = low - 1
    
    for j in range(low, high):
        if arr[j] < pivot:
            i += 1
            arr[i], arr[j] = arr[j], arr[i]
    
    arr[i + 1], arr[high] = arr[high], arr[i + 1]
    return i + 1


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
        sorted_arr = quick_sort(arr)
        print(f"Original: {original}")
        print(f"Sorted:   {sorted_arr}\n")
