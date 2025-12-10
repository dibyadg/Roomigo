from flask import Flask, render_template, request, abort
import oracledb

app = Flask(__name__)

# ----------------- ORACLE CONNECTION ----------------- #
def get_db_connection():
    return oracledb.connect(
        user="dibyadg",
        password="dibyadg",
        dsn="141.216.26.7/csep"
    )


# ----------------- HOME PAGE ----------------- #
@app.route("/")
def home():
    conn = None
    try:
        conn = get_db_connection()
        cur = conn.cursor()

        # Students shaped as:
        # (studentID, sname, email, password, gender, location)
        # If your real table is (studentID, sname, email, gender, location),
        # we just put '' as a fake password so the tuple length matches.
        cur.execute("""
            SELECT studentID,
                   sname,
                   email,
                   '' AS password,
                   gender,
                   location
            FROM Student
        """)
        students = cur.fetchall()

        # Listings shaped as:
        # (sname, address, rent, status, availableFrom, studentID)
        cur.execute("""
            SELECT s.sname,
                   l.address,
                   l.rent,
                   l.status,
                   l.availableFrom,
                   s.studentID
            FROM Listing l
            JOIN Student s ON l.studentID = s.studentID
        """)
        listings = cur.fetchall()

        cur.close()
        conn.close()
        conn = None

        # No messages passed, only students + listings
        return render_template(
            "home.html",
            students=students,
            listings=listings
        )

    except Exception as e:
        if conn:
            conn.close()
        return f"Error connecting to Oracle DB: {e}"


# ----------------- SEARCH LISTINGS (FROM HERO FORM) ----------------- #
@app.route("/search_listings", methods=["POST"])
def search_listings():
    location = request.form.get("location", "")
    min_rent = request.form.get("minRent")
    max_rent = request.form.get("maxRent")

    if not min_rent:
        min_rent = 0
    if not max_rent:
        max_rent = 9999999

    conn = None
    try:
        conn = get_db_connection()
        cur = conn.cursor()

        # Students again in same shape as above
        cur.execute("""
            SELECT studentID,
                   sname,
                   email,
                   '' AS password,
                   gender,
                   location
            FROM Student
        """)
        students = cur.fetchall()

        # Filtered listings, same shape:
        # (sname, address, rent, status, availableFrom, studentID)
        cur.execute("""
            SELECT s.sname,
                   l.address,
                   l.rent,
                   l.status,
                   l.availableFrom,
                   s.studentID
            FROM Listing l
            JOIN Student s ON l.studentID = s.studentID
            WHERE l.rent BETWEEN :minRent AND :maxRent
              AND (:location IS NULL OR :location = '' OR l.address LIKE '%' || :location || '%')
        """, {
            "minRent": min_rent,
            "maxRent": max_rent,
            "location": location
        })
        listings = cur.fetchall()

        cur.close()
        conn.close()
        conn = None

        return render_template(
            "home.html",
            students=students,
            listings=listings
        )

    except Exception as e:
        if conn:
            conn.close()
        return f"Error searching listings: {e}"


# ----------------- STUDENT PROFILE PAGE ----------------- #
@app.route("/student/<int:student_id>")
def student_profile(student_id):
    conn = None
    try:
        conn = get_db_connection()
        cur = conn.cursor()

        # Student shape must match profile.html comment:
        # (studentID, sname, email, password, gender, location)
        cur.execute("""
            SELECT studentID,
                   sname,
                   email,
                   '' AS password,
                   gender,
                   location
            FROM Student
            WHERE studentID = :sid
        """, {"sid": student_id})
        student = cur.fetchone()

        if not student:
            cur.close()
            conn.close()
            conn = None
            abort(404)

        # Profile: (age, lifestyle)
        cur.execute("""
            SELECT age, lifestyle
            FROM Profile
            WHERE studentID = :sid
        """, {"sid": student_id})
        profile = cur.fetchone()

        # Listings for this student:
        # (address, rent, status, availableFrom, description)
        cur.execute("""
            SELECT address, rent, status, availableFrom, description
            FROM Listing
            WHERE studentID = :sid
        """, {"sid": student_id})
        listings = cur.fetchall()

        cur.close()
        conn.close()
        conn = None

        return render_template(
            "login.html",
            student=student,
            profile=profile,
            listings=listings
        )

    except Exception as e:
        if conn:
            conn.close()
        return f"Error loading student profile: {e}"


# ----------------- MAIN ----------------- #
if __name__ == "__main__":
    app.run(debug=True)
