"""
Burstsort Algorithm (Non-Comparison Sort)

Time Complexity: O(n) - average case for strings, O(n log n) - worst case
Space Complexity: O(n)

Description:
Burstsort is a cache-efficient sorting algorithm particularly suited for sorting
strings and variable-length records. It uses a trie-like structure with bursting.

Note: This is a simplified educational version. Full implementation is complex.
"""

def burstsort(arr):
    """
    Sorts an array of strings using burstsort algorithm (simplified version).
    
    Args:
        arr: List of strings to sort
    
    Returns:
        Sorted list
    """
    if len(arr) <= 1:
        return arr
    
    # For educational purposes, use a simplified approach
    # Convert to strings if not already
    str_arr = [str(x) for x in arr]
    
    return burstsort_recursive(str_arr)


def burstsort_recursive(arr, depth=0):
    """
    Recursive helper for burstsort.
    
    Args:
        arr: Array of strings
        depth: Current character depth
    
    Returns:
        Sorted array
    """
    if len(arr) <= 1:
        return arr
    
    # Base case: use simple sort for small arrays
    if len(arr) < 16:
        return sorted(arr)
    
    # Group strings by character at current depth
    buckets = {}
    for string in arr:
        if depth < len(string):
            char = string[depth]
        else:
            char = '\0'  # Represent end of string
        
        if char not in buckets:
            buckets[char] = []
        buckets[char].append(string)
    
    # Sort each bucket recursively
    result = []
    for char in sorted(buckets.keys()):
        bucket = buckets[char]
        
        if char == '\0':
            # Strings that ended, just extend
            result.extend(bucket)
        else:
            # Recurse on strings with more characters
            sorted_bucket = burstsort_recursive(bucket, depth + 1)
            result.extend(sorted_bucket)
    
    return result


# Example usage
if __name__ == "__main__":
    # Test with strings
    test_cases = [
        ["banana", "apple", "cherry", "date", "apricot"],
        ["zebra", "apple", "mango", "banana"],
        ["aaa", "aab", "aba", "abb"],
        ["z", "a", "m", "b"],
        ["dog"],
        [],
    ]
    
    for arr in test_cases:
        if arr:
            original = arr.copy()
            sorted_arr = burstsort(arr)
            print(f"Original: {original}")
            print(f"Sorted:   {sorted_arr}\n")
    
    # Also test with numbers converted to strings
    print("=== Numeric strings ===")
    arr = ["64", "34", "25", "12", "22", "11", "90"]
    original = arr.copy()
    sorted_arr = burstsort(arr)
    print(f"Original: {original}")
    print(f"Sorted:   {sorted_arr}\n")
