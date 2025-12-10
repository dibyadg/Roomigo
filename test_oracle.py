import oracledb

try:
    conn = oracledb.connect(
        user="bindush",
        password="bindush",
        dsn="141.216.26.7/csep"  # Use the working DSN
    ) 
    cur = conn.cursor()
    cur.execute("SELECT * FROM Student")
    for row in cur:
        print(row)
    cur.close()
    conn.close()
    print("Oracle connection successful!")
except Exception as e:
    print("Oracle connection failed:", e)
