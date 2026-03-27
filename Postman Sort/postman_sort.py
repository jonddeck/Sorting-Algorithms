"""
Postman Sort Algorithm (Non-Comparison Sort)

Time Complexity: O(n * k) - where k is the alphabet size
Space Complexity: O(n + k)

Description:
Postman Sort (also called American Flag Sort) is a 2-dimensional generalization of
counting sort. It sorts elements based on multiple keys or digit positions.

Use Cases:
- Sorting strings
- Sorting tuples with multiple keys
- Stable multi-key sorting
- Lexicographic ordering
"""

def postman_sort(arr):
    """
    Sorts an array using postman sort algorithm.
    Works primarily with strings or tuples.
    
    Args:
        arr: List of strings or objects to sort
    
    Returns:
        Sorted list
    """
    if len(arr) <= 1:
        return arr
    
    # Convert to strings for processing
    string_arr = [str(x) for x in arr]
    
    # Find maximum key length
    max_len = max(len(s) for s in string_arr) if string_arr else 0
    
    # Sort from least significant key (rightmost) to most significant
    for i in range(max_len - 1, -1, -1):
        string_arr = count_sort_by_position(string_arr, i)
    
    return string_arr


def count_sort_by_position(arr, position):
    """
    Counts sort based on character at given position.
    
    Args:
        arr: List of strings
        position: Character position to sort by
    
    Returns:
        Sorted list
    """
    # Create buckets for all possible characters
    buckets = {}
    
    for string in arr:
        if position < len(string):
            char = string[position]
        else:
            char = ' '  # Pad with space for shorter strings
        
        if char not in buckets:
            buckets[char] = []
        buckets[char].append(string)
    
    # Concatenate buckets in sorted order
    result = []
    for char in sorted(buckets.keys()):
        result.extend(buckets[char])
    
    return result


def postman_sort_numeric(arr):
    """
    Postman sort adapted for numeric values (multi-digit numbers).
    
    Args:
        arr: List of numbers with maximum number of digits
    
    Returns:
        Sorted list
    """
    if len(arr) <= 1:
        return arr
    
    # Find the number with maximum digits
    max_num = max(abs(x) for x in arr) if arr else 0
    max_digits = len(str(max_num))
    
    # Convert to padded strings
    str_arr = [str(x).zfill(max_digits) for x in arr]
    
    # Sort from rightmost to leftmost digit
    for i in range(max_digits - 1, -1, -1):
        str_arr = count_sort_by_digit_position(str_arr, i)
    
    # Convert back to numbers
    return [int(x) for x in str_arr]


def count_sort_by_digit_position(arr, position):
    """
    Counting sort based on digit at given position.
    
    Args:
        arr: List of padded strings
        position: Digit position to sort by
    
    Returns:
        Sorted list
    """
    buckets = {}
    
    for string in arr:
        if position < len(string):
            digit = string[position]
        else:
            digit = '0'
        
        if digit not in buckets:
            buckets[digit] = []
        buckets[digit].append(string)
    
    result = []
    for digit in sorted(buckets.keys()):
        result.extend(buckets[digit])
    
    return result


# Example usage
if __name__ == "__main__":
    # Test with strings
    print("=== Postman Sort (Strings) ===")
    test_strings = [
        ["banana", "apple", "cherry", "date", "apricot"],
        ["dog", "cat", "bird", "ant"],
        ["aaa", "aab", "aba", "abb"],
    ]
    
    for arr in test_strings:
        if arr:
            original = arr.copy()
            sorted_arr = postman_sort(arr)
            print(f"Original: {original}")
            print(f"Sorted:   {sorted_arr}\n")
    
    # Test with numbers
    print("\n=== Postman Sort (Numbers) ===")
    test_numbers = [
        [64, 34, 25, 12, 22, 11, 90],
        [5, 2, 8, 1, 9],
        [170, 45, 75, 90, 802, 24, 2, 66],
    ]
    
    for arr in test_numbers:
        if arr:
            original = arr.copy()
            sorted_arr = postman_sort_numeric(arr)
            print(f"Original: {original}")
            print(f"Sorted:   {sorted_arr}\n")
