"""
Program 61: Arrays - Array Operations and Manipulation
Demonstrates various array operations, 2D arrays, and array manipulation techniques
"""


class ArrayOperations:
    """Class for performing various array operations"""

    def __init__(self):
        self.array = []

    # Time Complexity: O(1)
    def append(self, element):
        """Add element at the end"""
        self.array.append(element)

    # Time Complexity: O(n)
    def insert(self, index, element):
        """Insert element at specific position"""
        self.array.insert(index, element)

    # Time Complexity: O(n)
    def remove(self, element):
        """Remove first occurrence of element"""
        if element in self.array:
            self.array.remove(element)
            return True
        return False

    # Time Complexity: O(1)
    def pop(self, index=-1):
        """Remove and return element at index"""
        if self.array:
            return self.array.pop(index)
        return None

    # Time Complexity: O(n)
    def search(self, element):
        """Find index of element"""
        try:
            return self.array.index(element)
        except ValueError:
            return -1

    # Time Complexity: O(n)
    def reverse(self):
        """Reverse the array"""
        self.array.reverse()

    # Time Complexity: O(n log n)
    def sort(self):
        """Sort the array"""
        self.array.sort()

    def display(self):
        """Display the array"""
        return self.array


class Array2D:
    """Class for 2D array operations"""

    def __init__(self, rows, cols, initial_value=0):
        """Initialize 2D array with given dimensions"""
        self.rows = rows
        self.cols = cols
        self.matrix = [[initial_value for _ in range(cols)] for _ in range(rows)]

    def set(self, row, col, value):
        """Set value at position (row, col)"""
        if 0 <= row < self.rows and 0 <= col < self.cols:
            self.matrix[row][col] = value
            return True
        return False

    def get(self, row, col):
        """Get value at position (row, col)"""
        if 0 <= row < self.rows and 0 <= col < self.cols:
            return self.matrix[row][col]
        return None

    def transpose(self):
        """Return transpose of the matrix"""
        return [[self.matrix[j][i] for j in range(self.rows)]
                for i in range(self.cols)]

    def rotate_90_clockwise(self):
        """Rotate matrix 90 degrees clockwise"""
        # Transpose then reverse each row
        transposed = self.transpose()
        return [row[::-1] for row in transposed]

    def display(self):
        """Display the 2D array"""
        for row in self.matrix:
            print(' '.join(f'{val:4}' for val in row))


def array_manipulation_examples():
    """Demonstrate various array manipulation techniques"""

    print("=== Array Manipulation Examples ===\n")

    # 1. Array Rotation
    def rotate_array(arr, k):
        """Rotate array to right by k positions - Time: O(n), Space: O(1)"""
        n = len(arr)
        k = k % n
        arr[:] = arr[-k:] + arr[:-k]
        return arr

    arr = [1, 2, 3, 4, 5, 6, 7]
    print(f"Original array: {arr}")
    print(f"Rotated by 3: {rotate_array(arr.copy(), 3)}\n")

    # 2. Find Maximum Subarray Sum (Kadane's Algorithm)
    def max_subarray_sum(arr):
        """Find maximum sum of contiguous subarray - Time: O(n)"""
        max_sum = current_sum = arr[0]
        start = end = temp_start = 0

        for i in range(1, len(arr)):
            if current_sum < 0:
                current_sum = arr[i]
                temp_start = i
            else:
                current_sum += arr[i]

            if current_sum > max_sum:
                max_sum = current_sum
                start = temp_start
                end = i

        return max_sum, arr[start:end+1]

    arr = [-2, 1, -3, 4, -1, 2, 1, -5, 4]
    max_sum, subarray = max_subarray_sum(arr)
    print(f"Array: {arr}")
    print(f"Maximum subarray sum: {max_sum}")
    print(f"Subarray: {subarray}\n")

    # 3. Remove Duplicates from Sorted Array
    def remove_duplicates(arr):
        """Remove duplicates in-place from sorted array - Time: O(n)"""
        if not arr:
            return 0

        write_index = 1
        for read_index in range(1, len(arr)):
            if arr[read_index] != arr[read_index - 1]:
                arr[write_index] = arr[read_index]
                write_index += 1

        return write_index, arr[:write_index]

    arr = [1, 1, 2, 2, 2, 3, 4, 4, 5]
    length, unique_arr = remove_duplicates(arr.copy())
    print(f"Original sorted array: {arr}")
    print(f"After removing duplicates: {unique_arr}")
    print(f"New length: {length}\n")

    # 4. Merge Two Sorted Arrays
    def merge_sorted_arrays(arr1, arr2):
        """Merge two sorted arrays - Time: O(n+m)"""
        result = []
        i = j = 0

        while i < len(arr1) and j < len(arr2):
            if arr1[i] <= arr2[j]:
                result.append(arr1[i])
                i += 1
            else:
                result.append(arr2[j])
                j += 1

        result.extend(arr1[i:])
        result.extend(arr2[j:])
        return result

    arr1 = [1, 3, 5, 7]
    arr2 = [2, 4, 6, 8, 10]
    print(f"Array 1: {arr1}")
    print(f"Array 2: {arr2}")
    print(f"Merged: {merge_sorted_arrays(arr1, arr2)}\n")

    # 5. Find Missing Number
    def find_missing_number(arr, n):
        """Find missing number in array 1 to n - Time: O(n)"""
        expected_sum = n * (n + 1) // 2
        actual_sum = sum(arr)
        return expected_sum - actual_sum

    arr = [1, 2, 4, 5, 6]
    n = 6
    print(f"Array (1 to {n} with one missing): {arr}")
    print(f"Missing number: {find_missing_number(arr, n)}\n")

    # 6. Move Zeros to End
    def move_zeros_to_end(arr):
        """Move all zeros to end while maintaining order - Time: O(n)"""
        non_zero_index = 0

        for i in range(len(arr)):
            if arr[i] != 0:
                arr[non_zero_index], arr[i] = arr[i], arr[non_zero_index]
                non_zero_index += 1

        return arr

    arr = [0, 1, 0, 3, 12, 0, 5]
    print(f"Original array: {arr}")
    print(f"After moving zeros: {move_zeros_to_end(arr.copy())}\n")


def two_dimensional_array_operations():
    """Demonstrate 2D array operations"""

    print("=== 2D Array Operations ===\n")

    # Create and manipulate 2D array
    matrix = Array2D(3, 4)

    # Fill with values
    value = 1
    for i in range(3):
        for j in range(4):
            matrix.set(i, j, value)
            value += 1

    print("Original Matrix:")
    matrix.display()

    print("\nTransposed Matrix:")
    transposed = matrix.transpose()
    for row in transposed:
        print(' '.join(f'{val:4}' for val in row))

    # Square matrix operations
    square_matrix = Array2D(3, 3)
    values = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
    for i in range(3):
        for j in range(3):
            square_matrix.set(i, j, values[i][j])

    print("\n\nOriginal Square Matrix:")
    square_matrix.display()

    print("\nRotated 90° Clockwise:")
    rotated = square_matrix.rotate_90_clockwise()
    for row in rotated:
        print(' '.join(f'{val:4}' for val in row))

    # Spiral traversal
    def spiral_traversal(matrix):
        """Traverse matrix in spiral order - Time: O(m*n)"""
        if not matrix:
            return []

        result = []
        top, bottom = 0, len(matrix) - 1
        left, right = 0, len(matrix[0]) - 1

        while top <= bottom and left <= right:
            # Traverse right
            for col in range(left, right + 1):
                result.append(matrix[top][col])
            top += 1

            # Traverse down
            for row in range(top, bottom + 1):
                result.append(matrix[row][right])
            right -= 1

            # Traverse left
            if top <= bottom:
                for col in range(right, left - 1, -1):
                    result.append(matrix[bottom][col])
                bottom -= 1

            # Traverse up
            if left <= right:
                for row in range(bottom, top - 1, -1):
                    result.append(matrix[row][left])
                left += 1

        return result

    matrix_data = [[1, 2, 3, 4], [5, 6, 7, 8], [9, 10, 11, 12]]
    print("\n\nMatrix for Spiral Traversal:")
    for row in matrix_data:
        print(' '.join(f'{val:4}' for val in row))
    print(f"\nSpiral Order: {spiral_traversal(matrix_data)}")


def advanced_array_problems():
    """Demonstrate advanced array problems"""

    print("\n=== Advanced Array Problems ===\n")

    # 1. Find Pair with Given Sum
    def find_pair_with_sum(arr, target):
        """Find pair that sums to target - Time: O(n), Space: O(n)"""
        seen = set()
        for num in arr:
            complement = target - num
            if complement in seen:
                return (complement, num)
            seen.add(num)
        return None

    arr = [2, 7, 11, 15, 3, 6]
    target = 9
    print(f"Array: {arr}")
    print(f"Target sum: {target}")
    print(f"Pair found: {find_pair_with_sum(arr, target)}\n")

    # 2. Trapping Rain Water
    def trap_rain_water(heights):
        """Calculate trapped rain water - Time: O(n), Space: O(1)"""
        if not heights:
            return 0

        left, right = 0, len(heights) - 1
        left_max, right_max = 0, 0
        water = 0

        while left < right:
            if heights[left] < heights[right]:
                if heights[left] >= left_max:
                    left_max = heights[left]
                else:
                    water += left_max - heights[left]
                left += 1
            else:
                if heights[right] >= right_max:
                    right_max = heights[right]
                else:
                    water += right_max - heights[right]
                right -= 1

        return water

    heights = [0, 1, 0, 2, 1, 0, 1, 3, 2, 1, 2, 1]
    print(f"Heights: {heights}")
    print(f"Rain water trapped: {trap_rain_water(heights)} units\n")

    # 3. Product of Array Except Self
    def product_except_self(nums):
        """Calculate product of all except self - Time: O(n), Space: O(1)"""
        n = len(nums)
        result = [1] * n

        # Calculate left products
        left_product = 1
        for i in range(n):
            result[i] = left_product
            left_product *= nums[i]

        # Calculate right products and multiply
        right_product = 1
        for i in range(n - 1, -1, -1):
            result[i] *= right_product
            right_product *= nums[i]

        return result

    nums = [1, 2, 3, 4]
    print(f"Array: {nums}")
    print(f"Product except self: {product_except_self(nums)}\n")


def main():
    """Main function to demonstrate array operations"""

    print("=" * 60)
    print("PROGRAM 61: ARRAYS - OPERATIONS AND MANIPULATION")
    print("=" * 60)

    # Basic Array Operations
    print("\n=== Basic Array Operations ===\n")
    arr_ops = ArrayOperations()

    # Add elements
    for i in [5, 2, 8, 1, 9, 3]:
        arr_ops.append(i)
    print(f"Array after appending elements: {arr_ops.display()}")

    # Insert element
    arr_ops.insert(2, 7)
    print(f"After inserting 7 at index 2: {arr_ops.display()}")

    # Search element
    index = arr_ops.search(8)
    print(f"Index of element 8: {index}")

    # Remove element
    arr_ops.remove(1)
    print(f"After removing element 1: {arr_ops.display()}")

    # Sort array
    arr_ops.sort()
    print(f"After sorting: {arr_ops.display()}")

    # Reverse array
    arr_ops.reverse()
    print(f"After reversing: {arr_ops.display()}")

    # Pop element
    popped = arr_ops.pop()
    print(f"Popped element: {popped}")
    print(f"Array after pop: {arr_ops.display()}")

    print("\n" + "-" * 60 + "\n")

    # Array Manipulation Examples
    array_manipulation_examples()

    print("-" * 60 + "\n")

    # 2D Array Operations
    two_dimensional_array_operations()

    print("\n" + "-" * 60)

    # Advanced Problems
    advanced_array_problems()

    print("=" * 60)
    print("Array operations demonstration completed!")
    print("=" * 60)


if __name__ == "__main__":
    main()
