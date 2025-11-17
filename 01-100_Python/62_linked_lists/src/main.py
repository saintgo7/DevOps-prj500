"""
Program 62: Linked Lists - Singly and Doubly Linked Lists
Demonstrates implementation and operations of linked lists
"""


class Node:
    """Node class for singly linked list"""

    def __init__(self, data):
        self.data = data
        self.next = None


class SinglyLinkedList:
    """Singly Linked List implementation"""

    def __init__(self):
        self.head = None
        self.size = 0

    # Time Complexity: O(1)
    def insert_at_beginning(self, data):
        """Insert node at the beginning"""
        new_node = Node(data)
        new_node.next = self.head
        self.head = new_node
        self.size += 1

    # Time Complexity: O(n)
    def insert_at_end(self, data):
        """Insert node at the end"""
        new_node = Node(data)

        if not self.head:
            self.head = new_node
            self.size += 1
            return

        current = self.head
        while current.next:
            current = current.next

        current.next = new_node
        self.size += 1

    # Time Complexity: O(n)
    def insert_at_position(self, data, position):
        """Insert node at specific position"""
        if position < 0 or position > self.size:
            return False

        if position == 0:
            self.insert_at_beginning(data)
            return True

        new_node = Node(data)
        current = self.head

        for _ in range(position - 1):
            current = current.next

        new_node.next = current.next
        current.next = new_node
        self.size += 1
        return True

    # Time Complexity: O(1)
    def delete_from_beginning(self):
        """Delete node from beginning"""
        if not self.head:
            return None

        data = self.head.data
        self.head = self.head.next
        self.size -= 1
        return data

    # Time Complexity: O(n)
    def delete_from_end(self):
        """Delete node from end"""
        if not self.head:
            return None

        if not self.head.next:
            data = self.head.data
            self.head = None
            self.size -= 1
            return data

        current = self.head
        while current.next.next:
            current = current.next

        data = current.next.data
        current.next = None
        self.size -= 1
        return data

    # Time Complexity: O(n)
    def delete_by_value(self, value):
        """Delete first node with given value"""
        if not self.head:
            return False

        if self.head.data == value:
            self.head = self.head.next
            self.size -= 1
            return True

        current = self.head
        while current.next:
            if current.next.data == value:
                current.next = current.next.next
                self.size -= 1
                return True
            current = current.next

        return False

    # Time Complexity: O(n)
    def search(self, value):
        """Search for a value in the list"""
        current = self.head
        position = 0

        while current:
            if current.data == value:
                return position
            current = current.next
            position += 1

        return -1

    # Time Complexity: O(n)
    def reverse(self):
        """Reverse the linked list"""
        prev = None
        current = self.head

        while current:
            next_node = current.next
            current.next = prev
            prev = current
            current = next_node

        self.head = prev

    def display(self):
        """Display the linked list"""
        if not self.head:
            return "Empty list"

        result = []
        current = self.head
        while current:
            result.append(str(current.data))
            current = current.next

        return " -> ".join(result)

    def get_size(self):
        """Return size of the list"""
        return self.size


class DoubleNode:
    """Node class for doubly linked list"""

    def __init__(self, data):
        self.data = data
        self.next = None
        self.prev = None


class DoublyLinkedList:
    """Doubly Linked List implementation"""

    def __init__(self):
        self.head = None
        self.tail = None
        self.size = 0

    # Time Complexity: O(1)
    def insert_at_beginning(self, data):
        """Insert node at the beginning"""
        new_node = DoubleNode(data)

        if not self.head:
            self.head = self.tail = new_node
        else:
            new_node.next = self.head
            self.head.prev = new_node
            self.head = new_node

        self.size += 1

    # Time Complexity: O(1)
    def insert_at_end(self, data):
        """Insert node at the end"""
        new_node = DoubleNode(data)

        if not self.tail:
            self.head = self.tail = new_node
        else:
            new_node.prev = self.tail
            self.tail.next = new_node
            self.tail = new_node

        self.size += 1

    # Time Complexity: O(1)
    def delete_from_beginning(self):
        """Delete node from beginning"""
        if not self.head:
            return None

        data = self.head.data

        if self.head == self.tail:
            self.head = self.tail = None
        else:
            self.head = self.head.next
            self.head.prev = None

        self.size -= 1
        return data

    # Time Complexity: O(1)
    def delete_from_end(self):
        """Delete node from end"""
        if not self.tail:
            return None

        data = self.tail.data

        if self.head == self.tail:
            self.head = self.tail = None
        else:
            self.tail = self.tail.prev
            self.tail.next = None

        self.size -= 1
        return data

    def display_forward(self):
        """Display list from head to tail"""
        if not self.head:
            return "Empty list"

        result = []
        current = self.head
        while current:
            result.append(str(current.data))
            current = current.next

        return " <-> ".join(result)

    def display_backward(self):
        """Display list from tail to head"""
        if not self.tail:
            return "Empty list"

        result = []
        current = self.tail
        while current:
            result.append(str(current.data))
            current = current.prev

        return " <-> ".join(result)


def linked_list_problems():
    """Demonstrate common linked list problems"""

    print("\n=== Common Linked List Problems ===\n")

    # 1. Detect cycle in linked list
    def has_cycle(head):
        """Detect cycle using Floyd's algorithm - Time: O(n)"""
        if not head or not head.next:
            return False

        slow = fast = head

        while fast and fast.next:
            slow = slow.next
            fast = fast.next.next

            if slow == fast:
                return True

        return False

    # Create list with cycle
    ll = SinglyLinkedList()
    for i in [1, 2, 3, 4, 5]:
        ll.insert_at_end(i)

    print(f"List: {ll.display()}")
    print(f"Has cycle: {has_cycle(ll.head)}")

    # Create cycle for testing
    current = ll.head
    while current.next:
        current = current.next
    cycle_start = ll.head.next.next  # Node with value 3
    current.next = cycle_start
    print(f"After creating cycle (5 -> 3): Has cycle = {has_cycle(ll.head)}\n")

    # 2. Find middle element
    def find_middle(head):
        """Find middle element using slow-fast pointers - Time: O(n)"""
        if not head:
            return None

        slow = fast = head

        while fast and fast.next:
            slow = slow.next
            fast = fast.next.next

        return slow.data

    ll2 = SinglyLinkedList()
    for i in [1, 2, 3, 4, 5]:
        ll2.insert_at_end(i)

    print(f"List: {ll2.display()}")
    print(f"Middle element: {find_middle(ll2.head)}\n")

    # 3. Remove nth node from end
    def remove_nth_from_end(head, n):
        """Remove nth node from end - Time: O(n)"""
        dummy = Node(0)
        dummy.next = head
        first = second = dummy

        # Move first n+1 steps ahead
        for _ in range(n + 1):
            if first:
                first = first.next

        # Move both pointers
        while first:
            first = first.next
            second = second.next

        # Remove nth node
        second.next = second.next.next
        return dummy.next

    ll3 = SinglyLinkedList()
    for i in [1, 2, 3, 4, 5]:
        ll3.insert_at_end(i)

    print(f"Original list: {ll3.display()}")
    ll3.head = remove_nth_from_end(ll3.head, 2)
    ll3.size -= 1
    print(f"After removing 2nd node from end: {ll3.display()}\n")

    # 4. Merge two sorted lists
    def merge_sorted_lists(head1, head2):
        """Merge two sorted lists - Time: O(n+m)"""
        dummy = Node(0)
        current = dummy

        while head1 and head2:
            if head1.data <= head2.data:
                current.next = head1
                head1 = head1.next
            else:
                current.next = head2
                head2 = head2.next
            current = current.next

        current.next = head1 or head2
        return dummy.next

    ll4 = SinglyLinkedList()
    ll5 = SinglyLinkedList()

    for i in [1, 3, 5, 7]:
        ll4.insert_at_end(i)
    for i in [2, 4, 6, 8]:
        ll5.insert_at_end(i)

    print(f"List 1: {ll4.display()}")
    print(f"List 2: {ll5.display()}")

    merged = SinglyLinkedList()
    merged.head = merge_sorted_lists(ll4.head, ll5.head)
    print(f"Merged list: {merged.display()}\n")

    # 5. Check palindrome
    def is_palindrome(head):
        """Check if linked list is palindrome - Time: O(n)"""
        if not head or not head.next:
            return True

        # Find middle
        slow = fast = head
        while fast and fast.next:
            slow = slow.next
            fast = fast.next.next

        # Reverse second half
        prev = None
        current = slow
        while current:
            next_node = current.next
            current.next = prev
            prev = current
            current = next_node

        # Compare both halves
        first = head
        second = prev

        while second:
            if first.data != second.data:
                return False
            first = first.next
            second = second.next

        return True

    ll6 = SinglyLinkedList()
    for i in [1, 2, 3, 2, 1]:
        ll6.insert_at_end(i)

    print(f"List: {ll6.display()}")
    print(f"Is palindrome: {is_palindrome(ll6.head)}")


def main():
    """Main function to demonstrate linked lists"""

    print("=" * 60)
    print("PROGRAM 62: LINKED LISTS - SINGLY AND DOUBLY")
    print("=" * 60)

    # Singly Linked List Operations
    print("\n=== Singly Linked List Operations ===\n")

    sll = SinglyLinkedList()

    # Insert at end
    print("Inserting elements at end: 10, 20, 30, 40")
    for value in [10, 20, 30, 40]:
        sll.insert_at_end(value)
    print(f"List: {sll.display()}")
    print(f"Size: {sll.get_size()}\n")

    # Insert at beginning
    print("Inserting 5 at beginning")
    sll.insert_at_beginning(5)
    print(f"List: {sll.display()}\n")

    # Insert at position
    print("Inserting 25 at position 3")
    sll.insert_at_position(25, 3)
    print(f"List: {sll.display()}\n")

    # Search
    value = 30
    position = sll.search(value)
    print(f"Searching for {value}: Found at position {position}\n")

    # Delete operations
    print(f"Deleting from beginning: {sll.delete_from_beginning()}")
    print(f"List: {sll.display()}\n")

    print(f"Deleting from end: {sll.delete_from_end()}")
    print(f"List: {sll.display()}\n")

    print("Deleting value 25")
    sll.delete_by_value(25)
    print(f"List: {sll.display()}\n")

    # Reverse
    print("Reversing the list")
    sll.reverse()
    print(f"List: {sll.display()}")

    print("\n" + "-" * 60)

    # Doubly Linked List Operations
    print("\n=== Doubly Linked List Operations ===\n")

    dll = DoublyLinkedList()

    # Insert operations
    print("Inserting at end: 10, 20, 30")
    for value in [10, 20, 30]:
        dll.insert_at_end(value)
    print(f"Forward:  {dll.display_forward()}")
    print(f"Backward: {dll.display_backward()}\n")

    print("Inserting at beginning: 5")
    dll.insert_at_beginning(5)
    print(f"Forward:  {dll.display_forward()}")
    print(f"Backward: {dll.display_backward()}\n")

    # Delete operations
    print(f"Delete from beginning: {dll.delete_from_beginning()}")
    print(f"Forward: {dll.display_forward()}\n")

    print(f"Delete from end: {dll.delete_from_end()}")
    print(f"Forward: {dll.display_forward()}")

    print("\n" + "-" * 60)

    # Common problems
    linked_list_problems()

    print("\n" + "=" * 60)
    print("Linked list operations demonstration completed!")
    print("=" * 60)


if __name__ == "__main__":
    main()
