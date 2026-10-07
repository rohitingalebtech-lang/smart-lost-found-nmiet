"""
DSA CORE MODULE
Smart Lost & Found Management System
NMIET B.Tech AI & Data Science

This module demonstrates core Data Structures and Algorithms
used by the Smart Lost & Found system.

Covered here:
1. Arrays
2. Singly Linked List
3. Doubly Linked List
4. Circular Linked List
5. Stack
6. Queue
7. Circular Queue
8. Priority Queue
9. Deque
"""

from collections import deque
import heapq


# ============================================================
# 1. ARRAY
# ============================================================

class ItemArray:
    """
    Array-based storage for lost/found item records.
    """

    def __init__(self):
        self.items = []

    def add(self, item):
        self.items.append(item)

    def get(self, index):
        if 0 <= index < len(self.items):
            return self.items[index]
        return None

    def remove(self, index):
        if 0 <= index < len(self.items):
            return self.items.pop(index)
        return None

    def size(self):
        return len(self.items)

    def get_all(self):
        return self.items


# ============================================================
# 2. SINGLY LINKED LIST
# ============================================================

class SinglyNode:

    def __init__(self, data):
        self.data = data
        self.next = None


class LostItemHistory:

    def __init__(self):
        self.head = None

    def add(self, data):
        new_node = SinglyNode(data)

        if self.head is None:
            self.head = new_node
            return

        current = self.head

        while current.next:
            current = current.next

        current.next = new_node

    def get_all(self):
        result = []
        current = self.head

        while current:
            result.append(current.data)
            current = current.next

        return result


# ============================================================
# 3. DOUBLY LINKED LIST
# ============================================================

class DoublyNode:

    def __init__(self, data):
        self.data = data
        self.previous = None
        self.next = None


class SearchHistory:

    def __init__(self):
        self.head = None
        self.tail = None

    def add(self, data):
        new_node = DoublyNode(data)

        if self.head is None:
            self.head = new_node
            self.tail = new_node
            return

        new_node.previous = self.tail
        self.tail.next = new_node
        self.tail = new_node

    def get_forward(self):
        result = []
        current = self.head

        while current:
            result.append(current.data)
            current = current.next

        return result

    def get_backward(self):
        result = []
        current = self.tail

        while current:
            result.append(current.data)
            current = current.previous

        return result


# ============================================================
# 4. CIRCULAR LINKED LIST
# ============================================================

class CircularNode:

    def __init__(self, data):
        self.data = data
        self.next = None


class CampusLocationCycle:

    def __init__(self):
        self.head = None

    def add(self, data):
        new_node = CircularNode(data)

        if self.head is None:
            self.head = new_node
            new_node.next = self.head
            return

        current = self.head

        while current.next != self.head:
            current = current.next

        current.next = new_node
        new_node.next = self.head

    def get_all(self):
        result = []

        if self.head is None:
            return result

        current = self.head

        while True:
            result.append(current.data)
            current = current.next

            if current == self.head:
                break

        return result


# ============================================================
# 5. STACK
# ============================================================

class ActionStack:

    def __init__(self):
        self.stack = []

    def push(self, action):
        self.stack.append(action)

    def pop(self):
        if self.stack:
            return self.stack.pop()
        return None

    def peek(self):
        if self.stack:
            return self.stack[-1]
        return None

    def is_empty(self):
        return len(self.stack) == 0

    def size(self):
        return len(self.stack)


# ============================================================
# 6. QUEUE
# ============================================================

class ClaimQueue:

    def __init__(self):
        self.queue = deque()

    def enqueue(self, claim):
        self.queue.append(claim)

    def dequeue(self):
        if self.queue:
            return self.queue.popleft()
        return None

    def front(self):
        if self.queue:
            return self.queue[0]
        return None

    def size(self):
        return len(self.queue)

    def is_empty(self):
        return len(self.queue) == 0


# ============================================================
# 7. CIRCULAR QUEUE
# ============================================================

class CircularQueue:

    def __init__(self, capacity=10):
        self.capacity = capacity
        self.queue = [None] * capacity
        self.front_index = 0
        self.rear_index = -1
        self.count = 0

    def enqueue(self, item):
        if self.count == self.capacity:
            return False

        self.rear_index = (
            self.rear_index + 1
        ) % self.capacity

        self.queue[self.rear_index] = item
        self.count += 1

        return True

    def dequeue(self):
        if self.count == 0:
            return None

        item = self.queue[self.front_index]

        self.queue[self.front_index] = None

        self.front_index = (
            self.front_index + 1
        ) % self.capacity

        self.count -= 1

        return item

    def size(self):
        return self.count

    def is_empty(self):
        return self.count == 0


# ============================================================
# 8. PRIORITY QUEUE
# ============================================================

class MatchPriorityQueue:

    def __init__(self):
        self.queue = []
        self.counter = 0

    def add_match(self, score, item_id):
        """
        Higher score = higher priority.
        Python heap is min-heap, so negative score is used.
        """

        heapq.heappush(
            self.queue,
            (-score, self.counter, item_id)
        )

        self.counter += 1

    def get_best_match(self):
        if not self.queue:
            return None

        score, _, item_id = heapq.heappop(self.queue)

        return {
            "item_id": item_id,
            "score": -score
        }

    def size(self):
        return len(self.queue)


# ============================================================
# 9. DEQUE
# ============================================================

class RecentActivityDeque:

    def __init__(self):
        self.activities = deque()

    def add_recent(self, activity):
        self.activities.appendleft(activity)

    def add_old(self, activity):
        self.activities.append(activity)

    def remove_recent(self):
        if self.activities:
            return self.activities.popleft()
        return None

    def remove_oldest(self):
        if self.activities:
            return self.activities.pop()
        return None

    def get_all(self):
        return list(self.activities)


# ============================================================
# TEST FUNCTION
# ============================================================

def test_dsa_structures():

    print("=" * 60)
    print("NMIET SMART LOST & FOUND - DSA CORE TEST")
    print("=" * 60)

    # Array
    items = ItemArray()
    items.add("Black Wallet")
    items.add("Blue Water Bottle")

    print("\nArray:")
    print(items.get_all())

    # Singly Linked List
    history = LostItemHistory()
    history.add("Lost Wallet")
    history.add("Lost ID Card")

    print("\nSingly Linked List:")
    print(history.get_all())

    # Doubly Linked List
    searches = SearchHistory()
    searches.add("Wallet")
    searches.add("ID Card")
    searches.add("Bottle")

    print("\nDoubly Linked List - Forward:")
    print(searches.get_forward())

    print("Doubly Linked List - Backward:")
    print(searches.get_backward())

    # Circular Linked List
    locations = CampusLocationCycle()
    locations.add("Library")
    locations.add("Canteen")
    locations.add("Laboratory")

    print("\nCircular Linked List:")
    print(locations.get_all())

    # Stack
    actions = ActionStack()
    actions.push("Report Lost Item")
    actions.push("Upload Image")
    actions.push("Edit Description")

    print("\nStack - Top Action:")
    print(actions.peek())

    print("Stack - Undo:")
    print(actions.pop())

    # Queue
    claims = ClaimQueue()
    claims.enqueue("Claim #101")
    claims.enqueue("Claim #102")
    claims.enqueue("Claim #103")

    print("\nQueue - First Claim:")
    print(claims.dequeue())

    # Circular Queue
    department_queue = CircularQueue(3)

    department_queue.enqueue("Library")
    department_queue.enqueue("Canteen")
    department_queue.enqueue("Laboratory")

    print("\nCircular Queue Size:")
    print(department_queue.size())

    # Priority Queue
    matches = MatchPriorityQueue()

    matches.add_match(72, 101)
    matches.add_match(95, 102)
    matches.add_match(84, 103)

    print("\nPriority Queue - Best Match:")
    print(matches.get_best_match())

    # Deque
    activities = RecentActivityDeque()

    activities.add_recent("Found Laptop")
    activities.add_recent("Lost Wallet")
    activities.add_recent("Found ID Card")

    print("\nDeque - Recent Activities:")
    print(activities.get_all())

    print("\n" + "=" * 60)
    print("ALL DSA CORE STRUCTURES TESTED SUCCESSFULLY")
    print("=" * 60)


# ============================================================
# RUN DIRECTLY
# ============================================================

if __name__ == "__main__":
    test_dsa_structures()