"""
Program 66: Binary Trees - Implementation, Traversals, and Operations
Demonstrates binary tree data structure with various operations
"""

from collections import deque


class TreeNode:
    """Node class for binary tree"""

    def __init__(self, data):
        self.data = data
        self.left = None
        self.right = None


class BinaryTree:
    """Binary Tree implementation"""

    def __init__(self):
        self.root = None

    # Time Complexity: O(n)
    def insert_level_order(self, data):
        """Insert node in level order"""
        new_node = TreeNode(data)

        if not self.root:
            self.root = new_node
            return

        queue = deque([self.root])

        while queue:
            node = queue.popleft()

            if not node.left:
                node.left = new_node
                return
            else:
                queue.append(node.left)

            if not node.right:
                node.right = new_node
                return
            else:
                queue.append(node.right)

    # Time Complexity: O(n)
    def inorder_traversal(self, node, result=None):
        """Inorder: Left -> Root -> Right"""
        if result is None:
            result = []

        if node:
            self.inorder_traversal(node.left, result)
            result.append(node.data)
            self.inorder_traversal(node.right, result)

        return result

    # Time Complexity: O(n)
    def preorder_traversal(self, node, result=None):
        """Preorder: Root -> Left -> Right"""
        if result is None:
            result = []

        if node:
            result.append(node.data)
            self.preorder_traversal(node.left, result)
            self.preorder_traversal(node.right, result)

        return result

    # Time Complexity: O(n)
    def postorder_traversal(self, node, result=None):
        """Postorder: Left -> Right -> Root"""
        if result is None:
            result = []

        if node:
            self.postorder_traversal(node.left, result)
            self.postorder_traversal(node.right, result)
            result.append(node.data)

        return result

    # Time Complexity: O(n)
    def level_order_traversal(self):
        """Level order (BFS) traversal"""
        if not self.root:
            return []

        result = []
        queue = deque([self.root])

        while queue:
            node = queue.popleft()
            result.append(node.data)

            if node.left:
                queue.append(node.left)
            if node.right:
                queue.append(node.right)

        return result

    # Time Complexity: O(n)
    def height(self, node):
        """Calculate height of tree"""
        if not node:
            return 0

        left_height = self.height(node.left)
        right_height = self.height(node.right)

        return max(left_height, right_height) + 1

    # Time Complexity: O(n)
    def count_nodes(self, node):
        """Count total nodes"""
        if not node:
            return 0

        return 1 + self.count_nodes(node.left) + self.count_nodes(node.right)

    # Time Complexity: O(n)
    def count_leaf_nodes(self, node):
        """Count leaf nodes"""
        if not node:
            return 0

        if not node.left and not node.right:
            return 1

        return self.count_leaf_nodes(node.left) + self.count_leaf_nodes(node.right)

    # Time Complexity: O(n)
    def search(self, node, value):
        """Search for a value"""
        if not node:
            return False

        if node.data == value:
            return True

        return self.search(node.left, value) or self.search(node.right, value)

    # Time Complexity: O(n)
    def find_max(self, node):
        """Find maximum value"""
        if not node:
            return float('-inf')

        max_val = node.data
        left_max = self.find_max(node.left)
        right_max = self.find_max(node.right)

        return max(max_val, left_max, right_max)

    # Time Complexity: O(n)
    def find_min(self, node):
        """Find minimum value"""
        if not node:
            return float('inf')

        min_val = node.data
        left_min = self.find_min(node.left)
        right_min = self.find_min(node.right)

        return min(min_val, left_min, right_min)

    def display_tree(self, node, level=0, prefix="Root: "):
        """Display tree structure"""
        if node:
            print(" " * (level * 4) + prefix + str(node.data))
            if node.left or node.right:
                if node.left:
                    self.display_tree(node.left, level + 1, "L--- ")
                else:
                    print(" " * ((level + 1) * 4) + "L--- None")

                if node.right:
                    self.display_tree(node.right, level + 1, "R--- ")
                else:
                    print(" " * ((level + 1) * 4) + "R--- None")


def iterative_traversals():
    """Demonstrate iterative traversal implementations"""

    print("\n=== Iterative Traversals ===\n")

    def inorder_iterative(root):
        """Iterative inorder traversal"""
        result = []
        stack = []
        current = root

        while current or stack:
            while current:
                stack.append(current)
                current = current.left

            current = stack.pop()
            result.append(current.data)
            current = current.right

        return result

    def preorder_iterative(root):
        """Iterative preorder traversal"""
        if not root:
            return []

        result = []
        stack = [root]

        while stack:
            node = stack.pop()
            result.append(node.data)

            if node.right:
                stack.append(node.right)
            if node.left:
                stack.append(node.left)

        return result

    def postorder_iterative(root):
        """Iterative postorder traversal"""
        if not root:
            return []

        result = []
        stack = [root]

        while stack:
            node = stack.pop()
            result.append(node.data)

            if node.left:
                stack.append(node.left)
            if node.right:
                stack.append(node.right)

        return result[::-1]

    # Create tree
    tree = BinaryTree()
    for val in [1, 2, 3, 4, 5, 6, 7]:
        tree.insert_level_order(val)

    print("Tree structure:")
    tree.display_tree(tree.root)

    print("\nIterative Traversals:")
    print(f"Inorder:   {inorder_iterative(tree.root)}")
    print(f"Preorder:  {preorder_iterative(tree.root)}")
    print(f"Postorder: {postorder_iterative(tree.root)}")


def tree_properties():
    """Demonstrate various tree properties"""

    print("\n=== Tree Properties ===\n")

    def is_balanced(node):
        """Check if tree is balanced"""
        def check_height(node):
            if not node:
                return 0

            left_height = check_height(node.left)
            if left_height == -1:
                return -1

            right_height = check_height(node.right)
            if right_height == -1:
                return -1

            if abs(left_height - right_height) > 1:
                return -1

            return max(left_height, right_height) + 1

        return check_height(node) != -1

    def is_symmetric(root):
        """Check if tree is symmetric"""
        def is_mirror(left, right):
            if not left and not right:
                return True
            if not left or not right:
                return False

            return (left.data == right.data and
                    is_mirror(left.left, right.right) and
                    is_mirror(left.right, right.left))

        if not root:
            return True

        return is_mirror(root.left, root.right)

    def diameter(node):
        """Calculate diameter of tree"""
        def height_and_diameter(node):
            if not node:
                return 0, 0

            left_height, left_dia = height_and_diameter(node.left)
            right_height, right_dia = height_and_diameter(node.right)

            height = max(left_height, right_height) + 1
            dia = max(left_height + right_height, max(left_dia, right_dia))

            return height, dia

        _, dia = height_and_diameter(node)
        return dia

    # Create balanced tree
    tree1 = BinaryTree()
    for val in [1, 2, 3, 4, 5, 6, 7]:
        tree1.insert_level_order(val)

    print("Tree 1:")
    tree1.display_tree(tree1.root)
    print(f"\nIs balanced: {is_balanced(tree1.root)}")
    print(f"Diameter: {diameter(tree1.root)}")

    # Create symmetric tree
    tree2 = BinaryTree()
    tree2.root = TreeNode(1)
    tree2.root.left = TreeNode(2)
    tree2.root.right = TreeNode(2)
    tree2.root.left.left = TreeNode(3)
    tree2.root.left.right = TreeNode(4)
    tree2.root.right.left = TreeNode(4)
    tree2.root.right.right = TreeNode(3)

    print("\n\nTree 2 (Symmetric):")
    tree2.display_tree(tree2.root)
    print(f"\nIs symmetric: {is_symmetric(tree2.root)}")


def tree_views():
    """Demonstrate different tree views"""

    print("\n=== Tree Views ===\n")

    def left_view(root):
        """Left view of tree"""
        if not root:
            return []

        result = []
        queue = deque([root])

        while queue:
            level_size = len(queue)

            for i in range(level_size):
                node = queue.popleft()

                if i == 0:
                    result.append(node.data)

                if node.left:
                    queue.append(node.left)
                if node.right:
                    queue.append(node.right)

        return result

    def right_view(root):
        """Right view of tree"""
        if not root:
            return []

        result = []
        queue = deque([root])

        while queue:
            level_size = len(queue)

            for i in range(level_size):
                node = queue.popleft()

                if i == level_size - 1:
                    result.append(node.data)

                if node.left:
                    queue.append(node.left)
                if node.right:
                    queue.append(node.right)

        return result

    def top_view(root):
        """Top view of tree"""
        if not root:
            return []

        view_map = {}
        queue = deque([(root, 0)])

        while queue:
            node, hd = queue.popleft()

            if hd not in view_map:
                view_map[hd] = node.data

            if node.left:
                queue.append((node.left, hd - 1))
            if node.right:
                queue.append((node.right, hd + 1))

        return [view_map[key] for key in sorted(view_map.keys())]

    def bottom_view(root):
        """Bottom view of tree"""
        if not root:
            return []

        view_map = {}
        queue = deque([(root, 0)])

        while queue:
            node, hd = queue.popleft()
            view_map[hd] = node.data

            if node.left:
                queue.append((node.left, hd - 1))
            if node.right:
                queue.append((node.right, hd + 1))

        return [view_map[key] for key in sorted(view_map.keys())]

    # Create tree
    tree = BinaryTree()
    for val in [1, 2, 3, 4, 5, 6, 7]:
        tree.insert_level_order(val)

    print("Tree structure:")
    tree.display_tree(tree.root)

    print("\nDifferent Views:")
    print(f"Left view:   {left_view(tree.root)}")
    print(f"Right view:  {right_view(tree.root)}")
    print(f"Top view:    {top_view(tree.root)}")
    print(f"Bottom view: {bottom_view(tree.root)}")


def path_operations():
    """Demonstrate path-related operations"""

    print("\n=== Path Operations ===\n")

    def root_to_leaf_paths(node, path=None, paths=None):
        """Find all root to leaf paths"""
        if path is None:
            path = []
        if paths is None:
            paths = []

        if not node:
            return paths

        path.append(node.data)

        if not node.left and not node.right:
            paths.append(path.copy())
        else:
            root_to_leaf_paths(node.left, path, paths)
            root_to_leaf_paths(node.right, path, paths)

        path.pop()
        return paths

    def has_path_sum(node, target_sum, current_sum=0):
        """Check if path exists with given sum"""
        if not node:
            return False

        current_sum += node.data

        if not node.left and not node.right:
            return current_sum == target_sum

        return (has_path_sum(node.left, target_sum, current_sum) or
                has_path_sum(node.right, target_sum, current_sum))

    def lowest_common_ancestor(root, p, q):
        """Find lowest common ancestor"""
        if not root or root.data == p or root.data == q:
            return root

        left = lowest_common_ancestor(root.left, p, q)
        right = lowest_common_ancestor(root.right, p, q)

        if left and right:
            return root

        return left if left else right

    # Create tree
    tree = BinaryTree()
    for val in [1, 2, 3, 4, 5, 6, 7]:
        tree.insert_level_order(val)

    print("Tree structure:")
    tree.display_tree(tree.root)

    print("\nAll root-to-leaf paths:")
    paths = root_to_leaf_paths(tree.root)
    for path in paths:
        print(f"  {' -> '.join(map(str, path))}")

    target = 8
    print(f"\nHas path with sum {target}: {has_path_sum(tree.root, target)}")

    lca = lowest_common_ancestor(tree.root, 4, 5)
    print(f"LCA of 4 and 5: {lca.data if lca else None}")


def main():
    """Main function to demonstrate binary tree operations"""

    print("=" * 60)
    print("PROGRAM 66: BINARY TREES - IMPLEMENTATION & OPERATIONS")
    print("=" * 60)

    # Basic Binary Tree Operations
    print("\n=== Basic Binary Tree Operations ===\n")

    tree = BinaryTree()

    print("Inserting nodes in level order: 1, 2, 3, 4, 5, 6, 7")
    for value in [1, 2, 3, 4, 5, 6, 7]:
        tree.insert_level_order(value)

    print("\nTree structure:")
    tree.display_tree(tree.root)

    print("\nTraversals:")
    print(f"Inorder:      {tree.inorder_traversal(tree.root)}")
    print(f"Preorder:     {tree.preorder_traversal(tree.root)}")
    print(f"Postorder:    {tree.postorder_traversal(tree.root)}")
    print(f"Level order:  {tree.level_order_traversal()}")

    print(f"\nTree Statistics:")
    print(f"Height:       {tree.height(tree.root)}")
    print(f"Total nodes:  {tree.count_nodes(tree.root)}")
    print(f"Leaf nodes:   {tree.count_leaf_nodes(tree.root)}")
    print(f"Maximum:      {tree.find_max(tree.root)}")
    print(f"Minimum:      {tree.find_min(tree.root)}")

    search_val = 5
    print(f"\nSearch for {search_val}: {tree.search(tree.root, search_val)}")

    print("\n" + "-" * 60)

    # Iterative traversals
    iterative_traversals()

    print("\n" + "-" * 60)

    # Tree properties
    tree_properties()

    print("\n" + "-" * 60)

    # Tree views
    tree_views()

    print("\n" + "-" * 60)

    # Path operations
    path_operations()

    print("\n" + "=" * 60)
    print("Binary tree operations demonstration completed!")
    print("=" * 60)


if __name__ == "__main__":
    main()
