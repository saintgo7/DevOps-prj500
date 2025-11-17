"""
Program 64: Queues - Queue, Deque, Priority Queue, Circular Queue
Demonstrates various queue implementations and operations
"""

from collections import deque
import heapq


class Queue:
    """Queue implementation using list"""

    def __init__(self):
        self.items = []

    # Time Complexity: O(1)
    def enqueue(self, item):
        """Add item to rear of queue"""
        self.items.append(item)

    # Time Complexity: O(n) - due to list shift
    def dequeue(self):
        """Remove and return front item"""
        if not self.is_empty():
            return self.items.pop(0)
        raise IndexError("dequeue from empty queue")

    # Time Complexity: O(1)
    def front(self):
        """Return front item without removing"""
        if not self.is_empty():
            return self.items[0]
        raise IndexError("front from empty queue")

    # Time Complexity: O(1)
    def is_empty(self):
        """Check if queue is empty"""
        return len(self.items) == 0

    # Time Complexity: O(1)
    def size(self):
        """Return size of queue"""
        return len(self.items)

    def display(self):
        """Display queue contents"""
        return " <- ".join(str(item) for item in self.items) + " (front)"


class CircularQueue:
    """Circular Queue implementation using array"""

    def __init__(self, capacity):
        self.capacity = capacity
        self.queue = [None] * capacity
        self.front = -1
        self.rear = -1
        self.count = 0

    # Time Complexity: O(1)
    def enqueue(self, item):
        """Add item to queue"""
        if self.is_full():
            raise OverflowError("Queue is full")

        if self.front == -1:
            self.front = 0

        self.rear = (self.rear + 1) % self.capacity
        self.queue[self.rear] = item
        self.count += 1
        return True

    # Time Complexity: O(1)
    def dequeue(self):
        """Remove and return front item"""
        if self.is_empty():
            raise IndexError("dequeue from empty queue")

        item = self.queue[self.front]

        if self.front == self.rear:
            self.front = self.rear = -1
        else:
            self.front = (self.front + 1) % self.capacity

        self.count -= 1
        return item

    def peek(self):
        """Return front item without removing"""
        if self.is_empty():
            raise IndexError("peek from empty queue")
        return self.queue[self.front]

    def is_empty(self):
        """Check if queue is empty"""
        return self.count == 0

    def is_full(self):
        """Check if queue is full"""
        return self.count == self.capacity

    def size(self):
        """Return current size"""
        return self.count

    def display(self):
        """Display queue contents"""
        if self.is_empty():
            return "Empty queue"

        result = []
        i = self.front
        for _ in range(self.count):
            result.append(str(self.queue[i]))
            i = (i + 1) % self.capacity

        return " <- ".join(result) + " (front)"


class Deque:
    """Double-ended queue implementation"""

    def __init__(self):
        self.items = []

    # Time Complexity: O(1)
    def add_front(self, item):
        """Add item to front"""
        self.items.insert(0, item)

    # Time Complexity: O(1)
    def add_rear(self, item):
        """Add item to rear"""
        self.items.append(item)

    # Time Complexity: O(n)
    def remove_front(self):
        """Remove and return front item"""
        if not self.is_empty():
            return self.items.pop(0)
        raise IndexError("remove from empty deque")

    # Time Complexity: O(1)
    def remove_rear(self):
        """Remove and return rear item"""
        if not self.is_empty():
            return self.items.pop()
        raise IndexError("remove from empty deque")

    def is_empty(self):
        """Check if deque is empty"""
        return len(self.items) == 0

    def size(self):
        """Return size of deque"""
        return len(self.items)

    def display(self):
        """Display deque contents"""
        return "Front <- " + " <-> ".join(str(item) for item in self.items) + " <- Rear"


class PriorityQueue:
    """Priority Queue implementation using heap"""

    def __init__(self):
        self.heap = []
        self.counter = 0  # For stable ordering

    # Time Complexity: O(log n)
    def enqueue(self, item, priority):
        """Add item with priority (lower number = higher priority)"""
        heapq.heappush(self.heap, (priority, self.counter, item))
        self.counter += 1

    # Time Complexity: O(log n)
    def dequeue(self):
        """Remove and return highest priority item"""
        if not self.is_empty():
            priority, _, item = heapq.heappop(self.heap)
            return item, priority
        raise IndexError("dequeue from empty priority queue")

    def peek(self):
        """Return highest priority item without removing"""
        if not self.is_empty():
            priority, _, item = self.heap[0]
            return item, priority
        raise IndexError("peek from empty priority queue")

    def is_empty(self):
        """Check if priority queue is empty"""
        return len(self.heap) == 0

    def size(self):
        """Return size of priority queue"""
        return len(self.heap)

    def display(self):
        """Display priority queue contents"""
        items = [(item, priority) for priority, _, item in sorted(self.heap)]
        return "\n".join(f"  Priority {p}: {item}" for item, p in items)


def queue_using_stacks():
    """Implement queue using two stacks"""

    print("\n=== Queue Using Two Stacks ===\n")

    class QueueUsingStacks:
        """Queue implementation using two stacks"""

        def __init__(self):
            self.stack1 = []  # For enqueue
            self.stack2 = []  # For dequeue

        def enqueue(self, item):
            """Time: O(1)"""
            self.stack1.append(item)

        def dequeue(self):
            """Amortized Time: O(1)"""
            if not self.stack2:
                while self.stack1:
                    self.stack2.append(self.stack1.pop())

            if not self.stack2:
                raise IndexError("dequeue from empty queue")

            return self.stack2.pop()

        def is_empty(self):
            return not self.stack1 and not self.stack2

    q = QueueUsingStacks()

    operations = [
        ("enqueue", 1),
        ("enqueue", 2),
        ("enqueue", 3),
        ("dequeue", None),
        ("enqueue", 4),
        ("dequeue", None),
        ("dequeue", None),
    ]

    for op, val in operations:
        if op == "enqueue":
            q.enqueue(val)
            print(f"Enqueued: {val}")
        else:
            result = q.dequeue()
            print(f"Dequeued: {result}")


def sliding_window_maximum():
    """Find maximum in each sliding window - Time: O(n)"""

    print("\n=== Sliding Window Maximum ===\n")

    def max_sliding_window(arr, k):
        """Find max in each window of size k using deque"""
        if not arr or k == 0:
            return []

        dq = deque()
        result = []

        for i in range(len(arr)):
            # Remove elements outside window
            while dq and dq[0] < i - k + 1:
                dq.popleft()

            # Remove smaller elements from rear
            while dq and arr[dq[-1]] < arr[i]:
                dq.pop()

            dq.append(i)

            # Add to result if window is complete
            if i >= k - 1:
                result.append(arr[dq[0]])

        return result

    test_cases = [
        ([1, 3, -1, -3, 5, 3, 6, 7], 3),
        ([1, 5, 3, 2, 4, 6], 3),
    ]

    for arr, k in test_cases:
        result = max_sliding_window(arr, k)
        print(f"Array: {arr}")
        print(f"Window size: {k}")
        print(f"Maximums: {result}\n")


def first_non_repeating_character():
    """Find first non-repeating character in stream"""

    print("\n=== First Non-Repeating Character in Stream ===\n")

    def first_non_repeating(stream):
        """Find first non-repeating character using queue"""
        char_count = {}
        queue = deque()
        result = []

        for char in stream:
            char_count[char] = char_count.get(char, 0) + 1
            queue.append(char)

            # Remove repeating characters from front
            while queue and char_count[queue[0]] > 1:
                queue.popleft()

            # First non-repeating character or -1
            result.append(queue[0] if queue else '-1')

        return result

    streams = [
        "aabccb",
        "abcabc",
    ]

    for stream in streams:
        result = first_non_repeating(stream)
        print(f"Stream: {stream}")
        print(f"First non-repeating at each step:")
        for i, char in enumerate(stream):
            print(f"  After '{char}': {result[i]}")
        print()


def generate_binary_numbers():
    """Generate binary numbers from 1 to n using queue"""

    print("\n=== Generate Binary Numbers ===\n")

    def generate_binary(n):
        """Generate binary representations using queue"""
        result = []
        q = deque()
        q.append("1")

        for _ in range(n):
            front = q.popleft()
            result.append(front)

            q.append(front + "0")
            q.append(front + "1")

        return result

    n = 10
    binary_numbers = generate_binary(n)
    print(f"Binary numbers from 1 to {n}:")
    for i, binary in enumerate(binary_numbers, 1):
        print(f"  {i}: {binary}")


def task_scheduler():
    """Task scheduling with priority queue"""

    print("\n=== Task Scheduler (Priority Queue) ===\n")

    class Task:
        def __init__(self, name, priority, duration):
            self.name = name
            self.priority = priority
            self.duration = duration

        def __repr__(self):
            return f"Task({self.name}, P{self.priority}, {self.duration}s)"

    pq = PriorityQueue()

    tasks = [
        ("Email", 3, 5),
        ("Urgent Bug", 1, 10),
        ("Meeting", 2, 15),
        ("Documentation", 4, 20),
        ("Code Review", 2, 12),
    ]

    print("Adding tasks to scheduler:")
    for name, priority, duration in tasks:
        task = Task(name, priority, duration)
        pq.enqueue(task, priority)
        print(f"  Added: {task}")

    print("\nExecuting tasks in priority order:")
    total_time = 0
    while not pq.is_empty():
        task, priority = pq.dequeue()
        total_time += task.duration
        print(f"  Executing {task.name} (Priority {priority}, {task.duration}s)")

    print(f"\nTotal execution time: {total_time} seconds")


def main():
    """Main function to demonstrate queue operations"""

    print("=" * 60)
    print("PROGRAM 64: QUEUES - VARIOUS IMPLEMENTATIONS")
    print("=" * 60)

    # Basic Queue Operations
    print("\n=== Basic Queue Operations ===\n")

    q = Queue()

    print("Enqueueing: 10, 20, 30, 40, 50")
    for value in [10, 20, 30, 40, 50]:
        q.enqueue(value)

    print(f"Queue: {q.display()}")
    print(f"Size: {q.size()}")
    print(f"Front element: {q.front()}\n")

    print(f"Dequeued: {q.dequeue()}")
    print(f"Dequeued: {q.dequeue()}")
    print(f"Queue after dequeues: {q.display()}")

    print("\n" + "-" * 60)

    # Circular Queue
    print("\n=== Circular Queue Operations ===\n")

    cq = CircularQueue(5)

    print("Enqueueing: 1, 2, 3, 4, 5")
    for i in range(1, 6):
        cq.enqueue(i)

    print(f"Queue: {cq.display()}")
    print(f"Is full: {cq.is_full()}\n")

    print(f"Dequeued: {cq.dequeue()}")
    print(f"Dequeued: {cq.dequeue()}")
    print(f"Queue: {cq.display()}\n")

    print("Enqueueing: 6, 7")
    cq.enqueue(6)
    cq.enqueue(7)
    print(f"Queue (circular): {cq.display()}")

    print("\n" + "-" * 60)

    # Deque
    print("\n=== Deque Operations ===\n")

    dq = Deque()

    print("Adding to rear: 1, 2, 3")
    for i in [1, 2, 3]:
        dq.add_rear(i)
    print(f"Deque: {dq.display()}\n")

    print("Adding to front: 10, 20")
    dq.add_front(10)
    dq.add_front(20)
    print(f"Deque: {dq.display()}\n")

    print(f"Remove from front: {dq.remove_front()}")
    print(f"Remove from rear: {dq.remove_rear()}")
    print(f"Deque: {dq.display()}")

    print("\n" + "-" * 60)

    # Priority Queue
    print("\n=== Priority Queue Operations ===\n")

    pq = PriorityQueue()

    items = [
        ("Task A", 3),
        ("Task B", 1),
        ("Task C", 2),
        ("Task D", 1),
        ("Task E", 4),
    ]

    print("Enqueueing items with priorities:")
    for item, priority in items:
        pq.enqueue(item, priority)
        print(f"  {item}: Priority {priority}")

    print("\nPriority Queue contents:")
    print(pq.display())

    print("\nDequeueing in priority order:")
    while not pq.is_empty():
        item, priority = pq.dequeue()
        print(f"  {item} (Priority {priority})")

    print("\n" + "-" * 60)

    # Applications
    queue_using_stacks()
    print("\n" + "-" * 60)

    sliding_window_maximum()
    print("-" * 60)

    first_non_repeating_character()
    print("-" * 60)

    generate_binary_numbers()
    print("\n" + "-" * 60)

    task_scheduler()

    print("\n" + "=" * 60)
    print("Queue operations demonstration completed!")
    print("=" * 60)


if __name__ == "__main__":
    main()
