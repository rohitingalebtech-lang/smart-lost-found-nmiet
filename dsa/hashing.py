"""
HASHING DATA STRUCTURES & ALGORITHMS
Smart Lost & Found Management System
NMIET B.Tech AI & Data Science

Covered:
1. Hash Function
2. Hash Table
3. Collision Handling
4. Separate Chaining
5. Open Addressing
6. Linear Probing
7. Fast Item Lookup
"""


# ============================================================
# 1. HASH FUNCTION
# ============================================================

def hash_function(key, table_size):
    """
    Basic division-method hash function.
    """

    if isinstance(key, int):
        return key % table_size

    key_value = 0

    for character in str(key):
        key_value += ord(character)

    return key_value % table_size


# ============================================================
# 2. HASH TABLE USING SEPARATE CHAINING
# ============================================================

class ChainedHashTable:

    def __init__(self, size=10):
        self.size = size
        self.table = [[] for _ in range(size)]

    def _index(self, key):
        return hash_function(
            key,
            self.size
        )

    def insert(self, key, value):

        index = self._index(key)

        bucket = self.table[index]

        for position, (existing_key, _) in enumerate(bucket):

            if existing_key == key:

                bucket[position] = (
                    key,
                    value
                )

                return

        bucket.append(
            (key, value)
        )

    def search(self, key):

        index = self._index(key)

        bucket = self.table[index]

        for existing_key, value in bucket:

            if existing_key == key:
                return value

        return None

    def delete(self, key):

        index = self._index(key)

        bucket = self.table[index]

        for position, (existing_key, _) in enumerate(bucket):

            if existing_key == key:

                bucket.pop(position)
                return True

        return False

    def display(self):

        for index, bucket in enumerate(self.table):

            print(
                f"Index {index}: {bucket}"
            )


# ============================================================
# 3. HASH TABLE USING OPEN ADDRESSING
# ============================================================

class OpenAddressingHashTable:

    EMPTY = None
    DELETED = "__DELETED__"

    def __init__(self, size=10):
        self.size = size
        self.table = [
            self.EMPTY
            for _ in range(size)
        ]

    def _index(self, key):

        return hash_function(
            key,
            self.size
        )

    def insert(self, key, value):

        start_index = self._index(key)

        for offset in range(self.size):

            index = (
                start_index + offset
            ) % self.size

            slot = self.table[index]

            if (
                slot is self.EMPTY
                or slot == self.DELETED
                or slot[0] == key
            ):

                self.table[index] = (
                    key,
                    value
                )

                return True

        return False

    def search(self, key):

        start_index = self._index(key)

        for offset in range(self.size):

            index = (
                start_index + offset
            ) % self.size

            slot = self.table[index]

            if slot is self.EMPTY:
                return None

            if (
                slot != self.DELETED
                and slot[0] == key
            ):
                return slot[1]

        return None

    def delete(self, key):

        start_index = self._index(key)

        for offset in range(self.size):

            index = (
                start_index + offset
            ) % self.size

            slot = self.table[index]

            if slot is self.EMPTY:
                return False

            if (
                slot != self.DELETED
                and slot[0] == key
            ):

                self.table[index] = self.DELETED
                return True

        return False

    def display(self):

        for index, value in enumerate(self.table):

            print(
                f"Index {index}: {value}"
            )


# ============================================================
# 4. ITEM HASH TABLE
# ============================================================

class ItemHashTable:

    def __init__(self, size=20):
        self.table = ChainedHashTable(size)

    def add_item(self, item):

        item_id = item.get("id")

        if item_id is None:
            return False

        self.table.insert(
            item_id,
            item
        )

        return True

    def find_item(self, item_id):

        return self.table.search(
            item_id
        )

    def remove_item(self, item_id):

        return self.table.delete(
            item_id
        )


# ============================================================
# 5. STRING HASHING FOR ITEM NAMES
# ============================================================

def string_hash(text, table_size=50):

    text = str(text).lower()

    hash_value = 0

    for character in text:

        hash_value = (
            hash_value * 31
            + ord(character)
        )

    return hash_value % table_size


# ============================================================
# 6. TEST HASHING
# ============================================================

def test_hashing():

    print("=" * 65)
    print("NMIET SMART LOST & FOUND - HASHING TEST")
    print("=" * 65)

    # --------------------------------------------------------
    # Hash Function
    # --------------------------------------------------------

    print("\n--- HASH FUNCTION ---")

    print(
        "Hash of 101:",
        hash_function(101, 10)
    )

    print(
        "Hash of 202:",
        hash_function(202, 10)
    )

    print(
        "Hash of 'Wallet':",
        hash_function("Wallet", 10)
    )

    # --------------------------------------------------------
    # Separate Chaining
    # --------------------------------------------------------

    print("\n--- SEPARATE CHAINING ---")

    chained = ChainedHashTable(5)

    chained.insert(
        101,
        "Black Wallet"
    )

    chained.insert(
        106,
        "Blue Bottle"
    )

    chained.insert(
        111,
        "Student ID Card"
    )

    print("Hash Table:")

    chained.display()

    print(
        "\nSearch Item 106:"
    )

    print(
        chained.search(106)
    )

    # --------------------------------------------------------
    # Delete
    # --------------------------------------------------------

    print(
        "\nDelete Item 106:"
    )

    print(
        chained.delete(106)
    )

    print(
        "Search Item 106:"
    )

    print(
        chained.search(106)
    )

    # --------------------------------------------------------
    # Open Addressing
    # --------------------------------------------------------

    print("\n--- OPEN ADDRESSING ---")

    open_table = OpenAddressingHashTable(5)

    open_table.insert(
        101,
        "Black Wallet"
    )

    open_table.insert(
        106,
        "Blue Bottle"
    )

    open_table.insert(
        111,
        "Student ID Card"
    )

    open_table.display()

    print(
        "\nSearch Item 111:"
    )

    print(
        open_table.search(111)
    )

    # --------------------------------------------------------
    # Item Hash Table
    # --------------------------------------------------------

    print("\n--- ITEM HASH TABLE ---")

    items = ItemHashTable()

    items.add_item(
        {
            "id": 201,
            "name": "Black Wallet",
            "category": "Accessories",
            "location": "Library"
        }
    )

    items.add_item(
        {
            "id": 202,
            "name": "Blue Water Bottle",
            "category": "Bottle",
            "location": "Canteen"
        }
    )

    items.add_item(
        {
            "id": 203,
            "name": "Student ID Card",
            "category": "Documents",
            "location": "Classroom"
        }
    )

    print(
        "Search Item ID 202:"
    )

    print(
        items.find_item(202)
    )

    # --------------------------------------------------------
    # String Hash
    # --------------------------------------------------------

    print("\n--- STRING HASHING ---")

    print(
        "Wallet:",
        string_hash("Wallet")
    )

    print(
        "Water Bottle:",
        string_hash("Water Bottle")
    )

    print(
        "Student ID Card:",
        string_hash("Student ID Card")
    )

    print("\n" + "=" * 65)
    print("ALL HASHING TESTS COMPLETED")
    print("=" * 65)


# ============================================================
# RUN DIRECTLY
# ============================================================

if __name__ == "__main__":
    test_hashing()