from flask import Flask, render_template
import oracledb

app = Flask(__name__)

def get_db_connection():
    return oracledb.connect(
        user="dibyadg",
        password="dibyadg",
        dsn="141.216.26.7/csep"  # Use your working DSN
    )

@app.route("/")
def home():
    try:
        conn = get_db_connection()
        cur = conn.cursor()

        # Fetch students
        cur.execute("SELECT * FROM Student")
        students = cur.fetchall()

        # Fetch listings joined with students
        cur.execute("""
            SELECT s.sname, l.address, l.rent, l.status, l.availableFrom
            FROM Listing l
            JOIN Student s ON l.studentID = s.studentID
        """)
        listings = cur.fetchall()

        # Fetch profiles joined with students
        cur.execute("""
            SELECT s.sname, p.age, p.lifestyle
            FROM Profile p
            JOIN Student s ON p.studentID = s.studentID
        """)
        profiles = cur.fetchall()

        # Fetch latest 5 messages with sender and receiver names
        cur.execute("""
            SELECT s1.sname AS sender, s2.sname AS receiver, m.content, m.sentDate
            FROM Message m
            JOIN Student s1 ON m.senderID = s1.studentID
            JOIN Student s2 ON m.receiverID = s2.studentID
            ORDER BY m.sentDate DESC
            FETCH FIRST 5 ROWS ONLY
        """)
        messages = cur.fetchall()

        cur.close()
        conn.close()

        # Pass all tables to the template
        return render_template(
            "home.html",
            students=students,
            listings=listings,
            profiles=profiles,
            messages=messages
        )

    except Exception as e:
        return f"Error connecting to Oracle DB: {e}"

if __name__ == "__main__":
    app.run(debug=True)
