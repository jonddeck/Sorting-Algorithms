"""
Strand Sort Algorithm

Time Complexity: O(n²) - average and worst case, O(n) - best case (nearly sorted)
Space Complexity: O(n)

Description:
Strand Sort extracts increasing subsequences from the unsorted list and merges them
into the result. It's particularly efficient on nearly sorted data.

Use Cases:
- Nearly sorted data
- Linked lists
- When data has natural orderings already present
"""

def strand_sort(arr):
    """
    Sorts an array using strand sort algorithm.
    
    Args:
        arr: List of elements to sort
    
    Returns:
        Sorted list
    """
    if len(arr) <= 1:
        return arr
    
    result = []
    
    # Create a copy to work with
    remaining = arr.copy()
    
    while remaining:
        # Extract a strand (increasing subsequence)
        strand = [remaining[0]]
        remaining.pop(0)
        
        # Find elements that can be added to the strand
        i = 0
        while i < len(remaining):
            if remaining[i] >= strand[-1]:
                strand.append(remaining[i])
                remaining.pop(i)
            else:
                i += 1
        
        # Merge the strand with result
        result = merge(result, strand)
    
    return result


def merge(left, right):
    """
    Merges two sorted arrays.
    
    Args:
        left: First sorted array
        right: Second sorted array
    
    Returns:
        Merged sorted array
    """
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
        sorted_arr = strand_sort(arr)
        print(f"Original: {original}")
        print(f"Sorted:   {sorted_arr}\n")
