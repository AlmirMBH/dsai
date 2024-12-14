import sqlite3 as sql

connection = sql.connect("random.database.db")
cursor = connection.cursor()

# Create the client table if it doesn't exist
cursor.execute("""
CREATE TABLE IF NOT EXISTS client (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    address TEXT NOT NULL
)
""")

# Insert data into the client table
cursor.execute("INSERT INTO client (name, address) VALUES ('Almir', 'Sarajevo')")

connection.commit()
connection.close()

print("Data inserted successfully.")
