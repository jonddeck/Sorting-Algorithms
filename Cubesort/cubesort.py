"""
Cubesort Algorithm

Time Complexity: O(n log n) - average case, O(n) - best case
Space Complexity: O(n)

Description:
Cubesort is an in-place cache-oblivious sorting algorithm designed to be
efficient with modern CPU cache hierarchies and predictable branch patterns.

Note: This is a simplified educational version.
"""

def cubesort(arr):
    """
    Sorts an array using cubesort algorithm (simplified version).
    
    Args:
        arr: List of elements to sort
    
    Returns:
        Sorted list
    """
    if len(arr) <= 1:
        return arr
    
    # Adaptive approach: detect data characteristics
    if is_reverse_sorted(arr):
        arr.reverse()
    
    # Use a hybrid approach for different data distributions
    cubesort_recursive(arr, 0, len(arr) - 1)
    return arr


def is_reverse_sorted(arr):
    """Check if array is reverse sorted."""
    if len(arr) < 2:
        return False
    
    for i in range(len(arr) - 1):
        if arr[i] < arr[i + 1]:
            return False
    return True


def cubesort_recursive(arr, low, high):
    """Recursively sorts subarrays."""
    if high - low < 16:
        # Use insertion sort for small arrays
        insertion_sort_range(arr, low, high)
    else:
        # Divide into three parts and sort recursively
        len_third = (high - low) // 3
        
        mid1 = low + len_third
        mid2 = low + 2 * len_third
        
        cubesort_recursive(arr, low, mid1)
        cubesort_recursive(arr, mid1 + 1, mid2)
        cubesort_recursive(arr, mid2 + 1, high)
        
        # Merge the sorted parts
        merge_three_parts(arr, low, mid1, mid2, high)


def merge_three_parts(arr, low, mid1, mid2, high):
    """Merges three sorted parts."""
    # Create temporary array
    temp = []
    i, j, k = low, mid1 + 1, mid2 + 1
    
    # Merge all three parts
    while i <= mid1 and j <= mid2 and k <= high:
        if arr[i] <= arr[j]:
            if arr[i] <= arr[k]:
                temp.append(arr[i])
                i += 1
            else:
                temp.append(arr[k])
                k += 1
        else:
            if arr[j] <= arr[k]:
                temp.append(arr[j])
                j += 1
            else:
                temp.append(arr[k])
                k += 1
    
    # Handle remaining elements
    while i <= mid1 and j <= mid2:
        if arr[i] <= arr[j]:
            temp.append(arr[i])
            i += 1
        else:
            temp.append(arr[j])
            j += 1
    
    while i <= mid1 and k <= high:
        if arr[i] <= arr[k]:
            temp.append(arr[i])
            i += 1
        else:
            temp.append(arr[k])
            k += 1
    
    while j <= mid2 and k <= high:
        if arr[j] <= arr[k]:
            temp.append(arr[j])
            j += 1
        else:
            temp.append(arr[k])
            k += 1
    
    while i <= mid1:
        temp.append(arr[i])
        i += 1
    
    while j <= mid2:
        temp.append(arr[j])
        j += 1
    
    while k <= high:
        temp.append(arr[k])
        k += 1
    
    # Copy back
    for idx, val in enumerate(temp):
        arr[low + idx] = val


def insertion_sort_range(arr, low, high):
    """Insertion sort for a subarray."""
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
        sorted_arr = cubesort(arr)
        print(f"Original: {original}")
        print(f"Sorted:   {sorted_arr}\n")
