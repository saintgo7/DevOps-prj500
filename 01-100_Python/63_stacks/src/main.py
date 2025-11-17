"""
Program 63: Stacks - Stack Implementation and Applications
Demonstrates stack data structure and its various applications
"""


class Stack:
    """Stack implementation using list"""

    def __init__(self):
        self.items = []

    # Time Complexity: O(1)
    def push(self, item):
        """Push item onto stack"""
        self.items.append(item)

    # Time Complexity: O(1)
    def pop(self):
        """Pop item from stack"""
        if not self.is_empty():
            return self.items.pop()
        raise IndexError("pop from empty stack")

    # Time Complexity: O(1)
    def peek(self):
        """Return top item without removing"""
        if not self.is_empty():
            return self.items[-1]
        raise IndexError("peek from empty stack")

    # Time Complexity: O(1)
    def is_empty(self):
        """Check if stack is empty"""
        return len(self.items) == 0

    # Time Complexity: O(1)
    def size(self):
        """Return size of stack"""
        return len(self.items)

    def display(self):
        """Display stack contents"""
        return " <- ".join(str(item) for item in reversed(self.items))


class StackWithMin:
    """Stack with O(1) min operation"""

    def __init__(self):
        self.stack = []
        self.min_stack = []

    def push(self, item):
        """Push item and track minimum"""
        self.stack.append(item)

        if not self.min_stack or item <= self.min_stack[-1]:
            self.min_stack.append(item)

    def pop(self):
        """Pop item and update minimum"""
        if not self.stack:
            raise IndexError("pop from empty stack")

        item = self.stack.pop()

        if item == self.min_stack[-1]:
            self.min_stack.pop()

        return item

    def get_min(self):
        """Get minimum element in O(1)"""
        if not self.min_stack:
            raise IndexError("stack is empty")
        return self.min_stack[-1]

    def peek(self):
        """Return top element"""
        if not self.stack:
            raise IndexError("peek from empty stack")
        return self.stack[-1]


class TwoStacksInArray:
    """Implement two stacks using single array"""

    def __init__(self, capacity):
        self.capacity = capacity
        self.array = [None] * capacity
        self.top1 = -1
        self.top2 = capacity

    def push1(self, item):
        """Push to stack 1"""
        if self.top1 < self.top2 - 1:
            self.top1 += 1
            self.array[self.top1] = item
            return True
        return False

    def push2(self, item):
        """Push to stack 2"""
        if self.top1 < self.top2 - 1:
            self.top2 -= 1
            self.array[self.top2] = item
            return True
        return False

    def pop1(self):
        """Pop from stack 1"""
        if self.top1 >= 0:
            item = self.array[self.top1]
            self.top1 -= 1
            return item
        return None

    def pop2(self):
        """Pop from stack 2"""
        if self.top2 < self.capacity:
            item = self.array[self.top2]
            self.top2 += 1
            return item
        return None


def balanced_parentheses():
    """Check if parentheses are balanced - Time: O(n)"""

    print("\n=== Balanced Parentheses Checker ===\n")

    def is_balanced(expression):
        """Check if brackets are balanced"""
        stack = Stack()
        opening = "({["
        closing = ")}]"
        pairs = {"(": ")", "{": "}", "[": "]"}

        for char in expression:
            if char in opening:
                stack.push(char)
            elif char in closing:
                if stack.is_empty():
                    return False

                top = stack.pop()
                if pairs[top] != char:
                    return False

        return stack.is_empty()

    test_cases = [
        "()",
        "()[]{}",
        "(]",
        "([)]",
        "{[()]}",
        "((()))",
        "((())",
    ]

    for expr in test_cases:
        result = is_balanced(expr)
        print(f"'{expr}': {'Balanced' if result else 'Not Balanced'}")


def evaluate_postfix():
    """Evaluate postfix expression - Time: O(n)"""

    print("\n=== Postfix Expression Evaluation ===\n")

    def evaluate(expression):
        """Evaluate postfix expression"""
        stack = Stack()

        for token in expression.split():
            if token.isdigit() or (token[0] == '-' and token[1:].isdigit()):
                stack.push(int(token))
            else:
                operand2 = stack.pop()
                operand1 = stack.pop()

                if token == '+':
                    stack.push(operand1 + operand2)
                elif token == '-':
                    stack.push(operand1 - operand2)
                elif token == '*':
                    stack.push(operand1 * operand2)
                elif token == '/':
                    stack.push(operand1 // operand2)

        return stack.pop()

    expressions = [
        ("2 3 +", "2 + 3"),
        ("2 3 * 4 +", "2 * 3 + 4"),
        ("5 1 2 + 4 * + 3 -", "5 + ((1 + 2) * 4) - 3"),
    ]

    for postfix, infix in expressions:
        result = evaluate(postfix)
        print(f"Postfix: {postfix}")
        print(f"Infix: {infix}")
        print(f"Result: {result}\n")


def infix_to_postfix():
    """Convert infix to postfix - Time: O(n)"""

    print("\n=== Infix to Postfix Conversion ===\n")

    def convert(expression):
        """Convert infix to postfix"""
        precedence = {'+': 1, '-': 1, '*': 2, '/': 2, '^': 3}
        stack = Stack()
        output = []

        for char in expression:
            if char.isalnum():
                output.append(char)
            elif char == '(':
                stack.push(char)
            elif char == ')':
                while not stack.is_empty() and stack.peek() != '(':
                    output.append(stack.pop())
                stack.pop()  # Remove '('
            else:
                while (not stack.is_empty() and
                       stack.peek() != '(' and
                       precedence.get(stack.peek(), 0) >= precedence.get(char, 0)):
                    output.append(stack.pop())
                stack.push(char)

        while not stack.is_empty():
            output.append(stack.pop())

        return ''.join(output)

    expressions = [
        "A+B",
        "A+B*C",
        "(A+B)*C",
        "A+B*C-D",
        "A*(B+C)/D",
    ]

    for expr in expressions:
        postfix = convert(expr)
        print(f"Infix:   {expr}")
        print(f"Postfix: {postfix}\n")


def next_greater_element():
    """Find next greater element for each element - Time: O(n)"""

    print("\n=== Next Greater Element ===\n")

    def find_nge(arr):
        """Find next greater element using stack"""
        n = len(arr)
        result = [-1] * n
        stack = Stack()

        for i in range(n - 1, -1, -1):
            # Pop elements smaller than current
            while not stack.is_empty() and stack.peek() <= arr[i]:
                stack.pop()

            # If stack not empty, top is NGE
            if not stack.is_empty():
                result[i] = stack.peek()

            # Push current element
            stack.push(arr[i])

        return result

    arrays = [
        [4, 5, 2, 25],
        [13, 7, 6, 12],
        [1, 2, 3, 4, 5],
    ]

    for arr in arrays:
        nge = find_nge(arr)
        print(f"Array: {arr}")
        print(f"NGE:   {nge}\n")


def stock_span_problem():
    """Calculate stock span - Time: O(n)"""

    print("\n=== Stock Span Problem ===\n")

    def calculate_span(prices):
        """Calculate span of stock prices"""
        n = len(prices)
        span = [0] * n
        stack = Stack()

        for i in range(n):
            # Pop elements while stack not empty and top price <= current
            while not stack.is_empty() and prices[stack.peek()] <= prices[i]:
                stack.pop()

            # If stack empty, all previous prices are smaller
            span[i] = i + 1 if stack.is_empty() else i - stack.peek()

            # Push current index
            stack.push(i)

        return span

    price_data = [
        [100, 80, 60, 70, 60, 75, 85],
        [10, 4, 5, 90, 120, 80],
    ]

    for prices in price_data:
        span = calculate_span(prices)
        print(f"Prices: {prices}")
        print(f"Span:   {span}\n")


def largest_rectangle_histogram():
    """Find largest rectangle in histogram - Time: O(n)"""

    print("\n=== Largest Rectangle in Histogram ===\n")

    def largest_area(heights):
        """Calculate largest rectangle area"""
        stack = Stack()
        max_area = 0
        index = 0

        while index < len(heights):
            if stack.is_empty() or heights[index] >= heights[stack.peek()]:
                stack.push(index)
                index += 1
            else:
                top = stack.pop()
                width = index if stack.is_empty() else index - stack.peek() - 1
                area = heights[top] * width
                max_area = max(max_area, area)

        while not stack.is_empty():
            top = stack.pop()
            width = index if stack.is_empty() else index - stack.peek() - 1
            area = heights[top] * width
            max_area = max(max_area, area)

        return max_area

    histograms = [
        [2, 1, 5, 6, 2, 3],
        [6, 2, 5, 4, 5, 1, 6],
    ]

    for heights in histograms:
        area = largest_area(heights)
        print(f"Heights: {heights}")
        print(f"Largest rectangle area: {area}\n")


def main():
    """Main function to demonstrate stack operations"""

    print("=" * 60)
    print("PROGRAM 63: STACKS - IMPLEMENTATION AND APPLICATIONS")
    print("=" * 60)

    # Basic Stack Operations
    print("\n=== Basic Stack Operations ===\n")

    stack = Stack()

    print("Pushing elements: 10, 20, 30, 40, 50")
    for value in [10, 20, 30, 40, 50]:
        stack.push(value)

    print(f"Stack (top <- bottom): {stack.display()}")
    print(f"Size: {stack.size()}")
    print(f"Top element (peek): {stack.peek()}\n")

    print(f"Popped: {stack.pop()}")
    print(f"Popped: {stack.pop()}")
    print(f"Stack after pops: {stack.display()}")
    print(f"Size: {stack.size()}\n")

    print(f"Is empty: {stack.is_empty()}")

    print("\n" + "-" * 60)

    # Stack with Min
    print("\n=== Stack with O(1) Min Operation ===\n")

    min_stack = StackWithMin()

    values = [5, 3, 7, 2, 8, 1]
    print(f"Pushing: {values}")

    for val in values:
        min_stack.push(val)
        print(f"Pushed {val}, current min: {min_stack.get_min()}")

    print("\nPopping elements:")
    for _ in range(3):
        popped = min_stack.pop()
        if min_stack.stack:
            print(f"Popped {popped}, current min: {min_stack.get_min()}")
        else:
            print(f"Popped {popped}")

    print("\n" + "-" * 60)

    # Two Stacks in Array
    print("\n=== Two Stacks in Single Array ===\n")

    two_stacks = TwoStacksInArray(10)

    print("Pushing to Stack 1: 1, 2, 3")
    two_stacks.push1(1)
    two_stacks.push1(2)
    two_stacks.push1(3)

    print("Pushing to Stack 2: 10, 20, 30")
    two_stacks.push2(10)
    two_stacks.push2(20)
    two_stacks.push2(30)

    print(f"Pop from Stack 1: {two_stacks.pop1()}")
    print(f"Pop from Stack 2: {two_stacks.pop2()}")

    print("\n" + "-" * 60)

    # Applications
    balanced_parentheses()
    print("\n" + "-" * 60)

    evaluate_postfix()
    print("-" * 60)

    infix_to_postfix()
    print("-" * 60)

    next_greater_element()
    print("-" * 60)

    stock_span_problem()
    print("-" * 60)

    largest_rectangle_histogram()

    print("=" * 60)
    print("Stack operations demonstration completed!")
    print("=" * 60)


if __name__ == "__main__":
    main()
