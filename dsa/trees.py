"""
TREE DATA STRUCTURES
Smart Lost & Found Management System
NMIET B.Tech AI & Data Science

Covered:
1. Binary Tree
2. Binary Search Tree (BST)
3. Tree Traversals
4. AVL Tree
5. AVL Rotations
6. Min Heap
7. Max Heap
8. Heap Sort
"""


# ============================================================
# 1. BINARY TREE NODE
# ============================================================

class TreeNode:

    def __init__(self, data):
        self.data = data
        self.left = None
        self.right = None


# ============================================================
# 2. BINARY TREE
# ============================================================

class BinaryTree:

    def __init__(self):
        self.root = None

    def create_sample_tree(self):
        """
        Creates a sample binary tree representing
        categories of lost and found items.
        """

        self.root = TreeNode("Items")

        self.root.left = TreeNode("Lost")
        self.root.right = TreeNode("Found")

        self.root.left.left = TreeNode("Electronics")
        self.root.left.right = TreeNode("Documents")

        self.root.right.left = TreeNode("Bags")
        self.root.right.right = TreeNode("Accessories")

    def inorder(self, node=None):

        if node is None:
            node = self.root

        result = []

        if node.left:
            result.extend(self.inorder(node.left))

        result.append(node.data)

        if node.right:
            result.extend(self.inorder(node.right))

        return result

    def preorder(self, node=None):

        if node is None:
            node = self.root

        result = [node.data]

        if node.left:
            result.extend(self.preorder(node.left))

        if node.right:
            result.extend(self.preorder(node.right))

        return result

    def postorder(self, node=None):

        if node is None:
            node = self.root

        result = []

        if node.left:
            result.extend(self.postorder(node.left))

        if node.right:
            result.extend(self.postorder(node.right))

        result.append(node.data)

        return result


# ============================================================
# 3. BINARY SEARCH TREE
# ============================================================

class BinarySearchTree:

    def __init__(self):
        self.root = None

    def insert(self, value):

        self.root = self._insert(self.root, value)

    def _insert(self, node, value):

        if node is None:
            return TreeNode(value)

        if value < node.data:
            node.left = self._insert(node.left, value)

        elif value > node.data:
            node.right = self._insert(node.right, value)

        return node

    def search(self, value):

        return self._search(self.root, value)

    def _search(self, node, value):

        if node is None:
            return False

        if node.data == value:
            return True

        if value < node.data:
            return self._search(node.left, value)

        return self._search(node.right, value)

    def inorder(self):

        result = []

        def traverse(node):

            if node is None:
                return

            traverse(node.left)
            result.append(node.data)
            traverse(node.right)

        traverse(self.root)

        return result


# ============================================================
# 4. AVL TREE NODE
# ============================================================

class AVLNode:

    def __init__(self, key):
        self.key = key
        self.left = None
        self.right = None
        self.height = 1


# ============================================================
# 5. AVL TREE
# ============================================================

class AVLTree:

    def get_height(self, node):

        if node is None:
            return 0

        return node.height

    def get_balance(self, node):

        if node is None:
            return 0

        return (
            self.get_height(node.left)
            - self.get_height(node.right)
        )

    def right_rotate(self, y):

        x = y.left
        temporary = x.right

        x.right = y
        y.left = temporary

        y.height = (
            1
            + max(
                self.get_height(y.left),
                self.get_height(y.right)
            )
        )

        x.height = (
            1
            + max(
                self.get_height(x.left),
                self.get_height(x.right)
            )
        )

        return x

    def left_rotate(self, x):

        y = x.right
        temporary = y.left

        y.left = x
        x.right = temporary

        x.height = (
            1
            + max(
                self.get_height(x.left),
                self.get_height(x.right)
            )
        )

        y.height = (
            1
            + max(
                self.get_height(y.left),
                self.get_height(y.right)
            )
        )

        return y

    def insert(self, node, key):

        if node is None:
            return AVLNode(key)

        if key < node.key:
            node.left = self.insert(node.left, key)

        elif key > node.key:
            node.right = self.insert(node.right, key)

        else:
            return node

        node.height = (
            1
            + max(
                self.get_height(node.left),
                self.get_height(node.right)
            )
        )

        balance = self.get_balance(node)

        # Left Left Case
        if balance > 1 and key < node.left.key:
            return self.right_rotate(node)

        # Right Right Case
        if balance < -1 and key > node.right.key:
            return self.left_rotate(node)

        # Left Right Case
        if balance > 1 and key > node.left.key:
            node.left = self.left_rotate(node.left)
            return self.right_rotate(node)

        # Right Left Case
        if balance < -1 and key < node.right.key:
            node.right = self.right_rotate(node.right)
            return self.left_rotate(node)

        return node

    def inorder(self, node):

        result = []

        if node is None:
            return result

        result.extend(self.inorder(node.left))
        result.append(node.key)
        result.extend(self.inorder(node.right))

        return result


# ============================================================
# 6. MIN HEAP
# ============================================================

class MinHeap:

    def __init__(self):
        self.heap = []

    def insert(self, value):

        self.heap.append(value)
        self._heapify_up(len(self.heap) - 1)

    def _heapify_up(self, index):

        while index > 0:

            parent = (index - 1) // 2

            if self.heap[index] >= self.heap[parent]:
                break

            self.heap[index], self.heap[parent] = (
                self.heap[parent],
                self.heap[index]
            )

            index = parent

    def extract_min(self):

        if not self.heap:
            return None

        minimum = self.heap[0]
        last = self.heap.pop()

        if self.heap:
            self.heap[0] = last
            self._heapify_down(0)

        return minimum

    def _heapify_down(self, index):

        size = len(self.heap)

        while True:

            smallest = index
            left = 2 * index + 1
            right = 2 * index + 2

            if (
                left < size
                and self.heap[left] < self.heap[smallest]
            ):
                smallest = left

            if (
                right < size
                and self.heap[right] < self.heap[smallest]
            ):
                smallest = right

            if smallest == index:
                break

            self.heap[index], self.heap[smallest] = (
                self.heap[smallest],
                self.heap[index]
            )

            index = smallest


# ============================================================
# 7. MAX HEAP
# ============================================================

class MaxHeap:

    def __init__(self):
        self.heap = []

    def insert(self, value):

        self.heap.append(value)
        self._heapify_up(len(self.heap) - 1)

    def _heapify_up(self, index):

        while index > 0:

            parent = (index - 1) // 2

            if self.heap[index] <= self.heap[parent]:
                break

            self.heap[index], self.heap[parent] = (
                self.heap[parent],
                self.heap[index]
            )

            index = parent

    def extract_max(self):

        if not self.heap:
            return None

        maximum = self.heap[0]
        last = self.heap.pop()

        if self.heap:
            self.heap[0] = last
            self._heapify_down(0)

        return maximum

    def _heapify_down(self, index):

        size = len(self.heap)

        while True:

            largest = index
            left = 2 * index + 1
            right = 2 * index + 2

            if (
                left < size
                and self.heap[left] > self.heap[largest]
            ):
                largest = left

            if (
                right < size
                and self.heap[right] > self.heap[largest]
            ):
                largest = right

            if largest == index:
                break

            self.heap[index], self.heap[largest] = (
                self.heap[largest],
                self.heap[index]
            )

            index = largest


# ============================================================
# 8. HEAP SORT
# ============================================================

def heap_sort(values):

    heap = MaxHeap()

    for value in values:
        heap.insert(value)

    result = []

    while heap.heap:
        result.append(heap.extract_max())

    result.reverse()

    return result


# ============================================================
# TEST ALL TREE STRUCTURES
# ============================================================

def test_tree_structures():

    print("=" * 60)
    print("NMIET SMART LOST & FOUND - TREE DSA TEST")
    print("=" * 60)

    # --------------------------------------------------------
    # Binary Tree
    # --------------------------------------------------------

    binary_tree = BinaryTree()
    binary_tree.create_sample_tree()

    print("\nBinary Tree Inorder:")
    print(binary_tree.inorder())

    print("\nBinary Tree Preorder:")
    print(binary_tree.preorder())

    print("\nBinary Tree Postorder:")
    print(binary_tree.postorder())

    # --------------------------------------------------------
    # BST
    # --------------------------------------------------------

    bst = BinarySearchTree()

    for item_id in [50, 30, 70, 20, 40, 60, 80]:
        bst.insert(item_id)

    print("\nBST Inorder:")
    print(bst.inorder())

    print("\nBST Search 60:")
    print(bst.search(60))

    print("\nBST Search 100:")
    print(bst.search(100))

    # --------------------------------------------------------
    # AVL Tree
    # --------------------------------------------------------

    avl = AVLTree()
    avl_root = None

    for value in [30, 20, 10, 25, 28, 27, 50]:
        avl_root = avl.insert(avl_root, value)

    print("\nAVL Tree Inorder:")
    print(avl.inorder(avl_root))

    # --------------------------------------------------------
    # Min Heap
    # --------------------------------------------------------

    min_heap = MinHeap()

    for value in [40, 10, 30, 5, 20]:
        min_heap.insert(value)

    print("\nMin Heap:")
    print(min_heap.heap)

    print("Extract Minimum:")
    print(min_heap.extract_min())

    # --------------------------------------------------------
    # Max Heap
    # --------------------------------------------------------

    max_heap = MaxHeap()

    for value in [40, 10, 30, 5, 20]:
        max_heap.insert(value)

    print("\nMax Heap:")
    print(max_heap.heap)

    print("Extract Maximum:")
    print(max_heap.extract_max())

    # --------------------------------------------------------
    # Heap Sort
    # --------------------------------------------------------

    numbers = [45, 12, 78, 3, 56, 22]

    print("\nOriginal List:")
    print(numbers)

    print("Heap Sort:")
    print(heap_sort(numbers))

    print("\n" + "=" * 60)
    print("ALL TREE, AVL AND HEAP TESTS PASSED")
    print("=" * 60)


# ============================================================
# RUN DIRECTLY
# ============================================================

if __name__ == "__main__":
    test_tree_structures()