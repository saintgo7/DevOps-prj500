"""
Program 67: Binary Search Trees - BST Operations
Demonstrates BST implementation with insertion, deletion, and search
"""


class BSTNode:
    """Node class for Binary Search Tree"""

    def __init__(self, data):
        self.data = data
        self.left = None
        self.right = None


class BinarySearchTree:
    """Binary Search Tree implementation"""

    def __init__(self):
        self.root = None

    # Time Complexity: Average O(log n), Worst O(n)
    def insert(self, data):
        """Insert node into BST"""
        if not self.root:
            self.root = BSTNode(data)
        else:
            self._insert_recursive(self.root, data)

    def _insert_recursive(self, node, data):
        """Helper method for insertion"""
        if data < node.data:
            if node.left is None:
                node.left = BSTNode(data)
            else:
                self._insert_recursive(node.left, data)
        elif data > node.data:
            if node.right is None:
                node.right = BSTNode(data)
            else:
                self._insert_recursive(node.right, data)
        # Equal values are not inserted

    # Time Complexity: Average O(log n), Worst O(n)
    def search(self, data):
        """Search for a value in BST"""
        return self._search_recursive(self.root, data)

    def _search_recursive(self, node, data):
        """Helper method for search"""
        if node is None:
            return False

        if data == node.data:
            return True
        elif data < node.data:
            return self._search_recursive(node.left, data)
        else:
            return self._search_recursive(node.right, data)

    # Time Complexity: Average O(log n), Worst O(n)
    def delete(self, data):
        """Delete node from BST"""
        self.root = self._delete_recursive(self.root, data)

    def _delete_recursive(self, node, data):
        """Helper method for deletion"""
        if node is None:
            return None

        if data < node.data:
            node.left = self._delete_recursive(node.left, data)
        elif data > node.data:
            node.right = self._delete_recursive(node.right, data)
        else:
            # Node with one child or no child
            if node.left is None:
                return node.right
            elif node.right is None:
                return node.left

            # Node with two children
            # Get inorder successor (smallest in right subtree)
            min_node = self._find_min(node.right)
            node.data = min_node.data
            node.right = self._delete_recursive(node.right, min_node.data)

        return node

    def _find_min(self, node):
        """Find minimum node in subtree"""
        while node.left:
            node = node.left
        return node

    def _find_max(self, node):
        """Find maximum node in subtree"""
        while node.right:
            node = node.right
        return node

    # Time Complexity: O(n)
    def inorder(self, node, result=None):
        """Inorder traversal (gives sorted order)"""
        if result is None:
            result = []

        if node:
            self.inorder(node.left, result)
            result.append(node.data)
            self.inorder(node.right, result)

        return result

    def preorder(self, node, result=None):
        """Preorder traversal"""
        if result is None:
            result = []

        if node:
            result.append(node.data)
            self.preorder(node.left, result)
            self.preorder(node.right, result)

        return result

    def postorder(self, node, result=None):
        """Postorder traversal"""
        if result is None:
            result = []

        if node:
            self.postorder(node.left, result)
            self.postorder(node.right, result)
            result.append(node.data)

        return result

    def find_min_value(self):
        """Find minimum value in BST"""
        if not self.root:
            return None
        return self._find_min(self.root).data

    def find_max_value(self):
        """Find maximum value in BST"""
        if not self.root:
            return None
        return self._find_max(self.root).data

    def height(self, node):
        """Calculate height of BST"""
        if not node:
            return 0
        return max(self.height(node.left), self.height(node.right)) + 1

    def count_nodes(self, node):
        """Count total nodes"""
        if not node:
            return 0
        return 1 + self.count_nodes(node.left) + self.count_nodes(node.right)

    def display(self, node, level=0, prefix="Root: "):
        """Display BST structure"""
        if node:
            print(" " * (level * 4) + prefix + str(node.data))
            if node.left or node.right:
                if node.left:
                    self.display(node.left, level + 1, "L--- ")
                else:
                    print(" " * ((level + 1) * 4) + "L--- None")

                if node.right:
                    self.display(node.right, level + 1, "R--- ")
                else:
                    print(" " * ((level + 1) * 4) + "R--- None")


def bst_validation():
    """Validate if a binary tree is a valid BST"""

    print("\n=== BST Validation ===\n")

    def is_valid_bst(node, min_val=float('-inf'), max_val=float('inf')):
        """Check if tree is a valid BST - Time: O(n)"""
        if not node:
            return True

        if node.data <= min_val or node.data >= max_val:
            return False

        return (is_valid_bst(node.left, min_val, node.data) and
                is_valid_bst(node.right, node.data, max_val))

    # Create valid BST
    bst = BinarySearchTree()
    for val in [50, 30, 70, 20, 40, 60, 80]:
        bst.insert(val)

    print("Valid BST:")
    bst.display(bst.root)
    print(f"\nIs valid BST: {is_valid_bst(bst.root)}")

    # Create invalid BST
    invalid_tree = BSTNode(50)
    invalid_tree.left = BSTNode(30)
    invalid_tree.right = BSTNode(70)
    invalid_tree.left.left = BSTNode(20)
    invalid_tree.left.right = BSTNode(60)  # Invalid: 60 > 50

    print("\n\nInvalid BST (60 in wrong position):")
    bst2 = BinarySearchTree()
    bst2.root = invalid_tree
    bst2.display(bst2.root)
    print(f"\nIs valid BST: {is_valid_bst(bst2.root)}")


def kth_smallest_largest():
    """Find kth smallest and largest elements in BST"""

    print("\n=== Kth Smallest and Largest ===\n")

    def kth_smallest(root, k):
        """Find kth smallest element - Time: O(n)"""
        result = []

        def inorder(node):
            if not node or len(result) >= k:
                return

            inorder(node.left)
            result.append(node.data)
            inorder(node.right)

        inorder(root)
        return result[k - 1] if k <= len(result) else None

    def kth_largest(root, k):
        """Find kth largest element - Time: O(n)"""
        result = []

        def reverse_inorder(node):
            if not node or len(result) >= k:
                return

            reverse_inorder(node.right)
            result.append(node.data)
            reverse_inorder(node.left)

        reverse_inorder(root)
        return result[k - 1] if k <= len(result) else None

    bst = BinarySearchTree()
    values = [50, 30, 70, 20, 40, 60, 80, 10, 25, 35, 45]
    for val in values:
        bst.insert(val)

    print("BST:")
    bst.display(bst.root)

    print(f"\nSorted values: {bst.inorder(bst.root)}")

    for k in [1, 3, 5]:
        print(f"\n{k}th smallest: {kth_smallest(bst.root, k)}")
        print(f"{k}th largest: {kth_largest(bst.root, k)}")


def lca_in_bst():
    """Find Lowest Common Ancestor in BST"""

    print("\n=== Lowest Common Ancestor in BST ===\n")

    def find_lca(root, n1, n2):
        """Find LCA - Time: O(h) where h is height"""
        if not root:
            return None

        # If both n1 and n2 are smaller, LCA is in left
        if root.data > n1 and root.data > n2:
            return find_lca(root.left, n1, n2)

        # If both n1 and n2 are greater, LCA is in right
        if root.data < n1 and root.data < n2:
            return find_lca(root.right, n1, n2)

        # We found the split point
        return root

    bst = BinarySearchTree()
    for val in [50, 30, 70, 20, 40, 60, 80]:
        bst.insert(val)

    print("BST:")
    bst.display(bst.root)

    pairs = [(20, 40), (20, 80), (60, 80)]

    for n1, n2 in pairs:
        lca = find_lca(bst.root, n1, n2)
        print(f"\nLCA of {n1} and {n2}: {lca.data if lca else None}")


def bst_from_array():
    """Create balanced BST from sorted array"""

    print("\n=== Create Balanced BST from Sorted Array ===\n")

    def sorted_array_to_bst(arr):
        """Create balanced BST - Time: O(n)"""
        if not arr:
            return None

        mid = len(arr) // 2
        root = BSTNode(arr[mid])

        root.left = sorted_array_to_bst(arr[:mid])
        root.right = sorted_array_to_bst(arr[mid + 1:])

        return root

    sorted_arr = [1, 2, 3, 4, 5, 6, 7, 8, 9]
    print(f"Sorted array: {sorted_arr}")

    root = sorted_array_to_bst(sorted_arr)

    bst = BinarySearchTree()
    bst.root = root

    print("\nBalanced BST:")
    bst.display(bst.root)
    print(f"\nHeight: {bst.height(bst.root)}")
    print(f"Inorder: {bst.inorder(bst.root)}")


def bst_to_greater_tree():
    """Convert BST to Greater Tree"""

    print("\n=== Convert BST to Greater Tree ===\n")

    def convert_to_greater_tree(root):
        """Each node value = node + all greater nodes - Time: O(n)"""
        def reverse_inorder(node, cumsum):
            if not node:
                return cumsum

            cumsum = reverse_inorder(node.right, cumsum)
            cumsum += node.data
            node.data = cumsum
            cumsum = reverse_inorder(node.left, cumsum)

            return cumsum

        reverse_inorder(root, 0)
        return root

    bst = BinarySearchTree()
    for val in [5, 2, 13, 1, 3, 11, 14]:
        bst.insert(val)

    print("Original BST:")
    bst.display(bst.root)
    print(f"Inorder: {bst.inorder(bst.root)}")

    convert_to_greater_tree(bst.root)

    print("\nGreater Tree:")
    bst.display(bst.root)
    print(f"Inorder: {bst.inorder(bst.root)}")


def range_sum_bst():
    """Calculate sum of values in given range"""

    print("\n=== Range Sum in BST ===\n")

    def range_sum(root, low, high):
        """Sum values in range [low, high] - Time: O(n)"""
        if not root:
            return 0

        total = 0

        # Add current node if in range
        if low <= root.data <= high:
            total += root.data

        # Recurse left if necessary
        if root.data > low:
            total += range_sum(root.left, low, high)

        # Recurse right if necessary
        if root.data < high:
            total += range_sum(root.right, low, high)

        return total

    bst = BinarySearchTree()
    for val in [10, 5, 15, 3, 7, 13, 18, 1, 6]:
        bst.insert(val)

    print("BST:")
    bst.display(bst.root)

    ranges = [(6, 10), (1, 7), (13, 18)]

    for low, high in ranges:
        sum_val = range_sum(bst.root, low, high)
        print(f"\nSum of values in range [{low}, {high}]: {sum_val}")


def main():
    """Main function to demonstrate BST operations"""

    print("=" * 60)
    print("PROGRAM 67: BINARY SEARCH TREES - OPERATIONS")
    print("=" * 60)

    # Basic BST Operations
    print("\n=== Basic BST Operations ===\n")

    bst = BinarySearchTree()

    values = [50, 30, 70, 20, 40, 60, 80, 10, 25, 35, 45]
    print(f"Inserting values: {values}")

    for value in values:
        bst.insert(value)

    print("\nBST Structure:")
    bst.display(bst.root)

    print("\nTraversals:")
    print(f"Inorder (sorted):  {bst.inorder(bst.root)}")
    print(f"Preorder:          {bst.preorder(bst.root)}")
    print(f"Postorder:         {bst.postorder(bst.root)}")

    print(f"\nBST Statistics:")
    print(f"Height:      {bst.height(bst.root)}")
    print(f"Total nodes: {bst.count_nodes(bst.root)}")
    print(f"Minimum:     {bst.find_min_value()}")
    print(f"Maximum:     {bst.find_max_value()}")

    # Search
    search_values = [35, 55]
    print("\nSearch Operations:")
    for val in search_values:
        found = bst.search(val)
        print(f"  Search {val}: {'Found' if found else 'Not Found'}")

    # Delete
    print("\nDeletion Operations:")

    print(f"\nDeleting 20 (leaf node)")
    bst.delete(20)
    bst.display(bst.root)

    print(f"\nDeleting 30 (node with two children)")
    bst.delete(30)
    bst.display(bst.root)

    print(f"\nInorder after deletions: {bst.inorder(bst.root)}")

    print("\n" + "-" * 60)

    # BST Validation
    bst_validation()

    print("\n" + "-" * 60)

    # Kth smallest/largest
    kth_smallest_largest()

    print("\n" + "-" * 60)

    # LCA in BST
    lca_in_bst()

    print("\n" + "-" * 60)

    # Balanced BST from array
    bst_from_array()

    print("\n" + "-" * 60)

    # BST to Greater Tree
    bst_to_greater_tree()

    print("\n" + "-" * 60)

    # Range sum
    range_sum_bst()

    print("\n" + "=" * 60)
    print("BST operations demonstration completed!")
    print("=" * 60)


if __name__ == "__main__":
    main()
