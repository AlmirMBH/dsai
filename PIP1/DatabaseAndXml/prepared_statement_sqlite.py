import sqlite3 as sql

connection = sql.connect("random.database.db")
cursor = connection.cursor()

# Create the table
cursor.execute("""
CREATE TABLE IF NOT EXISTS client (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    address TEXT NOT NULL
)
""")

# Data to insert
data = [
    ("Almir", "Sarajevo"),
    ("John", "New York"),
    ("Jane", "London")
]

# Insert multiple rows
cursor.executemany("INSERT INTO client (name, address) VALUES (?, ?)", data)

connection.commit()
connection.close()
