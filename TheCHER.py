import sqlite3

# Create a connection to the SQLite database (or create it if it doesn't exist)
conn = sqlite3.connect("closet_inventory.db")
cursor = conn.cursor()

# Create a table for clothing items
cursor.execute("""
CREATE TABLE IF NOT EXISTS clothing (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    category TEXT NOT NULL,
    color TEXT NOT NULL,
    brand TEXT,
    material TEXT,
    image_path TEXT
)
""")

# Commit and close connection
conn.commit()
conn.close()

# Confirm creation
"SQLite database and 'clothing' table successfully created!"
