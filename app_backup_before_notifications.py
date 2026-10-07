from flask import (
    Flask,
    render_template,
    request,
    redirect,
    url_for,
    flash,
    jsonify,
    session
)

from werkzeug.utils import secure_filename

import sqlite3
import os
from datetime import datetime

from dsa.matching_engine import (
    find_matches,
    search_items_linear,
    search_item_by_id
)


# ============================================================
# FLASK APPLICATION
# ============================================================

app = Flask(__name__)

app.secret_key = "smart-lost-found-nmiet-2026"


# ============================================================
# PROJECT DIRECTORIES
# ============================================================

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

DATABASE_DIR = os.path.join(
    BASE_DIR,
    "database"
)

UPLOAD_FOLDER = os.path.join(
    BASE_DIR,
    "static",
    "uploads"
)

DATABASE_PATH = os.path.join(
    DATABASE_DIR,
    "lost_found.db"
)

os.makedirs(DATABASE_DIR, exist_ok=True)
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

ALLOWED_EXTENSIONS = {
    "png",
    "jpg",
    "jpeg",
    "webp"
}


# ============================================================
# DATABASE CONNECTION
# ============================================================

def get_db():

    connection = sqlite3.connect(
        DATABASE_PATH,
        timeout=30
    )

    connection.row_factory = sqlite3.Row

    connection.execute(
        "PRAGMA busy_timeout = 30000"
    )

    return connection


# ============================================================
# FILE CHECK
# ============================================================

def allowed_file(filename):

    return (
        "." in filename
        and filename.rsplit(".", 1)[1].lower()
        in ALLOWED_EXTENSIONS
    )


# ============================================================
# DATABASE INITIALIZATION
# ============================================================

def initialize_database():

    connection = get_db()
    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            roll_no TEXT,
            division TEXT,
            department TEXT DEFAULT 'AI&DS',
            email TEXT UNIQUE,
            phone TEXT,
            location TEXT,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS items (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            item_type TEXT NOT NULL,
            item_name TEXT NOT NULL,
            category TEXT,
            description TEXT,
            item_date TEXT,
            item_time TEXT,
            location TEXT,
            specific_area TEXT,
            color TEXT,
            brand TEXT,
            unique_mark TEXT,
            image_filename TEXT,
            status TEXT DEFAULT 'Active',
            created_at TEXT DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(id)
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS claims (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            item_id INTEGER NOT NULL,
            claimant_name TEXT NOT NULL,
            claimant_roll_no TEXT,
            claimant_department TEXT,
            reason TEXT,
            status TEXT DEFAULT 'Pending',
            created_at TEXT DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (item_id) REFERENCES items(id)
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS matches (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            lost_item_id INTEGER NOT NULL,
            found_item_id INTEGER NOT NULL,
            score REAL,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (lost_item_id) REFERENCES items(id),
            FOREIGN KEY (found_item_id) REFERENCES items(id)
        )
    """)

    connection.commit()
    connection.close()


# ============================================================
# HOME
# ============================================================

@app.route("/")
def home():

    connection = get_db()

    lost_count = connection.execute("""
        SELECT COUNT(*)
        FROM items
        WHERE item_type = 'Lost'
        AND status = 'Active'
    """).fetchone()[0]

    found_count = connection.execute("""
        SELECT COUNT(*)
        FROM items
        WHERE item_type = 'Found'
        AND status = 'Active'
    """).fetchone()[0]

    claims_count = connection.execute("""
        SELECT COUNT(*)
        FROM claims
        WHERE status = 'Pending'
    """).fetchone()[0]

    connection.close()

    return render_template(
        "index.html",
        lost_count=lost_count,
        found_count=found_count,
        claims_count=claims_count,
        total_lost=lost_count,
        total_found=found_count,
        total_claims=claims_count,
        logged_in="user_id" in session,
        user_name=session.get("user_name")
    )


# ============================================================
# LOGIN
# ============================================================

@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        name = request.form.get(
            "name",
            ""
        ).strip()

        roll_no = request.form.get(
            "roll_no",
            ""
        ).strip()

        division = request.form.get(
            "division",
            ""
        ).strip()

        department = request.form.get(
            "department",
            "AI&DS"
        ).strip()

        email = request.form.get(
            "email",
            ""
        ).strip()

        phone = request.form.get(
            "phone",
            ""
        ).strip()

        location = request.form.get(
            "location",
            ""
        ).strip()

        if not name or not email:

            flash(
                "Name and email are required.",
                "danger"
            )

            return redirect(
                url_for("login")
            )

        connection = get_db()

        try:

            existing_user = connection.execute(
                """
                SELECT id
                FROM users
                WHERE email = ?
                """,
                (email,)
            ).fetchone()

            if existing_user:

                user_id = existing_user["id"]

                connection.execute(
                    """
                    UPDATE users
                    SET
                        name = ?,
                        roll_no = ?,
                        division = ?,
                        department = ?,
                        phone = ?,
                        location = ?
                    WHERE id = ?
                    """,
                    (
                        name,
                        roll_no,
                        division,
                        department,
                        phone,
                        location,
                        user_id
                    )
                )

            else:

                cursor = connection.execute(
                    """
                    INSERT INTO users
                    (
                        name,
                        roll_no,
                        division,
                        department,
                        email,
                        phone,
                        location
                    )
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                    """,
                    (
                        name,
                        roll_no,
                        division,
                        department,
                        email,
                        phone,
                        location
                    )
                )

                user_id = cursor.lastrowid

            connection.commit()

        except sqlite3.OperationalError:

            connection.rollback()
            connection.close()

            flash(
                "Database is busy. Please try Login again.",
                "danger"
            )

            return redirect(
                url_for("login")
            )

        finally:

            try:
                connection.close()
            except:
                pass

        session["user_id"] = user_id
        session["user_name"] = name
        session["roll_no"] = roll_no
        session["department"] = department
        session["email"] = email

        flash(
            "Login successful.",
            "success"
        )

        return redirect(
            url_for("home")
        )

    return render_template("login.html")


# ============================================================
# LOGOUT
# ============================================================

@app.route("/logout")
def logout():

    session.clear()

    flash(
        "You have been logged out.",
        "success"
    )

    return redirect(
        url_for("home")
    )


# ============================================================
# IMAGE UPLOAD
# ============================================================

def save_uploaded_image(file):

    if not file or file.filename == "":
        return None

    if not allowed_file(file.filename):
        return None

    filename = secure_filename(
        file.filename
    )

    name, extension = os.path.splitext(
        filename
    )

    timestamp = datetime.now().strftime(
        "%Y%m%d%H%M%S%f"
    )

    filename = (
        f"{name}_{timestamp}{extension}"
    )

    file.save(
        os.path.join(
            app.config["UPLOAD_FOLDER"],
            filename
        )
    )

    return filename


# ============================================================
# REPORT LOST
# ============================================================

@app.route(
    "/report-lost",
    methods=["GET", "POST"]
)
def report_lost():

    if request.method == "POST":

        image_filename = save_uploaded_image(
            request.files.get("image")
        )

        connection = get_db()

        connection.execute(
            """
            INSERT INTO items
            (
                user_id,
                item_type,
                item_name,
                category,
                description,
                item_date,
                item_time,
                location,
                specific_area,
                color,
                brand,
                unique_mark,
                image_filename,
                status,
                created_at
            )
            VALUES
            (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                session.get("user_id"),
                "Lost",
                request.form.get(
                    "item_name",
                    ""
                ).strip(),
                request.form.get(
                    "category",
                    ""
                ).strip(),
                request.form.get(
                    "description",
                    ""
                ).strip(),
                request.form.get(
                    "item_date",
                    ""
                ).strip(),
                request.form.get(
                    "item_time",
                    ""
                ).strip(),
                request.form.get(
                    "location",
                    ""
                ).strip(),
                request.form.get(
                    "specific_area",
                    ""
                ).strip(),
                request.form.get(
                    "color",
                    ""
                ).strip(),
                request.form.get(
                    "brand",
                    ""
                ).strip(),
                request.form.get(
                    "unique_mark",
                    ""
                ).strip(),
                image_filename,
                "Active",
                datetime.now().isoformat()
            )
        )

        connection.commit()
        connection.close()

        flash(
            "Lost item reported successfully.",
            "success"
        )

        return redirect(
            url_for("home")
        )

    return render_template(
        "report_item.html",
        item_type="Lost"
    )
# ============================================================
# REPORT FOUND
# ============================================================

@app.route(
    "/report-found",
    methods=["GET", "POST"]
)
def report_found():

    if request.method == "POST":

        image_filename = save_uploaded_image(
            request.files.get("image")
        )

        connection = get_db()

        connection.execute(
            """
            INSERT INTO items
            (
                user_id,
                item_type,
                item_name,
                category,
                description,
                item_date,
                item_time,
                location,
                specific_area,
                color,
                brand,
                unique_mark,
                image_filename,
                status,
                created_at
            )
            VALUES
            (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                session.get("user_id"),
                "Found",
                request.form.get(
                    "item_name",
                    ""
                ).strip(),
                request.form.get(
                    "category",
                    ""
                ).strip(),
                request.form.get(
                    "description",
                    ""
                ).strip(),
                request.form.get(
                    "item_date",
                    ""
                ).strip(),
                request.form.get(
                    "item_time",
                    ""
                ).strip(),
                request.form.get(
                    "location",
                    ""
                ).strip(),
                request.form.get(
                    "specific_area",
                    ""
                ).strip(),
                request.form.get(
                    "color",
                    ""
                ).strip(),
                request.form.get(
                    "brand",
                    ""
                ).strip(),
                request.form.get(
                    "unique_mark",
                    ""
                ).strip(),
                image_filename,
                "Active",
                datetime.now().isoformat()
            )
        )

        connection.commit()
        connection.close()

        flash(
            "Found item reported successfully.",
            "success"
        )

        return redirect(
            url_for("home")
        )

    return render_template(
        "report_item.html",
        item_type="Found"
    )


# ============================================================
# SEARCH
# ============================================================

@app.route("/search")
def search_items():

    keyword = request.args.get(
        "q",
        ""
    ).strip()

    connection = get_db()

    database_items = connection.execute(
        """
        SELECT *
        FROM items
        WHERE status = 'Active'
        ORDER BY id DESC
        """
    ).fetchall()

    connection.close()

    items = [
        dict(item)
        for item in database_items
    ]

    if keyword:

        items = search_items_linear(
            items,
            keyword
        )

    return render_template(
        "search.html",
        items=items,
        keyword=keyword
    )


# ============================================================
# ITEM DETAILS
# ============================================================

@app.route("/item/<int:item_id>")
def view_item(item_id):

    connection = get_db()

    item = connection.execute(
        """
        SELECT *
        FROM items
        WHERE id = ?
        """,
        (item_id,)
    ).fetchone()

    connection.close()

    if item is None:
        return "Item not found", 404

    return render_template(
        "item_details.html",
        item=item
    )


# ============================================================
# CLAIM
# ============================================================

@app.route(
    "/claim/<int:item_id>",
    methods=["GET", "POST"]
)
def claim_item(item_id):

    connection = get_db()

    item = connection.execute(
        """
        SELECT *
        FROM items
        WHERE id = ?
        """,
        (item_id,)
    ).fetchone()

    if item is None:

        connection.close()

        return "Item not found", 404

    if request.method == "POST":

        claimant_name = request.form.get(
            "claimant_name",
            ""
        ).strip()

        claimant_roll_no = request.form.get(
            "claimant_roll_no",
            ""
        ).strip()

        claimant_department = request.form.get(
            "claimant_department",
            ""
        ).strip()

        reason = request.form.get(
            "reason",
            ""
        ).strip()

        connection.execute(
            """
            INSERT INTO claims
            (
                item_id,
                claimant_name,
                claimant_roll_no,
                claimant_department,
                reason,
                status,
                created_at
            )
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
            (
                item_id,
                claimant_name,
                claimant_roll_no,
                claimant_department,
                reason,
                "Pending",
                datetime.now().isoformat()
            )
        )

        connection.commit()
        connection.close()

        return render_template(
            "claim_success.html",
            item=item,
            claimant_name=claimant_name
        )

    connection.close()

    return render_template(
        "claim.html",
        item=item
    )


# ============================================================
# SMART MATCHING
# ============================================================

@app.route("/matches/<int:item_id>")
def matches_page(item_id):

    connection = get_db()

    source_item = connection.execute(
        """
        SELECT *
        FROM items
        WHERE id = ?
        """,
        (item_id,)
    ).fetchone()

    if source_item is None:

        connection.close()

        return "Item not found", 404

    opposite_type = (
        "Found"
        if source_item["item_type"] == "Lost"
        else "Lost"
    )

    database_items = connection.execute(
        """
        SELECT *
        FROM items
        WHERE item_type = ?
        AND id != ?
        AND status = 'Active'
        """,
        (
            opposite_type,
            item_id
        )
    ).fetchall()

    connection.close()

    matches = find_matches(
        dict(source_item),
        [
            dict(item)
            for item in database_items
        ],
        minimum_score=20
    )

    return render_template(
        "matches.html",
        item=source_item,
        matches=matches
    )


# ============================================================
# API - MATCHES
# ============================================================

@app.route(
    "/api/matches/<int:item_id>"
)
def api_matches(item_id):

    connection = get_db()

    source_item = connection.execute(
        """
        SELECT *
        FROM items
        WHERE id = ?
        """,
        (item_id,)
    ).fetchone()

    if source_item is None:

        connection.close()

        return jsonify({
            "error": "Item not found"
        }), 404

    opposite_type = (
        "Found"
        if source_item["item_type"] == "Lost"
        else "Lost"
    )

    database_items = connection.execute(
        """
        SELECT *
        FROM items
        WHERE item_type = ?
        AND id != ?
        AND status = 'Active'
        """,
        (
            opposite_type,
            item_id
        )
    ).fetchall()

    connection.close()

    matches = find_matches(
        dict(source_item),
        [
            dict(item)
            for item in database_items
        ],
        minimum_score=20
    )

    return jsonify({
        "source_item_id": item_id,
        "matching_algorithm":
            "DSA Smart Matching Engine",
        "total_matches": len(matches),
        "matches": matches
    })


# ============================================================
# API - ITEM LOOKUP
# ============================================================

@app.route(
    "/api/items/<int:item_id>"
)
def api_item_lookup(item_id):

    connection = get_db()

    database_items = connection.execute(
        """
        SELECT *
        FROM items
        WHERE status = 'Active'
        """
    ).fetchall()

    connection.close()

    items = [
        dict(item)
        for item in database_items
    ]

    item = search_item_by_id(
        items,
        item_id
    )

    if item is None:

        return jsonify({
            "error": "Item not found"
        }), 404

    return jsonify({
        "lookup_method": "Hash Table",
        "average_complexity": "O(1)",
        "item": item
    })
# ============================================================
# API - ALL ITEMS
# ============================================================

@app.route("/api/items")
def api_all_items():

    connection = get_db()

    database_items = connection.execute(
        """
        SELECT *
        FROM items
        ORDER BY id DESC
        """
    ).fetchall()

    connection.close()

    return jsonify([
        dict(item)
        for item in database_items
    ])


# ============================================================
# API - STATISTICS
# ============================================================

@app.route("/api/statistics")
def api_statistics():

    connection = get_db()

    total_items = connection.execute(
        """
        SELECT COUNT(*)
        FROM items
        """
    ).fetchone()[0]

    lost_items = connection.execute(
        """
        SELECT COUNT(*)
        FROM items
        WHERE item_type = 'Lost'
        """
    ).fetchone()[0]

    found_items = connection.execute(
        """
        SELECT COUNT(*)
        FROM items
        WHERE item_type = 'Found'
        """
    ).fetchone()[0]

    active_items = connection.execute(
        """
        SELECT COUNT(*)
        FROM items
        WHERE status = 'Active'
        """
    ).fetchone()[0]

    total_claims = connection.execute(
        """
        SELECT COUNT(*)
        FROM claims
        """
    ).fetchone()[0]

    pending_claims = connection.execute(
        """
        SELECT COUNT(*)
        FROM claims
        WHERE status = 'Pending'
        """
    ).fetchone()[0]

    connection.close()

    return jsonify({
        "total_items": total_items,
        "lost_items": lost_items,
        "found_items": found_items,
        "active_items": active_items,
        "total_claims": total_claims,
        "pending_claims": pending_claims
    })


# ============================================================
# PROFILE
# ============================================================

@app.route("/profile")
def profile():

    if "user_id" not in session:
        return redirect(
            url_for("login")
        )

    connection = get_db()

    user = connection.execute(
        """
        SELECT *
        FROM users
        WHERE id = ?
        """,
        (session["user_id"],)
    ).fetchone()

    connection.close()

    if user is None:
        return redirect(
            url_for("login")
        )

    return render_template(
        "profile.html",
        user=user
    )


# ============================================================
# MY REPORTS
# ============================================================

@app.route("/my-reports")
def my_reports():

    if "user_id" not in session:
        return redirect(
            url_for("login")
        )

    connection = get_db()

    items = connection.execute(
        """
        SELECT *
        FROM items
        WHERE user_id = ?
        ORDER BY id DESC
        """,
        (session["user_id"],)
    ).fetchall()

    connection.close()

    return render_template(
        "my_reports.html",
        items=items
    )


# ============================================================
# ADMIN DASHBOARD
# ============================================================

@app.route("/admin")
def admin():

    connection = get_db()

    total_items = connection.execute(
        """
        SELECT COUNT(*)
        FROM items
        """
    ).fetchone()[0]

    lost_items = connection.execute(
        """
        SELECT COUNT(*)
        FROM items
        WHERE item_type = 'Lost'
        """
    ).fetchone()[0]

    found_items = connection.execute(
        """
        SELECT COUNT(*)
        FROM items
        WHERE item_type = 'Found'
        """
    ).fetchone()[0]

    total_users = connection.execute(
        """
        SELECT COUNT(*)
        FROM users
        """
    ).fetchone()[0]

    total_claims = connection.execute(
        """
        SELECT COUNT(*)
        FROM claims
        """
    ).fetchone()[0]

    pending_claims = connection.execute(
        """
        SELECT COUNT(*)
        FROM claims
        WHERE status = 'Pending'
        """
    ).fetchone()[0]

    recent_items = connection.execute(
        """
        SELECT *
        FROM items
        ORDER BY id DESC
        LIMIT 10
        """
    ).fetchall()

    recent_claims = connection.execute(
        """
        SELECT claims.*, items.item_name
        FROM claims
        JOIN items
        ON claims.item_id = items.id
        ORDER BY claims.id DESC
        LIMIT 10
        """
    ).fetchall()

    connection.close()

    return render_template(
        "admin.html",
        total_items=total_items,
        lost_items=lost_items,
        found_items=found_items,
        total_users=total_users,
        total_claims=total_claims,
        pending_claims=pending_claims,
        recent_items=recent_items,
        recent_claims=recent_claims
    )
# ============================================================
# ADMIN CLAIM VERIFICATION
# ============================================================

@app.route("/api/admin/claims")
def admin_claims():

    connection = get_db()

    claims = connection.execute(
        """
        SELECT
            claims.id,
            claims.item_id,
            claims.claimant_name,
            claims.claimant_roll_no,
            claims.claimant_department,
            claims.reason,
            claims.status,
            claims.created_at,
            items.item_name,
            items.category,
            items.location
        FROM claims
        JOIN items
        ON claims.item_id = items.id
        ORDER BY claims.id DESC
        """
    ).fetchall()

    connection.close()

    return jsonify([
        dict(claim)
        for claim in claims
    ])


@app.route(
    "/admin/claim/<int:claim_id>/approve",
    methods=["POST"]
)
def approve_claim(claim_id):

    connection = get_db()

    claim = connection.execute(
        """
        SELECT item_id
        FROM claims
        WHERE id = ?
        """,
        (claim_id,)
    ).fetchone()

    if claim is None:
        connection.close()
        return jsonify({
            "success": False,
            "message": "Claim not found"
        }), 404

    connection.execute(
        """
        UPDATE claims
        SET status = 'Approved'
        WHERE id = ?
        """,
        (claim_id,)
    )

    connection.execute(
        """
        UPDATE items
        SET status = 'Returned'
        WHERE id = ?
        """,
        (claim["item_id"],)
    )

    connection.commit()
    connection.close()

    return jsonify({
        "success": True,
        "message": "Claim approved successfully"
    })


@app.route(
    "/admin/claim/<int:claim_id>/reject",
    methods=["POST"]
)
def reject_claim(claim_id):

    connection = get_db()

    claim = connection.execute(
        """
        SELECT id
        FROM claims
        WHERE id = ?
        """,
        (claim_id,)
    ).fetchone()

    if claim is None:
        connection.close()
        return jsonify({
            "success": False,
            "message": "Claim not found"
        }), 404

    connection.execute(
        """
        UPDATE claims
        SET status = 'Rejected'
        WHERE id = ?
        """,
        (claim_id,)
    )

    connection.commit()
    connection.close()

    return jsonify({
        "success": True,
        "message": "Claim rejected successfully"
    })

# ============================================================
# ERROR HANDLERS
# ============================================================

@app.errorhandler(404)
def page_not_found(error):

    return render_template(
        "404.html"
    ), 404


@app.errorhandler(500)
def internal_server_error(error):

    return render_template(
        "500.html"
    ), 500


# ============================================================
# DATABASE INITIALIZATION
# ============================================================

initialize_database()


# ============================================================
# RUN APPLICATION
# ============================================================

if __name__ == "__main__":

    app.run(
        debug=False,
        host="127.0.0.1",
        port=5000
    )