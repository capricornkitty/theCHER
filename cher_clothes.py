import sqlite3

# Function to insert a clothing item
def add_clothing_item(name, category, color, brand, material, image_path):
    conn = sqlite3.connect("closet_inventory.db")
    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO clothing (name, category, color, brand, material, image_path)
    VALUES (?, ?, ?, ?, ?, ?)
    """, (name, category, color, brand, material, image_path))

    conn.commit()
    conn.close()

    print(f"Added: {name} ({category}, {color}, {brand}, {material})")

# Example: Adding a sample clothing item
add_clothing_item("Nike T-Shirt", "Top", "Blue", "Nike", "Cotton", "path/to/image.jpg")
