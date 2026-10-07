"""
ADVANCED ALGORITHMS
Smart Lost & Found Management System
NMIET B.Tech AI & Data Science

Covered:
1. Greedy Algorithm
2. Activity Selection
3. Greedy Item Matching
4. Dynamic Programming
5. 0/1 Knapsack
6. Longest Common Subsequence
7. Lost & Found Match Optimization
"""


# ============================================================
# 1. GREEDY - ACTIVITY SELECTION
# ============================================================

def activity_selection(activities):
    """
    Selects the maximum number of non-overlapping activities.

    Each activity:
        (activity_name, start_time, finish_time)
    """

    activities = sorted(
        activities,
        key=lambda activity: activity[2]
    )

    selected = []

    last_finish = -1

    for activity in activities:

        name, start, finish = activity

        if start >= last_finish:

            selected.append(activity)

            last_finish = finish

    return selected


# ============================================================
# 2. GREEDY - LOST & FOUND ITEM MATCHING
# ============================================================

def greedy_match_score(lost_item, found_item):
    """
    Calculates a match score using a greedy approach.

    Higher matching attributes receive points.
    Maximum score = 100.
    """

    score = 0

    # Category
    if (
        lost_item.get("category")
        and found_item.get("category")
        and lost_item["category"].lower()
        == found_item["category"].lower()
    ):
        score += 25

    # Item name
    lost_name = str(
        lost_item.get("item_name", "")
    ).lower()

    found_name = str(
        found_item.get("item_name", "")
    ).lower()

    if (
        lost_name
        and found_name
        and (
            lost_name in found_name
            or found_name in lost_name
        )
    ):
        score += 25

    # Location
    if (
        lost_item.get("location")
        and found_item.get("location")
        and lost_item["location"].lower()
        == found_item["location"].lower()
    ):
        score += 20

    # Color
    if (
        lost_item.get("color")
        and found_item.get("color")
        and lost_item["color"].lower()
        == found_item["color"].lower()
    ):
        score += 10

    # Brand
    if (
        lost_item.get("brand")
        and found_item.get("brand")
        and lost_item["brand"].lower()
        == found_item["brand"].lower()
    ):
        score += 10

    # Specific area
    if (
        lost_item.get("specific_area")
        and found_item.get("specific_area")
        and lost_item["specific_area"].lower()
        == found_item["specific_area"].lower()
    ):
        score += 10

    return score


# ============================================================
# 3. GREEDY - PRIORITY CLAIM SELECTION
# ============================================================

def prioritize_claims(claims):
    """
    Greedily processes claims with higher priority first.

    Expected claim format:
        {
            "claimant": "...",
            "match_score": 90,
            "verification": 1
        }
    """

    def priority(claim):

        score = claim.get(
            "match_score",
            0
        )

        verification = claim.get(
            "verification",
            0
        )

        return (
            verification,
            score
        )

    return sorted(
        claims,
        key=priority,
        reverse=True
    )


# ============================================================
# 4. DYNAMIC PROGRAMMING - 0/1 KNAPSACK
# ============================================================

def knapsack(values, weights, capacity):
    """
    Classic 0/1 Knapsack Dynamic Programming algorithm.

    Used to select the best combination of items
    within a limited capacity.
    """

    n = len(values)

    dp = [
        [0 for _ in range(capacity + 1)]
        for _ in range(n + 1)
    ]

    for i in range(1, n + 1):

        for current_capacity in range(
            capacity + 1
        ):

            if (
                weights[i - 1]
                <= current_capacity
            ):

                dp[i][current_capacity] = max(
                    dp[i - 1][current_capacity],

                    values[i - 1]
                    + dp[
                        i - 1
                    ][
                        current_capacity
                        - weights[i - 1]
                    ]
                )

            else:

                dp[i][current_capacity] = (
                    dp[i - 1][current_capacity]
                )

    return dp[n][capacity]


# ============================================================
# 5. DYNAMIC PROGRAMMING - LONGEST COMMON SUBSEQUENCE
# ============================================================

def longest_common_subsequence(text1, text2):
    """
    Finds the Longest Common Subsequence.

    Useful for comparing item descriptions
    and finding common text patterns.
    """

    m = len(text1)
    n = len(text2)

    dp = [
        ["" for _ in range(n + 1)]
        for _ in range(m + 1)
    ]

    for i in range(1, m + 1):

        for j in range(1, n + 1):

            if text1[i - 1] == text2[j - 1]:

                dp[i][j] = (
                    dp[i - 1][j - 1]
                    + text1[i - 1]
                )

            else:

                if len(dp[i - 1][j]) >= len(
                    dp[i][j - 1]
                ):

                    dp[i][j] = dp[i - 1][j]

                else:

                    dp[i][j] = dp[i][j - 1]

    return dp[m][n]


# ============================================================
# 6. DP - ITEM DESCRIPTION SIMILARITY
# ============================================================

def description_similarity(
    lost_description,
    found_description
):
    """
    Uses LCS to calculate a simple
    description similarity percentage.
    """

    lost_description = str(
        lost_description
    ).lower()

    found_description = str(
        found_description
    ).lower()

    if not lost_description or not found_description:
        return 0

    common = longest_common_subsequence(
        lost_description,
        found_description
    )

    longest_length = max(
        len(lost_description),
        len(found_description)
    )

    similarity = (
        len(common)
        / longest_length
    ) * 100

    return round(
        similarity,
        2
    )


# ============================================================
# 7. DYNAMIC PROGRAMMING - OPTIMAL MATCH
# ============================================================

def optimize_matches(match_scores, maximum_matches):
    """
    Selects the maximum total match score
    from available match scores.

    Dynamic Programming is used to determine
    the best number of matches.
    """

    if maximum_matches <= 0:
        return 0

    n = len(match_scores)

    if n == 0:
        return 0

    dp = [
        [0 for _ in range(maximum_matches + 1)]
        for _ in range(n + 1)
    ]

    for i in range(1, n + 1):

        score = match_scores[i - 1]

        for count in range(
            1,
            maximum_matches + 1
        ):

            dp[i][count] = max(
                dp[i - 1][count],

                score
                + dp[
                    i - 1
                ][
                    count - 1
                ]
            )

    return dp[n][maximum_matches]


# ============================================================
# 8. TEST ADVANCED ALGORITHMS
# ============================================================

def test_advanced_algorithms():

    print("=" * 70)
    print("NMIET SMART LOST & FOUND - ADVANCED ALGORITHMS TEST")
    print("=" * 70)

    # --------------------------------------------------------
    # Greedy Activity Selection
    # --------------------------------------------------------

    print("\n--- GREEDY: ACTIVITY SELECTION ---")

    activities = [

        ("Library Verification", 1, 3),

        ("Canteen Verification", 2, 5),

        ("Lab Verification", 4, 6),

        ("Classroom Verification", 6, 8),

        ("Office Verification", 5, 9)

    ]

    selected = activity_selection(
        activities
    )

    print("Selected activities:")

    for activity in selected:

        print(
            activity
        )

    # --------------------------------------------------------
    # Greedy Item Matching
    # --------------------------------------------------------

    print("\n--- GREEDY: LOST & FOUND MATCHING ---")

    lost_item = {

        "item_name": "Black Wallet",

        "category": "Accessories",

        "location": "Library",

        "color": "Black",

        "brand": "Wildcraft",

        "specific_area": "Reading Room"

    }

    found_item = {

        "item_name": "Black Wallet",

        "category": "Accessories",

        "location": "Library",

        "color": "Black",

        "brand": "Wildcraft",

        "specific_area": "Reading Room"

    }

    score = greedy_match_score(
        lost_item,
        found_item
    )

    print(
        "Greedy Match Score:",
        score,
        "%"
    )

    # --------------------------------------------------------
    # Priority Claims
    # --------------------------------------------------------

    print("\n--- GREEDY: CLAIM PRIORITY ---")

    claims = [

        {
            "claimant": "Student A",
            "match_score": 70,
            "verification": 0
        },

        {
            "claimant": "Student B",
            "match_score": 92,
            "verification": 1
        },

        {
            "claimant": "Student C",
            "match_score": 85,
            "verification": 1
        }

    ]

    prioritized = prioritize_claims(
        claims
    )

    for claim in prioritized:

        print(
            claim["claimant"],
            "->",
            claim["match_score"],
            "%"
        )

    # --------------------------------------------------------
    # Knapsack
    # --------------------------------------------------------

    print("\n--- DYNAMIC PROGRAMMING: KNAPSACK ---")

    values = [
        60,
        100,
        120
    ]

    weights = [
        10,
        20,
        30
    ]

    capacity = 50

    maximum_value = knapsack(
        values,
        weights,
        capacity
    )

    print(
        "Maximum value:",
        maximum_value
    )

    # --------------------------------------------------------
    # LCS
    # --------------------------------------------------------

    print(
        "\n--- DYNAMIC PROGRAMMING: LCS ---"
    )

    text1 = "black wallet"

    text2 = "black leather wallet"

    common = longest_common_subsequence(
        text1,
        text2
    )

    print(
        "Common sequence:",
        common
    )

    # --------------------------------------------------------
    # Description Similarity
    # --------------------------------------------------------

    print(
        "\n--- ITEM DESCRIPTION SIMILARITY ---"
    )

    similarity = description_similarity(

        "black leather wallet with college ID",

        "black wallet with college ID"

    )

    print(
        "Description similarity:",
        similarity,
        "%"
    )

    # --------------------------------------------------------
    # Optimal Match
    # --------------------------------------------------------

    print(
        "\n--- DP: OPTIMAL MATCH SELECTION ---"
    )

    match_scores = [
        92,
        85,
        75,
        60,
        55
    ]

    best_score = optimize_matches(
        match_scores,
        3
    )

    print(
        "Best total score:",
        best_score
    )

    print("\n" + "=" * 70)
    print(
        "ALL ADVANCED ALGORITHM TESTS COMPLETED"
    )
    print("=" * 70)


# ============================================================
# RUN DIRECTLY
# ============================================================

if __name__ == "__main__":
    test_advanced_algorithms()