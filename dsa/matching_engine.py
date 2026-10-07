"""
SMART LOST & FOUND - DSA MATCHING ENGINE
NMIET B.Tech AI & Data Science

DSA used:
1. Hashing
2. Linear Search
3. Sorting
4. Priority Queue / Heap
5. Greedy Algorithm
6. Dynamic Programming
"""

import heapq


# ============================================================
# IMPORT PROJECT DSA MODULES
# ============================================================

from .advanced_algorithms import (
    greedy_match_score,
    description_similarity
)


# ============================================================
# 1. NORMALIZE TEXT
# ============================================================

def normalize_text(value):

    if value is None:
        return ""

    return str(value).strip().lower()


# ============================================================
# 2. HASH-BASED ITEM INDEX
# ============================================================

class ItemHashIndex:

    def __init__(self):

        self.index = {}

    def add(self, item):

        item_id = item.get("id")

        if item_id is not None:

            self.index[item_id] = item

    def add_many(self, items):

        for item in items:

            self.add(item)

    def get(self, item_id):

        return self.index.get(item_id)

    def remove(self, item_id):

        if item_id in self.index:

            del self.index[item_id]

            return True

        return False

    def size(self):

        return len(self.index)


# ============================================================
# 3. FIELD MATCHING
# ============================================================

def field_match(
    lost_item,
    found_item,
    field
):

    lost_value = normalize_text(
        lost_item.get(field)
    )

    found_value = normalize_text(
        found_item.get(field)
    )

    if not lost_value or not found_value:

        return 0

    if lost_value == found_value:

        return 1

    if (
        lost_value in found_value
        or found_value in lost_value
    ):

        return 0.5

    return 0


# ============================================================
# 4. DESCRIPTION MATCHING
# ============================================================

def description_match(
    lost_item,
    found_item
):

    lost_description = (
        lost_item.get("description")
        or ""
    )

    found_description = (
        found_item.get("description")
        or ""
    )

    return description_similarity(
        lost_description,
        found_description
    )


# ============================================================
# 5. COMPLETE MATCH SCORE
# ============================================================

def calculate_match_score(
    lost_item,
    found_item
):

    # Greedy algorithm score
    greedy_score = greedy_match_score(
        lost_item,
        found_item
    )

    # Dynamic Programming description score
    description_score = description_match(
        lost_item,
        found_item
    )

    # Date matching
    date_score = field_match(
        lost_item,
        found_item,
        "item_date"
    )

    # Time matching
    time_score = field_match(
        lost_item,
        found_item,
        "item_time"
    )

    # Description = maximum 10 points
    description_points = (
        description_score / 100
    ) * 10

    # Date = maximum 5 points
    date_points = (
        date_score * 5
    )

    # Time = maximum 5 points
    time_points = (
        time_score * 5
    )

    final_score = (
        greedy_score
        + description_points
        + date_points
        + time_points
    )

    final_score = min(
        100,
        final_score
    )

    return round(
        final_score,
        2
    )


# ============================================================
# 6. PRIORITY QUEUE FOR MATCHES
# ============================================================

def rank_matches(matches):

    priority_queue = []

    for match in matches:

        score = match["score"]

        heapq.heappush(
            priority_queue,
            (
                -score,
                match
            )
        )

    ranked = []

    while priority_queue:

        _, match = heapq.heappop(
            priority_queue
        )

        ranked.append(match)

    return ranked


# ============================================================
# 7. FIND ALL MATCHES
# ============================================================

def find_matches(
    lost_item,
    found_items,
    minimum_score=20
):

    possible_matches = []

    for found_item in found_items:

        if (
            lost_item.get("id") is not None
            and
            found_item.get("id")
            == lost_item.get("id")
        ):

            continue

        score = calculate_match_score(
            lost_item,
            found_item
        )

        if score >= minimum_score:

            possible_matches.append({

                "item_id":
                    found_item.get("id"),

                "item_name":
                    found_item.get("item_name"),

                "category":
                    found_item.get("category"),

                "location":
                    found_item.get("location"),

                "specific_area":
                    found_item.get("specific_area"),

                "color":
                    found_item.get("color"),

                "brand":
                    found_item.get("brand"),

                "score":
                    score

            })

    return rank_matches(
        possible_matches
    )


# ============================================================
# 8. SEARCH ITEMS
# ============================================================

def search_items_linear(
    items,
    keyword
):

    keyword = normalize_text(
        keyword
    )

    if not keyword:

        return items

    results = []

    for item in items:

        searchable_text = " ".join([

            normalize_text(
                item.get("item_name")
            ),

            normalize_text(
                item.get("category")
            ),

            normalize_text(
                item.get("description")
            ),

            normalize_text(
                item.get("location")
            ),

            normalize_text(
                item.get("color")
            ),

            normalize_text(
                item.get("brand")
            )

        ])

        if keyword in searchable_text:

            results.append(item)

    return results


# ============================================================
# 9. SEARCH ITEM BY ID USING HASHING
# ============================================================

def search_item_by_id(
    items,
    item_id
):

    index = ItemHashIndex()

    index.add_many(
        items
    )

    return index.get(
        item_id
    )


# ============================================================
# 10. SEARCH BY CATEGORY
# ============================================================

def search_by_category(
    items,
    category
):

    category = normalize_text(
        category
    )

    results = []

    for item in items:

        item_category = normalize_text(
            item.get("category")
        )

        if item_category == category:

            results.append(item)

    return results


# ============================================================
# 11. MATCH SUMMARY
# ============================================================

def match_summary(
    lost_item,
    found_items
):

    matches = find_matches(
        lost_item,
        found_items
    )

    return {

        "lost_item_id":
            lost_item.get("id"),

        "lost_item_name":
            lost_item.get("item_name"),

        "total_matches":
            len(matches),

        "best_match":
            matches[0]
            if matches
            else None,

        "matches":
            matches

    }


# ============================================================
# 12. DEMONSTRATION DATA
# ============================================================

def demo_data():

    lost_item = {

        "id": 1,

        "item_name":
            "Black Wallet",

        "category":
            "Accessories",

        "description":
            "Black leather wallet with college ID",

        "item_date":
            "2026-10-01",

        "item_time":
            "10:30",

        "location":
            "Library",

        "specific_area":
            "Reading Room",

        "color":
            "Black",

        "brand":
            "Wildcraft"

    }

    found_items = [

        {

            "id": 2,

            "item_name":
                "Black Wallet",

            "category":
                "Accessories",

            "description":
                "Black wallet containing a college ID",

            "item_date":
                "2026-10-01",

            "item_time":
                "10:35",

            "location":
                "Library",

            "specific_area":
                "Reading Room",

            "color":
                "Black",

            "brand":
                "Wildcraft"

        },

        {

            "id": 3,

            "item_name":
                "Blue Water Bottle",

            "category":
                "Bottle",

            "description":
                "Blue bottle found near canteen",

            "item_date":
                "2026-10-01",

            "item_time":
                "12:00",

            "location":
                "Canteen",

            "specific_area":
                "Main Counter",

            "color":
                "Blue",

            "brand":
                "Milton"

        },

        {

            "id": 4,

            "item_name":
                "Black Purse",

            "category":
                "Accessories",

            "description":
                "Black purse found in corridor",

            "item_date":
                "2026-09-30",

            "item_time":
                "09:00",

            "location":
                "Corridor",

            "specific_area":
                "First Floor",

            "color":
                "Black",

            "brand":
                ""

        }

    ]

    return (
        lost_item,
        found_items
    )


# ============================================================
# 13. TEST MATCHING ENGINE
# ============================================================

def test_matching_engine():

    print("=" * 75)

    print(
        "NMIET SMART LOST & FOUND - DSA MATCHING ENGINE"
    )

    print("=" * 75)


    lost_item, found_items = demo_data()


    # --------------------------------------------------------
    # HASHING
    # --------------------------------------------------------

    print(
        "\n--- HASHING: FAST ITEM LOOKUP ---"
    )

    item_index = ItemHashIndex()

    item_index.add_many(
        found_items
    )

    print(
        "Indexed items:",
        item_index.size()
    )

    found_item = item_index.get(2)

    print(
        "Item ID 2:",
        found_item["item_name"]
        if found_item
        else "Not Found"
    )


    # --------------------------------------------------------
    # LINEAR SEARCH
    # --------------------------------------------------------

    print(
        "\n--- LINEAR SEARCH ---"
    )

    search_results = search_items_linear(
        found_items,
        "black"
    )

    print(
        "Items containing 'black':",
        len(search_results)
    )

    for item in search_results:

        print(
            "-",
            item["item_name"]
        )


    # --------------------------------------------------------
    # CATEGORY SEARCH
    # --------------------------------------------------------

    print(
        "\n--- CATEGORY SEARCH ---"
    )

    category_results = search_by_category(
        found_items,
        "Accessories"
    )

    print(
        "Accessories found:",
        len(category_results)
    )


    # --------------------------------------------------------
    # SMART MATCHING
    # --------------------------------------------------------

    print(
        "\n--- SMART DSA MATCHING ---"
    )

    summary = match_summary(
        lost_item,
        found_items
    )

    print(
        "Lost item:",
        summary["lost_item_name"]
    )

    print(
        "Total possible matches:",
        summary["total_matches"]
    )


    # --------------------------------------------------------
    # PRIORITY QUEUE MATCH RANKING
    # --------------------------------------------------------

    print(
        "\n--- PRIORITY QUEUE MATCH RANKING ---"
    )

    for position, match in enumerate(
        summary["matches"],
        start=1
    ):

        print(

            f"{position}. "
            f"{match['item_name']} "
            f"-> "
            f"{match['score']}%"

        )


    # --------------------------------------------------------
    # BEST MATCH
    # --------------------------------------------------------

    print(
        "\n--- BEST MATCH ---"
    )

    best_match = summary["best_match"]

    if best_match:

        print(
            "Item:",
            best_match["item_name"]
        )

        print(
            "Location:",
            best_match["location"]
        )

        print(
            "Match Score:",
            best_match["score"],
            "%"
        )

    else:

        print(
            "No suitable match found."
        )


    print(
        "\n" + "=" * 75
    )

    print(
        "DSA MATCHING ENGINE TEST COMPLETED"
    )

    print(
        "=" * 75
    )


# ============================================================
# RUN DIRECTLY
# ============================================================

if __name__ == "__main__":

    test_matching_engine()