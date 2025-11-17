"""
Program 65: Hash Tables - Hash Table Implementation and Collision Handling
Demonstrates hash table data structure with various collision resolution techniques
"""


class HashTableChaining:
    """Hash Table with chaining for collision resolution"""

    def __init__(self, size=10):
        self.size = size
        self.table = [[] for _ in range(size)]
        self.count = 0

    def _hash(self, key):
        """Hash function using division method - Time: O(1)"""
        return hash(key) % self.size

    # Time Complexity: Average O(1), Worst O(n)
    def insert(self, key, value):
        """Insert key-value pair"""
        index = self._hash(key)

        # Update if key exists
        for i, (k, v) in enumerate(self.table[index]):
            if k == key:
                self.table[index][i] = (key, value)
                return

        # Insert new key-value
        self.table[index].append((key, value))
        self.count += 1

        # Rehash if load factor > 0.7
        if self.count / self.size > 0.7:
            self._rehash()

    # Time Complexity: Average O(1), Worst O(n)
    def get(self, key):
        """Get value for key"""
        index = self._hash(key)

        for k, v in self.table[index]:
            if k == key:
                return v

        raise KeyError(f"Key '{key}' not found")

    # Time Complexity: Average O(1), Worst O(n)
    def delete(self, key):
        """Delete key-value pair"""
        index = self._hash(key)

        for i, (k, v) in enumerate(self.table[index]):
            if k == key:
                self.table[index].pop(i)
                self.count -= 1
                return v

        raise KeyError(f"Key '{key}' not found")

    def contains(self, key):
        """Check if key exists"""
        try:
            self.get(key)
            return True
        except KeyError:
            return False

    def _rehash(self):
        """Rehash table when load factor exceeds threshold"""
        old_table = self.table
        self.size *= 2
        self.table = [[] for _ in range(self.size)]
        self.count = 0

        for bucket in old_table:
            for key, value in bucket:
                self.insert(key, value)

    def keys(self):
        """Return all keys"""
        result = []
        for bucket in self.table:
            for key, _ in bucket:
                result.append(key)
        return result

    def values(self):
        """Return all values"""
        result = []
        for bucket in self.table:
            for _, value in bucket:
                result.append(value)
        return result

    def items(self):
        """Return all key-value pairs"""
        result = []
        for bucket in self.table:
            for key, value in bucket:
                result.append((key, value))
        return result

    def display(self):
        """Display hash table structure"""
        print(f"Hash Table (size={self.size}, count={self.count}):")
        for i, bucket in enumerate(self.table):
            if bucket:
                items = [f"({k}: {v})" for k, v in bucket]
                print(f"  [{i}]: {' -> '.join(items)}")


class HashTableOpenAddressing:
    """Hash Table with open addressing (linear probing)"""

    def __init__(self, size=10):
        self.size = size
        self.keys = [None] * size
        self.values = [None] * size
        self.count = 0
        self.DELETED = object()  # Marker for deleted slots

    def _hash(self, key):
        """Hash function"""
        return hash(key) % self.size

    def _probe(self, index):
        """Linear probing"""
        return (index + 1) % self.size

    # Time Complexity: Average O(1), Worst O(n)
    def insert(self, key, value):
        """Insert key-value pair with linear probing"""
        if self.count >= self.size * 0.7:
            self._rehash()

        index = self._hash(key)
        initial_index = index

        while True:
            # Empty slot or deleted slot
            if self.keys[index] is None or self.keys[index] is self.DELETED:
                self.keys[index] = key
                self.values[index] = value
                self.count += 1
                return

            # Update existing key
            if self.keys[index] == key:
                self.values[index] = value
                return

            # Probe next position
            index = self._probe(index)

            # Table is full
            if index == initial_index:
                raise OverflowError("Hash table is full")

    # Time Complexity: Average O(1), Worst O(n)
    def get(self, key):
        """Get value for key"""
        index = self._hash(key)
        initial_index = index

        while self.keys[index] is not None:
            if self.keys[index] == key:
                return self.values[index]

            index = self._probe(index)

            if index == initial_index:
                break

        raise KeyError(f"Key '{key}' not found")

    # Time Complexity: Average O(1), Worst O(n)
    def delete(self, key):
        """Delete key-value pair"""
        index = self._hash(key)
        initial_index = index

        while self.keys[index] is not None:
            if self.keys[index] == key:
                value = self.values[index]
                self.keys[index] = self.DELETED
                self.values[index] = None
                self.count -= 1
                return value

            index = self._probe(index)

            if index == initial_index:
                break

        raise KeyError(f"Key '{key}' not found")

    def _rehash(self):
        """Rehash table"""
        old_keys = self.keys
        old_values = self.values
        self.size *= 2
        self.keys = [None] * self.size
        self.values = [None] * self.size
        self.count = 0

        for i in range(len(old_keys)):
            if old_keys[i] is not None and old_keys[i] is not self.DELETED:
                self.insert(old_keys[i], old_values[i])

    def display(self):
        """Display hash table"""
        print(f"Hash Table (size={self.size}, count={self.count}):")
        for i in range(self.size):
            if self.keys[i] is not None and self.keys[i] is not self.DELETED:
                print(f"  [{i}]: {self.keys[i]} = {self.values[i]}")


def hash_functions_comparison():
    """Compare different hash functions"""

    print("\n=== Hash Functions Comparison ===\n")

    def division_method(key, table_size):
        """Division method: h(k) = k mod m"""
        return key % table_size

    def multiplication_method(key, table_size):
        """Multiplication method: h(k) = floor(m * (kA mod 1))"""
        A = 0.6180339887  # (sqrt(5) - 1) / 2
        return int(table_size * ((key * A) % 1))

    def mid_square_method(key, table_size):
        """Mid-square method"""
        squared = key * key
        squared_str = str(squared)
        mid = len(squared_str) // 2
        # Extract middle digits
        if len(squared_str) >= 3:
            mid_digits = int(squared_str[mid-1:mid+2])
        else:
            mid_digits = squared
        return mid_digits % table_size

    keys = [123, 456, 789, 1024, 2048]
    table_size = 10

    print(f"Table size: {table_size}")
    print(f"Keys: {keys}\n")

    print("Division Method:")
    for key in keys:
        print(f"  h({key}) = {division_method(key, table_size)}")

    print("\nMultiplication Method:")
    for key in keys:
        print(f"  h({key}) = {multiplication_method(key, table_size)}")

    print("\nMid-Square Method:")
    for key in keys:
        print(f"  h({key}) = {mid_square_method(key, table_size)}")


def hash_table_applications():
    """Demonstrate hash table applications"""

    print("\n=== Hash Table Applications ===\n")

    # 1. Two Sum Problem
    def two_sum(nums, target):
        """Find two numbers that sum to target - Time: O(n)"""
        seen = {}
        for i, num in enumerate(nums):
            complement = target - num
            if complement in seen:
                return [seen[complement], i]
            seen[num] = i
        return None

    nums = [2, 7, 11, 15]
    target = 9
    print(f"Two Sum Problem:")
    print(f"  Array: {nums}")
    print(f"  Target: {target}")
    print(f"  Indices: {two_sum(nums, target)}\n")

    # 2. First Unique Character
    def first_unique_char(s):
        """Find first unique character - Time: O(n)"""
        char_count = {}
        for char in s:
            char_count[char] = char_count.get(char, 0) + 1

        for i, char in enumerate(s):
            if char_count[char] == 1:
                return i

        return -1

    string = "leetcode"
    print(f"First Unique Character:")
    print(f"  String: {string}")
    print(f"  Index: {first_unique_char(string)}\n")

    # 3. Group Anagrams
    def group_anagrams(words):
        """Group anagrams together - Time: O(n*k log k)"""
        anagram_groups = {}

        for word in words:
            # Sort characters as key
            key = ''.join(sorted(word))
            if key not in anagram_groups:
                anagram_groups[key] = []
            anagram_groups[key].append(word)

        return list(anagram_groups.values())

    words = ["eat", "tea", "tan", "ate", "nat", "bat"]
    print(f"Group Anagrams:")
    print(f"  Words: {words}")
    print(f"  Groups: {group_anagrams(words)}\n")

    # 4. Longest Consecutive Sequence
    def longest_consecutive(nums):
        """Find longest consecutive sequence - Time: O(n)"""
        if not nums:
            return 0

        num_set = set(nums)
        longest = 0

        for num in num_set:
            # Check if it's the start of a sequence
            if num - 1 not in num_set:
                current_num = num
                current_length = 1

                while current_num + 1 in num_set:
                    current_num += 1
                    current_length += 1

                longest = max(longest, current_length)

        return longest

    nums = [100, 4, 200, 1, 3, 2]
    print(f"Longest Consecutive Sequence:")
    print(f"  Array: {nums}")
    print(f"  Length: {longest_consecutive(nums)}\n")

    # 5. Subarray Sum Equals K
    def subarray_sum(nums, k):
        """Count subarrays with sum k - Time: O(n)"""
        count = 0
        cum_sum = 0
        sum_freq = {0: 1}

        for num in nums:
            cum_sum += num

            if cum_sum - k in sum_freq:
                count += sum_freq[cum_sum - k]

            sum_freq[cum_sum] = sum_freq.get(cum_sum, 0) + 1

        return count

    nums = [1, 1, 1]
    k = 2
    print(f"Subarray Sum Equals K:")
    print(f"  Array: {nums}")
    print(f"  K: {k}")
    print(f"  Count: {subarray_sum(nums, k)}")


def collision_handling_demo():
    """Demonstrate collision handling techniques"""

    print("\n=== Collision Handling Demonstration ===\n")

    # Keys that will collide with simple hash function
    keys_with_collisions = [
        ("apple", 100),
        ("banana", 200),
        ("apricot", 150),  # Might collide with apple
        ("berry", 250),    # Might collide with banana
        ("avocado", 180),
    ]

    print("Creating hash table with chaining:")
    ht_chain = HashTableChaining(5)

    for key, value in keys_with_collisions:
        ht_chain.insert(key, value)
        print(f"  Inserted: {key} = {value}")

    print()
    ht_chain.display()

    print("\n" + "-" * 40)

    print("\nCreating hash table with open addressing:")
    ht_open = HashTableOpenAddressing(5)

    for key, value in keys_with_collisions:
        ht_open.insert(key, value)
        print(f"  Inserted: {key} = {value}")

    print()
    ht_open.display()


def frequency_counter():
    """Count frequency of elements using hash table"""

    print("\n=== Frequency Counter ===\n")

    def count_frequencies(items):
        """Count frequency of each item"""
        freq = {}
        for item in items:
            freq[item] = freq.get(item, 0) + 1
        return freq

    # Word frequency
    text = "the quick brown fox jumps over the lazy dog the fox"
    words = text.split()
    word_freq = count_frequencies(words)

    print(f"Text: {text}")
    print("\nWord frequencies:")
    for word, count in sorted(word_freq.items(), key=lambda x: -x[1]):
        print(f"  {word}: {count}")

    print("\n" + "-" * 40)

    # Character frequency
    string = "hello world"
    char_freq = count_frequencies(string.replace(" ", ""))

    print(f"\nString: {string}")
    print("\nCharacter frequencies:")
    for char, count in sorted(char_freq.items()):
        print(f"  '{char}': {count}")


def main():
    """Main function to demonstrate hash table operations"""

    print("=" * 60)
    print("PROGRAM 65: HASH TABLES - IMPLEMENTATION & COLLISIONS")
    print("=" * 60)

    # Hash Table with Chaining
    print("\n=== Hash Table with Chaining ===\n")

    ht = HashTableChaining(5)

    items = [
        ("name", "Alice"),
        ("age", 30),
        ("city", "New York"),
        ("country", "USA"),
        ("email", "alice@example.com"),
    ]

    print("Inserting items:")
    for key, value in items:
        ht.insert(key, value)
        print(f"  {key}: {value}")

    print()
    ht.display()

    print(f"\nGet 'city': {ht.get('city')}")
    print(f"Contains 'age': {ht.contains('age')}")
    print(f"Contains 'phone': {ht.contains('phone')}")

    print(f"\nAll keys: {ht.keys()}")
    print(f"All values: {ht.values()}")

    print("\n" + "-" * 60)

    # Hash Table with Open Addressing
    print("\n=== Hash Table with Open Addressing ===\n")

    ht2 = HashTableOpenAddressing(5)

    print("Inserting items:")
    for key, value in items[:4]:
        ht2.insert(key, value)
        print(f"  {key}: {value}")

    print()
    ht2.display()

    print(f"\nDeleting 'age'")
    ht2.delete('age')
    ht2.display()

    print("\n" + "-" * 60)

    # Hash functions comparison
    hash_functions_comparison()

    print("\n" + "-" * 60)

    # Collision handling
    collision_handling_demo()

    print("\n" + "-" * 60)

    # Applications
    hash_table_applications()

    print("\n" + "-" * 60)

    # Frequency counter
    frequency_counter()

    print("\n" + "=" * 60)
    print("Hash table operations demonstration completed!")
    print("=" * 60)


if __name__ == "__main__":
    main()
