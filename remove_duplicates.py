import sqlite3

def remove_duplicates():
    """Removes exact duplicate clothing items from the SQLite database."""
    conn = sqlite3.connect("closet_inventory.db")
    cursor = conn.cursor()

    # Find and remove duplicate rows
    cursor.execute("""
    DELETE FROM clothing
    WHERE id NOT IN (
        SELECT MIN(id)
        FROM clothing
        GROUP BY name, category, color, brand, material
    )
    """)

    conn.commit()
    conn.close()
    print("✅ Duplicates removed successfully!")

# Run the function
remove_duplicates()
