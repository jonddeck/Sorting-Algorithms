"""
Library Sort Algorithm

Time Complexity: O(n log n) - average case, O(n²) - worst case
Space Complexity: O(n)

Description:
Library Sort is an insertion sort variant that uses a gap-based approach to avoid
excessive shifting of elements. It maintains gaps between elements to reduce data movement.

Use Cases:
- When data arrives dynamically
- Nearly sorted data
- Educational purposes
"""

def library_sort(arr):
    """
    Sorts an array using library sort algorithm.
    
    Args:
        arr: List of elements to sort
    
    Returns:
        Sorted list
    """
    if len(arr) <= 1:
        return arr
    
    # Create a larger array with gaps for insertion flexibility
    size = len(arr)
    gap_size = size
    
    # Initialize the library array with None values
    library = [None] * (size + gap_size)
    
    # Place first element
    library[gap_size // 2] = arr[0]
    
    # Insert remaining elements
    for i in range(1, size):
        insert_in_library(library, arr[i], size + gap_size)
    
    # Extract sorted elements
    result = [x for x in library if x is not None]
    return result


def insert_in_library(library, value, size):
    """Inserts a value into the library."""
    # Find the position where value should be inserted
    pos = find_position(library, value)
    
    if library[pos] is None:
        library[pos] = value
    else:
        # Shift elements to make space
        if value < library[pos]:
            # Shift left to find empty spot
            j = pos - 1
            while j >= 0 and library[j] is not None:
                j -= 1
            
            if j >= 0:
                # Shift elements to the left
                while j < pos:
                    library[j] = library[j + 1]
                    j += 1
                library[pos] = value
        else:
            # Shift right to find empty spot
            j = pos + 1
            while j < size and library[j] is not None:
                j += 1
            
            if j < size:
                # Shift elements to the right
                while j > pos:
                    library[j] = library[j - 1]
                    j -= 1
                library[pos] = value


def find_position(library, value):
    """Finds the position where value should be inserted."""
    # Binary search for the position
    left, right = 0, len(library) - 1
    
    while left <= right:
        mid = (left + right) // 2
        
        if library[mid] is None:
            # Skip None values
            # Find nearest non-None value
            j = mid - 1
            while j >= left and library[j] is None:
                j -= 1
            
            if j >= left and library[j] < value:
                left = mid + 1
            else:
                right = mid - 1
        elif library[mid] < value:
            left = mid + 1
        else:
            right = mid - 1
    
    return left


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
        sorted_arr = library_sort(arr)
        print(f"Original: {original}")
        print(f"Sorted:   {sorted_arr}\n")
