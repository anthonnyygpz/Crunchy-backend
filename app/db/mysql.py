import mysql.connector
import os
from dotenv import load_dotenv

load_dotenv()

mydb = mysql.connector.connect(
    host=os.getenv("HOST"),
    user=os.getenv("USER_MYSQL"),
    password=os.getenv("PASSWORD"),
    collation=os.getenv("COLLATION"),
    database=os.getenv("DATABASE_MYSQL"),
)
if mydb.is_connected():
    print("Connected to the MySQL Server")
else:
    print("Error in connection")
