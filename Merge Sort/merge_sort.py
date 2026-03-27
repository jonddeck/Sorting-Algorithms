"""
Merge Sort Algorithm

Time Complexity: O(n log n) - all cases
Space Complexity: O(n)

Description:
Merge Sort is a divide-and-conquer algorithm that divides the array into halves,
recursively sorts them, and then merges the sorted halves back together.

Use Cases:
- When consistent O(n log n) performance is required
- External sorting (when data doesn't fit in memory)
- Linked lists
- Stable sorting needed
"""

def merge_sort(arr):
    """
    Sorts an array using merge sort algorithm.
    
    Args:
        arr: List of elements to sort
    
    Returns:
        Sorted list
    """
    if len(arr) <= 1:
        return arr
    
    # Divide the array into two halves
    mid = len(arr) // 2
    left = arr[:mid]
    right = arr[mid:]
    
    # Recursively sort both halves
    left = merge_sort(left)
    right = merge_sort(right)
    
    # Merge the sorted halves
    return merge(left, right)


def merge(left, right):
    """
    Merges two sorted arrays into a single sorted array.
    
    Args:
        left: First sorted array
        right: Second sorted array
    
    Returns:
        Merged sorted array
    """
    result = []
    i = j = 0
    
    # Compare elements from left and right arrays
    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1
    
    # Add remaining elements
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
        sorted_arr = merge_sort(arr)
        print(f"Original: {original}")
        print(f"Sorted:   {sorted_arr}\n")
