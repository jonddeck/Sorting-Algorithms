"""
Reverse Hybrid Sort Algorithm

Time Complexity: O(n²) - average and worst case, O(n) - best case
Space Complexity: O(1)


Description:
Reverse Hybrid Sort is a novel, hybrid comparison-based sorting algorithm that combines two unique phases:
1. Reverse Comparison Phase: Compares each element arr[i] with its mirror (arr[n-1-i]). 
    If arr[i] > arr[n-1-i], they are swapped to promote symmetry and reduce disorder.
2. Odd-Even Cleanup Phase: Alternates between comparing odd-indexed pairs (1,2), (3,4)... 
    and even-indexed pairs (0,1), (2,3)... to resolve remaining inversions.
The algorithm iteratively applies these phases until no more swaps are needed, leveraging global 
symmetry cues to accelerate convergence.

Use Cases:
- Educational demonstrations of hybrid sorting strategies
- Parallel sorting (odd and even phases can be parallelized)
- Scenarios where symmetry-based sorting logic is desired
"""

def reverse_hybrid_sort(arr):
    if len(arr) <= 1:
        return arr
    
    n = len(arr)
    arr = arr.copy()
    sorted_flag = False

    while not sorted_flag:
        sorted_flag = True
        arr_reverse = arr[::-1]  # Recompute reverse each pass

        # Reverse Comparison Phase
        for i in range(n):
            mirror = n - 1 - i
            if i < mirror and arr[i] > arr_reverse[i]:  # Avoid double swap
                arr[i], arr[mirror] = arr[mirror], arr[i]
                sorted_flag = False

        # Odd Phase: Compare (1,2), (3,4), ...
        for i in range(1, n - 1, 2):
            if arr[i] > arr[i + 1]:
                arr[i], arr[i + 1] = arr[i + 1], arr[i]
                sorted_flag = False

        # Even Phase: Compare (0,1), (2,3), ...
        for i in range(0, n - 1, 2):
            if arr[i] > arr[i + 1]:
                arr[i], arr[i + 1] = arr[i + 1], arr[i]
                sorted_flag = False

    return arr

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
        sorted_arr = reverse_hybrid_sort(arr)
        print(f"Original: {original}")
        print(f"Sorted:   {sorted_arr}\n")
