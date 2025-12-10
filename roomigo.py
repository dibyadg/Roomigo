import getpass
import oracledb

def connect_db():
    username = input("Enter Oracle username: ")
    password = getpass.getpass("Enter Oracle password: ")
    dsn = "oracle.csep.umflint.edu:1521/csep"  # replace if your DSN is different

    try:
        connection = oracledb.connect(user=username, password=password, dsn=dsn)
        print("Successfully connected to Oracle Database")
        return connection
    except Exception as e:
        print("Connection failed:", e)
        return None
