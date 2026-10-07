"""
SEARCHING & SORTING ALGORITHMS
Smart Lost & Found Management System
NMIET B.Tech AI & Data Science

Covered:
1. Linear Search
2. Binary Search
3. Bubble Sort
4. Selection Sort
5. Insertion Sort
6. Merge Sort
7. Quick Sort
8. Radix Sort
"""


# ============================================================
# 1. LINEAR SEARCH
# ============================================================

def linear_search(items, target):

    for index in range(len(items)):

        if items[index] == target:
            return index

    return -1


# ============================================================
# 2. BINARY SEARCH
# ============================================================

def binary_search(items, target):

    left = 0
    right = len(items) - 1

    while left <= right:

        middle = (left + right) // 2

        if items[middle] == target:
            return middle

        elif items[middle] < target:
            left = middle + 1

        else:
            right = middle - 1

    return -1


# ============================================================
# 3. BUBBLE SORT
# ============================================================

def bubble_sort(items):

    arr = items.copy()
    n = len(arr)

    for i in range(n):

        swapped = False

        for j in range(0, n - i - 1):

            if arr[j] > arr[j + 1]:

                arr[j], arr[j + 1] = (
                    arr[j + 1],
                    arr[j]
                )

                swapped = True

        if not swapped:
            break

    return arr


# ============================================================
# 4. SELECTION SORT
# ============================================================

def selection_sort(items):

    arr = items.copy()
    n = len(arr)

    for i in range(n):

        minimum_index = i

        for j in range(i + 1, n):

            if arr[j] < arr[minimum_index]:
                minimum_index = j

        arr[i], arr[minimum_index] = (
            arr[minimum_index],
            arr[i]
        )

    return arr


# ============================================================
# 5. INSERTION SORT
# ============================================================

def insertion_sort(items):

    arr = items.copy()

    for i in range(1, len(arr)):

        current = arr[i]
        position = i - 1

        while (
            position >= 0
            and arr[position] > current
        ):

            arr[position + 1] = arr[position]
            position -= 1

        arr[position + 1] = current

    return arr


# ============================================================
# 6. MERGE SORT
# ============================================================

def merge_sort(items):

    if len(items) <= 1:
        return items.copy()

    middle = len(items) // 2

    left = merge_sort(items[:middle])
    right = merge_sort(items[middle:])

    return merge(left, right)


def merge(left, right):

    result = []

    i = 0
    j = 0

    while i < len(left) and j < len(right):

        if left[i] <= right[j]:

            result.append(left[i])
            i += 1

        else:

            result.append(right[j])
            j += 1

    result.extend(left[i:])
    result.extend(right[j:])

    return result


# ============================================================
# 7. QUICK SORT
# ============================================================

def quick_sort(items):

    if len(items) <= 1:
        return items.copy()

    pivot = items[-1]

    smaller = []
    equal = []
    greater = []

    for item in items:

        if item < pivot:
            smaller.append(item)

        elif item == pivot:
            equal.append(item)

        else:
            greater.append(item)

    return (
        quick_sort(smaller)
        + equal
        + quick_sort(greater)
    )


# ============================================================
# 8. RADIX SORT
# ============================================================

def radix_sort(items):

    if not items:
        return []

    arr = items.copy()

    # Radix sort here handles non-negative integers.
    if any(number < 0 for number in arr):
        raise ValueError(
            "Radix Sort supports non-negative integers only."
        )

    maximum = max(arr)
    place = 1

    while maximum // place > 0:

        buckets = [[] for _ in range(10)]

        for number in arr:

            digit = (
                number // place
            ) % 10

            buckets[digit].append(number)

        arr = []

        for bucket in buckets:
            arr.extend(bucket)

        place *= 10

    return arr


# ============================================================
# ITEM SEARCHING
# ============================================================

def search_item_by_id(items, item_id):

    """
    Linear search for item records.

    Each item should contain an 'id' field.
    """

    for item in items:

        if item.get("id") == item_id:
            return item

    return None


def binary_search_item_ids(items, item_id):

    """
    Binary search for item records.

    The items must already be sorted
    by ID in ascending order.
    """

    left = 0
    right = len(items) - 1

    while left <= right:

        middle = (left + right) // 2

        current_id = items[middle].get("id")

        if current_id == item_id:
            return items[middle]

        if current_id < item_id:
            left = middle + 1

        else:
            right = middle - 1

    return None


# ============================================================
# TEST ALL SEARCHING & SORTING ALGORITHMS
# ============================================================

def test_searching_sorting():

    print("=" * 65)
    print("NMIET SMART LOST & FOUND - SEARCHING & SORTING TEST")
    print("=" * 65)

    numbers = [64, 25, 12, 22, 11, 90, 34, 5]

    print("\nOriginal List:")
    print(numbers)

    # --------------------------------------------------------
    # Linear Search
    # --------------------------------------------------------

    print("\n--- LINEAR SEARCH ---")

    target = 22

    result = linear_search(
        numbers,
        target
    )

    print(f"Searching for {target}")

    print(f"Index: {result}")

    # --------------------------------------------------------
    # Binary Search
    # --------------------------------------------------------

    print("\n--- BINARY SEARCH ---")

    sorted_numbers = sorted(numbers)

    print("Sorted List:")
    print(sorted_numbers)

    target = 34

    result = binary_search(
        sorted_numbers,
        target
    )

    print(f"Searching for {target}")

    print(f"Index: {result}")

    # --------------------------------------------------------
    # Bubble Sort
    # --------------------------------------------------------

    print("\n--- BUBBLE SORT ---")

    print(bubble_sort(numbers))

    # --------------------------------------------------------
    # Selection Sort
    # --------------------------------------------------------

    print("\n--- SELECTION SORT ---")

    print(selection_sort(numbers))

    # --------------------------------------------------------
    # Insertion Sort
    # --------------------------------------------------------

    print("\n--- INSERTION SORT ---")

    print(insertion_sort(numbers))

    # --------------------------------------------------------
    # Merge Sort
    # --------------------------------------------------------

    print("\n--- MERGE SORT ---")

    print(merge_sort(numbers))

    # --------------------------------------------------------
    # Quick Sort
    # --------------------------------------------------------

    print("\n--- QUICK SORT ---")

    print(quick_sort(numbers))

    # --------------------------------------------------------
    # Radix Sort
    # --------------------------------------------------------

    print("\n--- RADIX SORT ---")

    radix_numbers = [
        170,
        45,
        75,
        90,
        802,
        24,
        2,
        66
    ]

    print(radix_sort(radix_numbers))

    # --------------------------------------------------------
    # Item Search
    # --------------------------------------------------------

    print("\n--- ITEM ID SEARCH ---")

    items = [
        {
            "id": 101,
            "name": "Black Wallet"
        },
        {
            "id": 102,
            "name": "Blue Bottle"
        },
        {
            "id": 103,
            "name": "Student ID Card"
        }
    ]

    found_item = search_item_by_id(
        items,
        102
    )

    print("Linear Search Result:")
    print(found_item)

    found_item = binary_search_item_ids(
        items,
        103
    )

    print("\nBinary Search Result:")
    print(found_item)

    print("\n" + "=" * 65)
    print("ALL SEARCHING & SORTING ALGORITHMS TESTED")
    print("=" * 65)


# ============================================================
# RUN DIRECTLY
# ============================================================

if __name__ == "__main__":
    test_searching_sorting()