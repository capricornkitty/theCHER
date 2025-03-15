import sqlite3

def get_all_clothing_items():
    """Retrieves all clothing items from the SQLite database."""
    conn = sqlite3.connect("closet_inventory.db")
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM clothing")
    rows = cursor.fetchall()

    conn.close()

    # Print the items
    print("Clothing Items in Database:")
    for row in rows:
        print(row)

# Run the function
get_all_clothing_items()
import sqlite3


