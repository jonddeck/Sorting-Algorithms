"""
Radix Sort Algorithm (Non-Comparison Sort)

Time Complexity: O(d * (n + k)) - where d is number of digits, n is count, k is radix
Space Complexity: O(n + k)

Description:
Radix Sort sorts numbers by processing individual digits. Includes both LSD (Least 
Significant Digit) and MSD (Most Significant Digit) variants.

Use Cases:
- Sorting integers
- Sorting strings
- External sorting
- Lexicographic sorting
"""

def radix_sort_lsd(arr):
    """
    Sorts array using Radix Sort with LSD (Least Significant Digit) approach.
    
    Args:
        arr: List of non-negative integers to sort
    
    Returns:
        Sorted list
    """
    if len(arr) <= 1:
        return arr
    
    max_val = max(arr)
    exp = 1
    
    # Process each digit position
    while max_val // exp > 0:
        arr = counting_sort_by_digit(arr, exp)
        exp *= 10
    
    return arr


def radix_sort_msd(arr, exp=None):
    """
    Sorts array using Radix Sort with MSD (Most Significant Digit) approach.
    
    Args:
        arr: List of non-negative integers to sort
        exp: Current exponent (for recursion)
    
    Returns:
        Sorted list
    """
    if len(arr) <= 1:
        return arr
    
    if exp is None:
        max_val = max(arr)
        exp = 10 ** (len(str(max_val)) - 1)
    
    if exp == 0:
        return arr
    
    # Partition by current digit
    buckets = {}
    for num in arr:
        digit = (num // exp) % 10
        if digit not in buckets:
            buckets[digit] = []
        buckets[digit].append(num)
    
    # Recursively sort each bucket
    result = []
    for digit in sorted(buckets.keys()):
        if exp >= 10:
            result.extend(radix_sort_msd(buckets[digit], exp // 10))
        else:
            result.extend(sorted(buckets[digit]))
    
    return result


def counting_sort_by_digit(arr, exp):
    """
    Counting sort used as subroutine in radix sort, based on digit at exp position.
    
    Args:
        arr: Array to sort
        exp: Current exponent (represents digit position)
    
    Returns:
        Sorted array
    """
    count = [0] * 10
    output = [0] * len(arr)
    
    # Store count of occurrences
    for num in arr:
        index = (num // exp) % 10
        count[index] += 1
    
    # Change count to actual positions
    for i in range(1, 10):
        count[i] += count[i - 1]
    
    # Build output array
    for i in range(len(arr) - 1, -1, -1):
        index = (arr[i] // exp) % 10
        output[count[index] - 1] = arr[i]
        count[index] -= 1
    
    return output


# Example usage
if __name__ == "__main__":
    # Test with various arrays
    test_cases = [
        [64, 34, 25, 12, 22, 11, 90],
        [5, 2, 8, 1, 9],
        [170, 45, 75, 90, 802, 24, 2, 66],
        [1, 2, 3, 4, 5],  # Already sorted
        [5, 4, 3, 2, 1],  # Reverse sorted
    ]
    
    for arr in test_cases:
        if arr:
            original = arr.copy()
            sorted_lsd = radix_sort_lsd(arr.copy())
            sorted_msd = radix_sort_msd(arr.copy())
            print(f"Original: {original}")
            print(f"LSD:      {sorted_lsd}")
            print(f"MSD:      {sorted_msd}\n")
