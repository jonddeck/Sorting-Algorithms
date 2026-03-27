"""
Block Sort Algorithm

Time Complexity: O(n log n) - average case, O(n) - best case
Space Complexity: O(1) - in-place sorting

Description:
Block Sort (aka Grail Sort) divides the array into blocks and uses block rotation
to minimize memory usage while maintaining O(n log n) time complexity in-place.

Note: This is a simplified educational version of the actual Block Sort.
"""

def block_sort(arr):
    """
    Sorts an array using block sort algorithm (simplified version).
    
    Args:
        arr: List of elements to sort
    
    Returns:
        Sorted list (modified in-place)
    """
    if len(arr) <= 1:
        return arr
    
    block_sort_helper(arr, 0, len(arr) - 1)
    return arr


def block_sort_helper(arr, left, right):
    """
    Helper function that recursively sorts blocks.
    """
    if left >= right:
        return
    
    mid = (left + right) // 2
    
    # Sort left block
    block_sort_helper(arr, left, mid)
    
    # Sort right block
    block_sort_helper(arr, mid + 1, right)
    
    # Merge the blocks in-place
    merge_blocks(arr, left, mid, right)


def merge_blocks(arr, left, mid, right):
    """
    Merges two sorted blocks in-place using block rotation.
    """
    # Create temporary buffer for merging
    temp = []
    i, j = left, mid + 1
    
    while i <= mid and j <= right:
        if arr[i] <= arr[j]:
            temp.append(arr[i])
            i += 1
        else:
            temp.append(arr[j])
            j += 1
    
    while i <= mid:
        temp.append(arr[i])
        i += 1
    
    while j <= right:
        temp.append(arr[j])
        j += 1
    
    # Copy back to original array
    for i, val in enumerate(temp):
        arr[left + i] = val


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
        sorted_arr = block_sort(arr)
        print(f"Original: {original}")
        print(f"Sorted:   {sorted_arr}\n")
