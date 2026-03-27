"""
Introsort Algorithm (Hybrid Sort)

Time Complexity: O(n log n) - all cases
Space Complexity: O(log n)

Description:
Introsort (introspective sort) is a hybrid algorithm that combines Quicksort,
Heapsort, and Insertion Sort. It starts with Quicksort and switches to Heapsort
if recursion depth exceeds a limit, with Insertion Sort for small arrays.

Use Cases:
- Default sorting in C++ (std::sort)
- When guaranteed O(n log n) is needed with in-place sorting
- General-purpose sorting algorithm
"""

def introsort(arr):
    """
    Sorts an array using introsort algorithm.
    
    Args:
        arr: List of elements to sort
    
    Returns:
        Sorted list
    """
    max_depth = 2 * len(bin(len(arr))) - 5  # 2 * log(n)
    intro_sort_helper(arr, 0, len(arr) - 1, max_depth)
    return arr


def intro_sort_helper(arr, low, high, max_depth):
    """
    Helper function for introsort that manages algorithm selection.
    
    Args:
        arr: Array to sort
        low: Starting index
        high: Ending index
        max_depth: Maximum recursion depth before switching to heapsort
    """
    while high - low > 1:
        if max_depth == 0:
            # Switch to heapsort if max depth exceeded
            heapsort(arr, low, high)
            return
        elif high - low < 16:
            # Use insertion sort for small arrays
            insertion_sort_range(arr, low, high)
            return
        else:
            # Use quicksort
            max_depth -= 1
            pivot_idx = partition(arr, low, high)
            intro_sort_helper(arr, pivot_idx + 1, high, max_depth)
            high = pivot_idx - 1


def partition(arr, low, high):
    """Partitions array around pivot."""
    pivot = arr[high]
    i = low - 1
    
    for j in range(low, high):
        if arr[j] < pivot:
            i += 1
            arr[i], arr[j] = arr[j], arr[i]
    
    arr[i + 1], arr[high] = arr[high], arr[i + 1]
    return i + 1


def heapsort(arr, low, high):
    """Performs heapsort on a subarray."""
    n = high - low + 1
    
    for i in range((n // 2 - 1), -1, -1):
        heapify(arr, low, high, i)
    
    for i in range(high, low, -1):
        arr[low], arr[i] = arr[i], arr[low]
        heapify(arr, low, i - 1, 0)


def heapify(arr, low, high, i):
    """Maintains heap property."""
    largest = i
    left = 2 * i + 1
    right = 2 * i + 2
    
    if left <= high and arr[left] > arr[largest]:
        largest = left
    
    if right <= high and arr[right] > arr[largest]:
        largest = right
    
    if largest != i:
        arr[i], arr[largest] = arr[largest], arr[i]
        heapify(arr, low, high, largest)


def insertion_sort_range(arr, low, high):
    """Performs insertion sort on a subarray."""
    for i in range(low + 1, high + 1):
        key = arr[i]
        j = i - 1
        while j >= low and arr[j] > key:
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
        [3],               # Single element
        []                 # Empty array
    ]
    
    for arr in test_cases:
        original = arr.copy()
        sorted_arr = introsort(arr)
        print(f"Original: {original}")
        print(f"Sorted:   {sorted_arr}\n")
