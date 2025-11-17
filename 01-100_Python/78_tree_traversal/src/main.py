"""
Program 78: Tree Traversal - Inorder, Preorder, Postorder, Level-order
Demonstrates various tree traversal techniques
"""

from collections import deque


class TreeNode:
    """Node for binary tree"""

    def __init__(self, data):
        self.data = data
        self.left = None
        self.right = None


class BinaryTree:
    """Binary tree for traversal demonstrations"""

    def __init__(self):
        self.root = None

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


def recursive_traversals():
    """
    Recursive Tree Traversals
    Time: O(n), Space: O(h) where h is height
    """

    print("\n=== Recursive Traversals ===\n")

    def inorder(node, result=None):
        """Inorder: Left -> Root -> Right"""
        if result is None:
            result = []

        if node:
            inorder(node.left, result)
            result.append(node.data)
            inorder(node.right, result)

        return result

    def preorder(node, result=None):
        """Preorder: Root -> Left -> Right"""
        if result is None:
            result = []

        if node:
            result.append(node.data)
            preorder(node.left, result)
            preorder(node.right, result)

        return result

    def postorder(node, result=None):
        """Postorder: Left -> Right -> Root"""
        if result is None:
            result = []

        if node:
            postorder(node.left, result)
            postorder(node.right, result)
            result.append(node.data)

        return result

    # Create tree
    tree = BinaryTree()
    for val in [1, 2, 3, 4, 5, 6, 7]:
        tree.insert_level_order(val)

    print("Tree structure:")
    print("       1")
    print("      / \\")
    print("     2   3")
    print("    / \\ / \\")
    print("   4  5 6  7")

    print("\nRecursive Traversals:")
    print(f"Inorder:   {inorder(tree.root)}")
    print(f"Preorder:  {preorder(tree.root)}")
    print(f"Postorder: {postorder(tree.root)}")


def iterative_traversals():
    """
    Iterative Tree Traversals using Stack
    Time: O(n), Space: O(h)
    """

    print("\n=== Iterative Traversals ===\n")

    def inorder_iterative(root):
        """Iterative inorder"""
        result = []
        stack = []
        current = root

        while current or stack:
            # Go to leftmost node
            while current:
                stack.append(current)
                current = current.left

            # Process node
            current = stack.pop()
            result.append(current.data)

            # Visit right subtree
            current = current.right

        return result

    def preorder_iterative(root):
        """Iterative preorder"""
        if not root:
            return []

        result = []
        stack = [root]

        while stack:
            node = stack.pop()
            result.append(node.data)

            # Push right first (LIFO)
            if node.right:
                stack.append(node.right)
            if node.left:
                stack.append(node.left)

        return result

    def postorder_iterative(root):
        """Iterative postorder using two stacks"""
        if not root:
            return []

        stack1 = [root]
        stack2 = []

        while stack1:
            node = stack1.pop()
            stack2.append(node)

            if node.left:
                stack1.append(node.left)
            if node.right:
                stack1.append(node.right)

        result = []
        while stack2:
            result.append(stack2.pop().data)

        return result

    # Create tree
    tree = BinaryTree()
    for val in [1, 2, 3, 4, 5, 6, 7]:
        tree.insert_level_order(val)

    print("Iterative Traversals:")
    print(f"Inorder:   {inorder_iterative(tree.root)}")
    print(f"Preorder:  {preorder_iterative(tree.root)}")
    print(f"Postorder: {postorder_iterative(tree.root)}")


def level_order_traversal():
    """
    Level-order (BFS) Traversal
    Time: O(n), Space: O(w) where w is max width
    """

    print("\n=== Level-order Traversal ===\n")

    def level_order(root):
        """Basic level-order traversal"""
        if not root:
            return []

        result = []
        queue = deque([root])

        while queue:
            node = queue.popleft()
            result.append(node.data)

            if node.left:
                queue.append(node.left)
            if node.right:
                queue.append(node.right)

        return result

    def level_order_by_levels(root):
        """Level-order with level separation"""
        if not root:
            return []

        result = []
        queue = deque([root])

        while queue:
            level_size = len(queue)
            level = []

            for _ in range(level_size):
                node = queue.popleft()
                level.append(node.data)

                if node.left:
                    queue.append(node.left)
                if node.right:
                    queue.append(node.right)

            result.append(level)

        return result

    def zigzag_level_order(root):
        """Zigzag level-order traversal"""
        if not root:
            return []

        result = []
        queue = deque([root])
        left_to_right = True

        while queue:
            level_size = len(queue)
            level = deque()

            for _ in range(level_size):
                node = queue.popleft()

                if left_to_right:
                    level.append(node.data)
                else:
                    level.appendleft(node.data)

                if node.left:
                    queue.append(node.left)
                if node.right:
                    queue.append(node.right)

            result.append(list(level))
            left_to_right = not left_to_right

        return result

    # Create tree
    tree = BinaryTree()
    for val in [1, 2, 3, 4, 5, 6, 7]:
        tree.insert_level_order(val)

    print("Level-order: ", level_order(tree.root))
    print("\nLevel-order by levels:")
    for i, level in enumerate(level_order_by_levels(tree.root)):
        print(f"  Level {i}: {level}")

    print("\nZigzag level-order:")
    for i, level in enumerate(zigzag_level_order(tree.root)):
        print(f"  Level {i}: {level}")


def morris_traversal():
    """
    Morris Traversal - Inorder without recursion/stack
    Time: O(n), Space: O(1)
    """

    print("\n=== Morris Traversal ===\n")

    def morris_inorder(root):
        """Morris inorder traversal"""
        result = []
        current = root

        while current:
            if not current.left:
                # No left child, visit and go right
                result.append(current.data)
                current = current.right
            else:
                # Find inorder predecessor
                predecessor = current.left
                while predecessor.right and predecessor.right != current:
                    predecessor = predecessor.right

                if not predecessor.right:
                    # Create thread
                    predecessor.right = current
                    current = current.left
                else:
                    # Remove thread
                    predecessor.right = None
                    result.append(current.data)
                    current = current.right

        return result

    def morris_preorder(root):
        """Morris preorder traversal"""
        result = []
        current = root

        while current:
            if not current.left:
                result.append(current.data)
                current = current.right
            else:
                predecessor = current.left
                while predecessor.right and predecessor.right != current:
                    predecessor = predecessor.right

                if not predecessor.right:
                    result.append(current.data)  # Visit before going left
                    predecessor.right = current
                    current = current.left
                else:
                    predecessor.right = None
                    current = current.right

        return result

    # Create tree
    tree = BinaryTree()
    for val in [1, 2, 3, 4, 5, 6, 7]:
        tree.insert_level_order(val)

    print("Morris Traversals (O(1) space):")
    print(f"Inorder:  {morris_inorder(tree.root)}")
    print(f"Preorder: {morris_preorder(tree.root)}")


def boundary_traversal():
    """Boundary Traversal of Binary Tree"""

    print("\n=== Boundary Traversal ===\n")

    def boundary(root):
        """Get boundary nodes"""
        if not root:
            return []

        result = [root.data]

        def add_left_boundary(node):
            """Add left boundary (excluding leaves)"""
            if not node or (not node.left and not node.right):
                return

            result.append(node.data)

            if node.left:
                add_left_boundary(node.left)
            else:
                add_left_boundary(node.right)

        def add_leaves(node):
            """Add leaf nodes"""
            if not node:
                return

            if not node.left and not node.right:
                result.append(node.data)
                return

            add_leaves(node.left)
            add_leaves(node.right)

        def add_right_boundary(node):
            """Add right boundary (excluding leaves)"""
            if not node or (not node.left and not node.right):
                return

            if node.right:
                add_right_boundary(node.right)
            else:
                add_right_boundary(node.left)

            result.append(node.data)

        add_left_boundary(root.left)
        add_leaves(root)
        add_right_boundary(root.right)

        return result

    # Create tree
    tree = BinaryTree()
    for val in [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]:
        tree.insert_level_order(val)

    print("Boundary traversal:")
    print(f"  {boundary(tree.root)}")


def diagonal_traversal():
    """Diagonal Traversal of Binary Tree"""

    print("\n=== Diagonal Traversal ===\n")

    def diagonal(root):
        """Get diagonal traversal"""
        if not root:
            return []

        result = []
        queue = deque([root])

        while queue:
            node = queue.popleft()

            while node:
                result.append(node.data)

                if node.left:
                    queue.append(node.left)

                node = node.right

        return result

    # Create tree
    tree = BinaryTree()
    for val in [1, 2, 3, 4, 5, 6, 7]:
        tree.insert_level_order(val)

    print("Diagonal traversal:")
    print(f"  {diagonal(tree.root)}")


def vertical_order_traversal():
    """Vertical Order Traversal"""

    print("\n=== Vertical Order Traversal ===\n")

    def vertical_order(root):
        """Get vertical order traversal"""
        if not root:
            return []

        from collections import defaultdict
        column_table = defaultdict(list)
        queue = deque([(root, 0)])

        while queue:
            node, column = queue.popleft()
            column_table[column].append(node.data)

            if node.left:
                queue.append((node.left, column - 1))
            if node.right:
                queue.append((node.right, column + 1))

        result = []
        for col in sorted(column_table.keys()):
            result.append(column_table[col])

        return result

    # Create tree
    tree = BinaryTree()
    for val in [1, 2, 3, 4, 5, 6, 7]:
        tree.insert_level_order(val)

    print("Vertical order traversal:")
    for i, column in enumerate(vertical_order(tree.root)):
        print(f"  Column {i - 3}: {column}")


def main():
    """Main function to demonstrate tree traversals"""

    print("=" * 60)
    print("PROGRAM 78: TREE TRAVERSAL")
    print("=" * 60)

    # Recursive Traversals
    recursive_traversals()

    print("\n" + "=" * 60)

    # Iterative Traversals
    iterative_traversals()

    print("\n" + "=" * 60)

    # Level-order Traversal
    level_order_traversal()

    print("\n" + "=" * 60)

    # Morris Traversal
    morris_traversal()

    print("\n" + "=" * 60)

    # Boundary Traversal
    boundary_traversal()

    print("\n" + "=" * 60)

    # Diagonal Traversal
    diagonal_traversal()

    print("\n" + "=" * 60)

    # Vertical Order Traversal
    vertical_order_traversal()

    print("\n" + "=" * 60)
    print("Tree traversal demonstration completed!")
    print("=" * 60)


if __name__ == "__main__":
    main()
