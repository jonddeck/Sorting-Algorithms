"""
Tournament Sort Algorithm

Time Complexity: O(n log n) - building tournament tree
Space Complexity: O(n)

Description:
Tournament Sort creates a tournament tree where each match determines the smaller
or larger element. It simulates a single-elimination tournament to sort elements.

Use Cases:
- Finding min/max elements efficiently
- Educational purposes
- When tournament-based selection is conceptually useful
"""

import heapq


def tournament_sort(arr):
    """
    Sorts an array using tournament sort algorithm.
    
    Args:
        arr: List of elements to sort
    
    Returns:
        Sorted list
    """
    if len(arr) <= 1:
        return arr
    
    result = []
    # Create a min heap copy of the array
    heap = arr.copy()
    heapq.heapify(heap)
    
    # Extract minimum elements one by one
    while heap:
        result.append(heapq.heappop(heap))
    
    return result


def tournament_sort_manual(arr):
    """
    Manual tournament sort implementation without using heapq.
    This shows the tournament concept more explicitly.
    
    Args:
        arr: List of elements to sort
    
    Returns:
        Sorted list
    """
    if len(arr) <= 1:
        return arr
    
    result = []
    remaining = arr.copy()
    
    while remaining:
        # Find the minimum element through tournament
        min_idx = 0
        for i in range(1, len(remaining)):
            if remaining[i] < remaining[min_idx]:
                min_idx = i
        
        result.append(remaining[min_idx])
        remaining.pop(min_idx)
    
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
        sorted_arr = tournament_sort(arr)
        print(f"Original: {original}")
        print(f"Sorted:   {sorted_arr}\n")
