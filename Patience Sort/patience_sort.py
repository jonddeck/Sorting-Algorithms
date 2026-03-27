"""
Patience Sort Algorithm

Time Complexity: O(n log n) - average case with binary search
Space Complexity: O(n)

Description:
Patience Sort simulates the game of Patience. It builds piles and uses binary search
to place each element in the correct pile, then merges piles to get sorted result.

Use Cases:
- Finding longest increasing subsequence (LIS)
- Small to medium datasets
- When subsequence properties are needed
"""

import bisect


def patience_sort(arr):
    """
    Sorts an array using patience sort algorithm.
    
    Args:
        arr: List of elements to sort
    
    Returns:
        Sorted list
    """
    if len(arr) <= 1:
        return arr
    
    piles = []
    
    # Create piles by placing each element optimally
    for element in arr:
        # Find the leftmost pile whose top is >= element
        pos = bisect.bisect_left(piles, element)
        
        if pos == len(piles):
            # No suitable pile found, create a new one
            piles.append([element])
        else:
            # Place element on the found pile
            piles[pos].append(element)
    
    # Merge all piles into sorted result
    # Extract the top element from each pile and create final sorted array
    result = []
    
    # Get the last element (top) from each pile
    tops = [pile[-1] for pile in piles]
    
    # Use a systematic approach to extract and sort
    while piles:
        # Find minimum top element
        min_idx = 0
        for i in range(1, len(piles)):
            if piles[i][-1] < piles[min_idx][-1]:
                min_idx = i
        
        # Add to result and remove from pile
        result.append(piles[min_idx].pop())
        
        # Remove empty piles
        piles = [pile for pile in piles if pile]
    
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
        sorted_arr = patience_sort(arr)
        print(f"Original: {original}")
        print(f"Sorted:   {sorted_arr}\n")
