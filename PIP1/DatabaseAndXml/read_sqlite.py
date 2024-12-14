import sqlite3 as sql

connection = sql.connect("random.database.db")
cursor = connection.cursor()

clients = cursor.execute("SELECT * FROM client")
columns = [column[0] for column in cursor.description]  # Extract column names

clients_dict = [dict(zip(columns, client)) for client in clients]  # Convert to list of dictionaries

print("\nDICTIONARY")
for client in clients_dict:
    print(client)


print("\nTABLE DATA")
clients = cursor.execute("SELECT * FROM client")
print(" | " . join(columns))

for client in clients:
    print(" | ".join(str(value) for value in client))


print("\nFETCH")
cursor.execute("SELECT * FROM client")
results = cursor.fetchall()

for client in results:
    print(client)
    # print(" | ".join(str(value) for value in client))


print("\nFETCH SINGLE")
query = "SELECT * FROM client WHERE id = ?"
params = (8,)
results = cursor.execute(query, params)

for client in results:
    print(client)


print("\nFETCH MULTIPLE")
query = "SELECT * FROM client WHERE id BETWEEN ? AND ?"
params = (6,8)
results = cursor.execute(query, params)

for client in results:
    print(client)