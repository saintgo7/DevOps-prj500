"""
Program 75: Backtracking - N-Queens, Sudoku, Permutations
Demonstrates backtracking algorithm technique with classic problems
"""

import copy


def n_queens():
    """
    N-Queens Problem - Place N queens on N×N board
    Time: O(N!), Space: O(N²)
    """

    print("\n=== N-Queens Problem ===\n")

    def is_safe(board, row, col, n):
        """Check if queen can be placed at board[row][col]"""
        # Check row on left side
        for j in range(col):
            if board[row][j] == 1:
                return False

        # Check upper diagonal
        i, j = row, col
        while i >= 0 and j >= 0:
            if board[i][j] == 1:
                return False
            i -= 1
            j -= 1

        # Check lower diagonal
        i, j = row, col
        while i < n and j >= 0:
            if board[i][j] == 1:
                return False
            i += 1
            j -= 1

        return True

    def solve_n_queens_util(board, col, n, solutions):
        """Solve using backtracking"""
        if col >= n:
            solutions.append([row[:] for row in board])
            return

        for row in range(n):
            if is_safe(board, row, col, n):
                board[row][col] = 1
                solve_n_queens_util(board, col + 1, n, solutions)
                board[row][col] = 0  # Backtrack

    def solve_n_queens(n):
        """Find all solutions"""
        board = [[0] * n for _ in range(n)]
        solutions = []
        solve_n_queens_util(board, 0, n, solutions)
        return solutions

    def print_board(board):
        """Print board nicely"""
        for row in board:
            print("  " + " ".join("Q" if cell == 1 else "." for cell in row))

    n = 4
    solutions = solve_n_queens(n)

    print(f"N = {n}")
    print(f"Number of solutions: {len(solutions)}\n")

    for i, solution in enumerate(solutions, 1):
        print(f"Solution {i}:")
        print_board(solution)
        print()


def sudoku_solver():
    """
    Sudoku Solver using Backtracking
    Time: O(9^(n*n)), Space: O(n*n)
    """

    print("\n=== Sudoku Solver ===\n")

    def is_valid(board, row, col, num):
        """Check if number can be placed"""
        # Check row
        if num in board[row]:
            return False

        # Check column
        if num in [board[i][col] for i in range(9)]:
            return False

        # Check 3x3 box
        box_row, box_col = 3 * (row // 3), 3 * (col // 3)
        for i in range(box_row, box_row + 3):
            for j in range(box_col, box_col + 3):
                if board[i][j] == num:
                    return False

        return True

    def solve_sudoku(board):
        """Solve sudoku using backtracking"""
        for row in range(9):
            for col in range(9):
                if board[row][col] == 0:
                    for num in range(1, 10):
                        if is_valid(board, row, col, num):
                            board[row][col] = num

                            if solve_sudoku(board):
                                return True

                            board[row][col] = 0  # Backtrack

                    return False

        return True

    def print_sudoku(board):
        """Print sudoku board"""
        for i, row in enumerate(board):
            if i % 3 == 0 and i != 0:
                print("  " + "-" * 21)

            for j, num in enumerate(row):
                if j % 3 == 0 and j != 0:
                    print("| ", end="")

                if num == 0:
                    print(". ", end="")
                else:
                    print(f"{num} ", end="")

            print()

    # Sudoku puzzle (0 represents empty cell)
    board = [
        [5, 3, 0, 0, 7, 0, 0, 0, 0],
        [6, 0, 0, 1, 9, 5, 0, 0, 0],
        [0, 9, 8, 0, 0, 0, 0, 6, 0],
        [8, 0, 0, 0, 6, 0, 0, 0, 3],
        [4, 0, 0, 8, 0, 3, 0, 0, 1],
        [7, 0, 0, 0, 2, 0, 0, 0, 6],
        [0, 6, 0, 0, 0, 0, 2, 8, 0],
        [0, 0, 0, 4, 1, 9, 0, 0, 5],
        [0, 0, 0, 0, 8, 0, 0, 7, 9],
    ]

    print("Original Sudoku:")
    print_sudoku(board)

    if solve_sudoku(board):
        print("\n\nSolved Sudoku:")
        print_sudoku(board)
    else:
        print("\n\nNo solution exists")


def generate_permutations():
    """
    Generate all permutations using backtracking
    Time: O(N!), Space: O(N)
    """

    print("\n=== Generate Permutations ===\n")

    def permute(arr):
        """Generate all permutations"""
        result = []

        def backtrack(first=0):
            if first == len(arr):
                result.append(arr[:])
                return

            for i in range(first, len(arr)):
                arr[first], arr[i] = arr[i], arr[first]
                backtrack(first + 1)
                arr[first], arr[i] = arr[i], arr[first]  # Backtrack

        backtrack()
        return result

    arr = [1, 2, 3]
    perms = permute(arr)

    print(f"Array: {arr}")
    print(f"Number of permutations: {len(perms)}")
    print("Permutations:")
    for perm in perms:
        print(f"  {perm}")


def generate_combinations():
    """
    Generate all combinations using backtracking
    Time: O(2^N), Space: O(N)
    """

    print("\n=== Generate Combinations ===\n")

    def combine(n, k):
        """Generate all k-element combinations from 1 to n"""
        result = []

        def backtrack(start, path):
            if len(path) == k:
                result.append(path[:])
                return

            for i in range(start, n + 1):
                path.append(i)
                backtrack(i + 1, path)
                path.pop()  # Backtrack

        backtrack(1, [])
        return result

    n, k = 5, 3
    combs = combine(n, k)

    print(f"n = {n}, k = {k}")
    print(f"Number of combinations: {len(combs)}")
    print("Combinations:")
    for comb in combs:
        print(f"  {comb}")


def subset_sum_backtrack():
    """
    Subset Sum using Backtracking
    Find all subsets with given sum
    """

    print("\n=== Subset Sum (Backtracking) ===\n")

    def find_subsets(arr, target):
        """Find all subsets that sum to target"""
        result = []

        def backtrack(start, path, current_sum):
            if current_sum == target:
                result.append(path[:])
                return

            if current_sum > target:
                return

            for i in range(start, len(arr)):
                path.append(arr[i])
                backtrack(i + 1, path, current_sum + arr[i])
                path.pop()  # Backtrack

        backtrack(0, [], 0)
        return result

    arr = [2, 3, 6, 7]
    target = 7

    subsets = find_subsets(arr, target)

    print(f"Array: {arr}")
    print(f"Target sum: {target}")
    print(f"Number of subsets: {len(subsets)}")
    print("Subsets:")
    for subset in subsets:
        print(f"  {subset} (sum = {sum(subset)})")


def knight_tour():
    """
    Knight's Tour Problem
    Visit all squares on chessboard using knight moves
    """

    print("\n=== Knight's Tour ===\n")

    def is_safe(x, y, board, n):
        """Check if position is valid and unvisited"""
        return 0 <= x < n and 0 <= y < n and board[x][y] == -1

    def solve_knight_tour(n):
        """Solve knight's tour"""
        board = [[-1 for _ in range(n)] for _ in range(n)]

        # Knight move directions
        moves_x = [2, 1, -1, -2, -2, -1, 1, 2]
        moves_y = [1, 2, 2, 1, -1, -2, -2, -1]

        def backtrack(x, y, move_count):
            board[x][y] = move_count

            if move_count == n * n - 1:
                return True

            for i in range(8):
                next_x = x + moves_x[i]
                next_y = y + moves_y[i]

                if is_safe(next_x, next_y, board, n):
                    if backtrack(next_x, next_y, move_count + 1):
                        return True

            board[x][y] = -1  # Backtrack
            return False

        # Start from (0, 0)
        if backtrack(0, 0, 0):
            return board
        return None

    n = 5
    print(f"Board size: {n}x{n}")

    solution = solve_knight_tour(n)

    if solution:
        print("\nKnight's Tour Solution:")
        for row in solution:
            print("  " + " ".join(f"{num:3d}" for num in row))
    else:
        print("\nNo solution exists")


def rat_in_maze():
    """
    Rat in a Maze Problem
    Find path from source to destination
    """

    print("\n=== Rat in a Maze ===\n")

    def solve_maze(maze):
        """Find path in maze (1 = open, 0 = blocked)"""
        n = len(maze)
        solution = [[0] * n for _ in range(n)]

        def is_safe(x, y):
            return 0 <= x < n and 0 <= y < n and maze[x][y] == 1

        def backtrack(x, y):
            if x == n - 1 and y == n - 1:
                solution[x][y] = 1
                return True

            if is_safe(x, y):
                solution[x][y] = 1

                # Move right
                if backtrack(x, y + 1):
                    return True

                # Move down
                if backtrack(x + 1, y):
                    return True

                solution[x][y] = 0  # Backtrack
                return False

            return False

        if backtrack(0, 0):
            return solution
        return None

    maze = [
        [1, 0, 0, 0],
        [1, 1, 0, 1],
        [0, 1, 0, 0],
        [1, 1, 1, 1],
    ]

    print("Maze (1 = open, 0 = blocked):")
    for row in maze:
        print("  " + " ".join(str(cell) for cell in row))

    solution = solve_maze(maze)

    if solution:
        print("\nPath (1 = path):")
        for row in solution:
            print("  " + " ".join(str(cell) for cell in row))
    else:
        print("\nNo path exists")


def word_search():
    """
    Word Search in 2D grid
    """

    print("\n=== Word Search in Grid ===\n")

    def exist(board, word):
        """Check if word exists in board"""
        rows, cols = len(board), len(board[0])

        def backtrack(r, c, index):
            if index == len(word):
                return True

            if (r < 0 or r >= rows or c < 0 or c >= cols or
                    board[r][c] != word[index]):
                return False

            # Mark as visited
            temp = board[r][c]
            board[r][c] = '#'

            # Explore all directions
            found = (backtrack(r + 1, c, index + 1) or
                     backtrack(r - 1, c, index + 1) or
                     backtrack(r, c + 1, index + 1) or
                     backtrack(r, c - 1, index + 1))

            # Backtrack
            board[r][c] = temp

            return found

        for i in range(rows):
            for j in range(cols):
                if backtrack(i, j, 0):
                    return True

        return False

    board = [
        ['A', 'B', 'C', 'E'],
        ['S', 'F', 'C', 'S'],
        ['A', 'D', 'E', 'E']
    ]

    words = ["ABCCED", "SEE", "ABCB"]

    print("Board:")
    for row in board:
        print("  " + " ".join(row))

    print("\nWord search results:")
    for word in words:
        board_copy = [row[:] for row in board]
        result = exist(board_copy, word)
        print(f"  '{word}': {'Found' if result else 'Not found'}")


def main():
    """Main function to demonstrate backtracking"""

    print("=" * 60)
    print("PROGRAM 75: BACKTRACKING ALGORITHMS")
    print("=" * 60)

    # N-Queens
    n_queens()

    print("=" * 60)

    # Sudoku Solver
    sudoku_solver()

    print("\n" + "=" * 60)

    # Permutations
    generate_permutations()

    print("\n" + "=" * 60)

    # Combinations
    generate_combinations()

    print("\n" + "=" * 60)

    # Subset Sum
    subset_sum_backtrack()

    print("\n" + "=" * 60)

    # Knight's Tour
    knight_tour()

    print("\n" + "=" * 60)

    # Rat in Maze
    rat_in_maze()

    print("\n" + "=" * 60)

    # Word Search
    word_search()

    print("\n" + "=" * 60)
    print("Backtracking algorithms demonstration completed!")
    print("=" * 60)


if __name__ == "__main__":
    main()
