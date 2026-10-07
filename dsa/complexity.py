"""
ALGORITHM ANALYSIS & COMPLEXITY
Smart Lost & Found Management System
NMIET B.Tech AI & Data Science

Covered:
1. Time Complexity
2. Space Complexity
3. Big-O
4. Big-Omega
5. Big-Theta
6. Common Complexity Classes
7. Recurrence Relations
8. Complexity of Project DSA Algorithms
"""


# ============================================================
# 1. COMMON COMPLEXITY CLASSES
# ============================================================

COMPLEXITY_CLASSES = {

    "Constant": "O(1)",

    "Logarithmic": "O(log n)",

    "Linear": "O(n)",

    "Linearithmic": "O(n log n)",

    "Quadratic": "O(n^2)",

    "Cubic": "O(n^3)",

    "Exponential": "O(2^n)"

}


def display_complexity_classes():

    print("\n--- COMMON COMPLEXITY CLASSES ---")

    for name, notation in COMPLEXITY_CLASSES.items():

        print(
            f"{name:<15} : {notation}"
        )


# ============================================================
# 2. BIG-O
# ============================================================

def big_o_example(n):

    """
    Example of O(n).

    The loop executes n times.
    """

    operations = 0

    for _ in range(n):

        operations += 1

    return operations


# ============================================================
# 3. BIG-OMEGA
# ============================================================

def big_omega_example(items, target):

    """
    Demonstrates best-case / Omega behavior.

    If target is found at the first position,
    only one comparison is required.
    """

    if not items:

        return 0

    if items[0] == target:

        return 1

    return len(items)


# ============================================================
# 4. BIG-THETA
# ============================================================

def big_theta_example(n):

    """
    Performs exactly n operations.

    Therefore:

        Θ(n)
    """

    operations = 0

    for _ in range(n):

        operations += 1

    return operations


# ============================================================
# 5. LINEAR SEARCH COMPLEXITY
# ============================================================

def linear_search_with_operations(
    items,
    target
):

    operations = 0

    for index, item in enumerate(items):

        operations += 1

        if item == target:

            return index, operations

    return -1, operations


# ============================================================
# 6. BINARY SEARCH COMPLEXITY
# ============================================================

def binary_search_with_operations(
    items,
    target
):

    low = 0

    high = len(items) - 1

    operations = 0

    while low <= high:

        operations += 1

        middle = (
            low + high
        ) // 2

        if items[middle] == target:

            return middle, operations

        elif items[middle] < target:

            low = middle + 1

        else:

            high = middle - 1

    return -1, operations


# ============================================================
# 7. RECURSION
# ============================================================

def factorial(n):

    """
    Recursive factorial.

    Recurrence:

        T(n) = T(n-1) + O(1)

    Therefore:

        O(n)
    """

    if n <= 1:

        return 1

    return n * factorial(n - 1)


# ============================================================
# 8. FIBONACCI - EXPONENTIAL RECURSION
# ============================================================

def fibonacci_recursive(n):

    """
    Demonstrates exponential recursive complexity.

    Approximate complexity:

        O(2^n)
    """

    if n <= 1:

        return n

    return (
        fibonacci_recursive(n - 1)
        + fibonacci_recursive(n - 2)
    )


# ============================================================
# 9. FIBONACCI - DYNAMIC PROGRAMMING
# ============================================================

def fibonacci_dynamic(n):

    """
    Dynamic Programming version.

    Time Complexity: O(n)
    Space Complexity: O(n)
    """

    if n <= 1:

        return n

    dp = [0] * (n + 1)

    dp[1] = 1

    for i in range(2, n + 1):

        dp[i] = (
            dp[i - 1]
            + dp[i - 2]
        )

    return dp[n]


# ============================================================
# 10. SPACE COMPLEXITY EXAMPLE
# ============================================================

def create_storage(n):

    """
    Creates a list of n elements.

    Space Complexity:

        O(n)
    """

    data = []

    for i in range(n):

        data.append(i)

    return data


# ============================================================
# 11. PROJECT ALGORITHM COMPLEXITIES
# ============================================================

PROJECT_COMPLEXITIES = {

    "Array Access":
        "O(1)",

    "Linear Search":
        "O(n)",

    "Binary Search":
        "O(log n)",

    "Stack Push":
        "O(1)",

    "Stack Pop":
        "O(1)",

    "Queue Enqueue":
        "O(1)",

    "Queue Dequeue":
        "O(1)",

    "BST Search":
        "O(log n) average",

    "AVL Search":
        "O(log n)",

    "Heap Insert":
        "O(log n)",

    "Heap Delete":
        "O(log n)",

    "BFS":
        "O(V + E)",

    "DFS":
        "O(V + E)",

    "Dijkstra":
        "O((V + E) log V)",

    "Prim":
        "O(E log V)",

    "Kruskal":
        "O(E log E)",

    "Bubble Sort":
        "O(n^2)",

    "Selection Sort":
        "O(n^2)",

    "Insertion Sort":
        "O(n^2)",

    "Merge Sort":
        "O(n log n)",

    "Quick Sort":
        "O(n log n) average",

    "Radix Sort":
        "O(nk)",

    "Hash Table Search":
        "O(1) average",

    "Greedy Algorithms":
        "Depends on algorithm",

    "Dynamic Programming":
        "Depends on problem"

}


def display_project_complexities():

    print(
        "\n--- PROJECT ALGORITHM COMPLEXITIES ---"
    )

    for algorithm, complexity in (
        PROJECT_COMPLEXITIES.items()
    ):

        print(
            f"{algorithm:<25} : {complexity}"
        )


# ============================================================
# 12. RECURRENCE RELATION EXAMPLES
# ============================================================

RECURRENCE_RELATIONS = {

    "Linear Recursion":
        "T(n) = T(n-1) + O(1)  ->  O(n)",

    "Binary Search":
        "T(n) = T(n/2) + O(1)  ->  O(log n)",

    "Merge Sort":
        "T(n) = 2T(n/2) + O(n)  ->  O(n log n)",

    "Binary Tree Traversal":
        "T(n) = 2T(n/2) + O(1)  ->  O(n)",

    "Naive Fibonacci":
        "T(n) = T(n-1) + T(n-2) + O(1)  ->  O(2^n)"

}


def display_recurrence_relations():

    print(
        "\n--- RECURRENCE RELATIONS ---"
    )

    for algorithm, relation in (
        RECURRENCE_RELATIONS.items()
    ):

        print(
            f"{algorithm:<25} : {relation}"
        )


# ============================================================
# 13. COMPARE SEARCH ALGORITHMS
# ============================================================

def compare_search_algorithms():

    data = list(
        range(1, 1001)
    )

    target = 1000

    linear_index, linear_operations = (
        linear_search_with_operations(
            data,
            target
        )
    )

    binary_index, binary_operations = (
        binary_search_with_operations(
            data,
            target
        )
    )

    print(
        "\n--- SEARCH COMPARISON ---"
    )

    print(
        "Linear Search:"
    )

    print(
        "Index:",
        linear_index,
        "| Operations:",
        linear_operations,
        "| Complexity: O(n)"
    )

    print(
        "\nBinary Search:"
    )

    print(
        "Index:",
        binary_index,
        "| Operations:",
        binary_operations,
        "| Complexity: O(log n)"
    )


# ============================================================
# 14. TEST COMPLEXITY MODULE
# ============================================================

def test_complexity():

    print("=" * 70)

    print(
        "NMIET SMART LOST & FOUND - COMPLEXITY ANALYSIS"
    )

    print("=" * 70)

    # Complexity classes

    display_complexity_classes()

    # Big-O

    print(
        "\n--- BIG-O EXAMPLE ---"
    )

    print(
        "Operations for n = 10:",
        big_o_example(10)
    )

    print(
        "Complexity: O(n)"
    )

    # Big-Omega

    print(
        "\n--- BIG-OMEGA EXAMPLE ---"
    )

    items = [
        "Wallet",
        "Bottle",
        "ID Card",
        "Keys"
    ]

    print(
        "Best-case operations:",
        big_omega_example(
            items,
            "Wallet"
        )
    )

    print(
        "Best-case complexity: Ω(1)"
    )

    # Big-Theta

    print(
        "\n--- BIG-THETA EXAMPLE ---"
    )

    print(
        "Operations:",
        big_theta_example(10)
    )

    print(
        "Complexity: Θ(n)"
    )

    # Factorial

    print(
        "\n--- RECURSIVE FACTORIAL ---"
    )

    print(
        "5! =",
        factorial(5)
    )

    print(
        "Time Complexity: O(n)"
    )

    # Fibonacci

    print(
        "\n--- FIBONACCI COMPARISON ---"
    )

    print(
        "Recursive Fibonacci(10):",
        fibonacci_recursive(10)
    )

    print(
        "Dynamic Fibonacci(10):",
        fibonacci_dynamic(10)
    )

    print(
        "Recursive Complexity: O(2^n)"
    )

    print(
        "Dynamic Programming Complexity: O(n)"
    )

    # Space

    print(
        "\n--- SPACE COMPLEXITY ---"
    )

    storage = create_storage(10)

    print(
        "Created elements:",
        len(storage)
    )

    print(
        "Space Complexity: O(n)"
    )

    # Search comparison

    compare_search_algorithms()

    # Project complexities

    display_project_complexities()

    # Recurrence relations

    display_recurrence_relations()

    print("\n" + "=" * 70)

    print(
        "ALL COMPLEXITY ANALYSIS TESTS COMPLETED"
    )

    print("=" * 70)


# ============================================================
# RUN DIRECTLY
# ============================================================

if __name__ == "__main__":

    test_complexity()