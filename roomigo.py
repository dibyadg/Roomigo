from flask import Flask, render_template
import oracledb

app = Flask(__name__)

# ORACLE DB CONNECTION -----------------------------
def get_db_connection():
    connection = oracledb.connect(
        user="bindush",
        password="bindush",
        dsn="141.216.26.7/csep"  
    )
    return connection
# --------------------------------------------------

@app.route("/")
@app.route("/")
def home():
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("SELECT * FROM Student")
        students = cur.fetchall()
        cur.close()
        conn.close()
        return f"Connection Successful! Students: {students}"
    except Exception as e:
        return f"Error connecting to Oracle DB: {e}"


if __name__ == "__main__":
    app.run(debug=True)
