print("✅ Smart Closet Manager is running!")

import sqlite3
import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
import requests
from io import BytesIO

# Create main UI window
root = tk.Tk()
root.title("Smart Closet Manager")
root.geometry("600x600")

# Function to fetch clothing items from the database with optional filters
def fetch_clothing_items(filter_query=""):
    conn = sqlite3.connect("closet_inventory.db")
    cursor = conn.cursor()
    
    if filter_query:
        cursor.execute("""
        SELECT id, name, category, color, brand, material, image_path 
        FROM clothing 
        WHERE name LIKE ? OR category LIKE ? OR color LIKE ? OR brand LIKE ?
        """, (f"%{filter_query}%", f"%{filter_query}%", f"%{filter_query}%", f"%{filter_query}%"))
    else:
        cursor.execute("SELECT id, name, category, color, brand, material, image_path FROM clothing")
    
    rows = cursor.fetchall()
    conn.close()
    return rows

# Function to update the listbox with clothing items
def update_clothing_list():
    filter_text = search_entry.get().strip()
    clothing_list.delete(0, tk.END)
    items = fetch_clothing_items(filter_text)
    for item in items:
        clothing_list.insert(tk.END, f"{item[1]} - {item[2]} ({item[3]})")

# Function to show item details and load images
def show_item_details(event):
    try:
        selected_index = clothing_list.curselection()[0]
        items = fetch_clothing_items(search_entry.get().strip())
        item = items[selected_index]

        details_text.set(f"Name: {item[1]}\nCategory: {item[2]}\nColor: {item[3]}\nBrand: {item[4]}\nMaterial: {item[5]}")

        # Load and display image if available
        image_url = item[6]
        if image_url and image_url.startswith("http"):
            try:
                response = requests.get(image_url)
                response.raise_for_status()  # Check if the URL is accessible
                img_data = BytesIO(response.content)
                img = Image.open(img_data)
                img = img.resize((150, 150), Image.LANCZOS)  # Use LANCZOS instead of ANTIALIAS (better quality)
                img_tk = ImageTk.PhotoImage(img)
                clothing_image_label.config(image=img_tk)
                clothing_image_label.image = img_tk
            except Exception as e:
                print(f"Error loading image: {e}")  # Print error for debugging
                clothing_image_label.config(text="Image Not Found", image="")
        else:
            clothing_image_label.config(text="No Image Provided", image="")
    except IndexError:
        pass


# Function to delete a selected item and refresh the list
def delete_selected_item():
    print("🛠 DEBUG: Delete button was clicked!")  # Debugging print

    try:
        selected_index = clothing_list.curselection()[0]
        print(f"🛠 DEBUG: Selected index = {selected_index}")  # Debugging print
        
        items = fetch_clothing_items(search_entry.get().strip())
        if not items:
            print("❌ ERROR: No items found in the database!")
            return

        item_id = items[selected_index][0]
        print(f"🛠 DEBUG: Selected Item ID = {item_id}")  # Debugging print

        conn = sqlite3.connect("closet_inventory.db")
        cursor = conn.cursor()

        # Debugging: Print all items in the database
        cursor.execute("SELECT * FROM clothing;")
        all_items = cursor.fetchall()
        print(f"📋 DEBUG: Current items in database: {all_items}")

        # Check if the selected item exists before deleting
        cursor.execute("SELECT * FROM clothing WHERE id=?", (item_id,))
        item_check = cursor.fetchone()
        if item_check:
            print(f"🗑️ DEBUG: Deleting item: {item_check}")  # Debugging output

            # Delete the item
            cursor.execute("DELETE FROM clothing WHERE id=?", (item_id,))
            conn.commit()

            # Verify deletion
            cursor.execute("SELECT * FROM clothing WHERE id=?", (item_id,))
            item_check_after = cursor.fetchone()

            if item_check_after:
                print("❌ ERROR: Item was NOT deleted!")  # If item is still there, deletion failed
            else:
                print("✅ SUCCESS: Item deleted successfully!")  # Item is gone

        conn.close()

        # Refresh the list properly
       

   
        # Refresh the list properly
        clothing_list.delete(0, tk.END)  # Clear listbox
        update_clothing_list()  # Reload all items
        details_text.set("Item deleted!")  # Update message
        clothing_image_label.config(image="", text="No Image")  # Clear image
    except IndexError:
        print("❌ ERROR: No item was selected to delete.")  # Debug print
        messagebox.showerror("Error", "Please select an item to delete.")


        # Refresh the list properly
        clothing_list.delete(0, tk.END)  # Clear listbox
        update_clothing_list()  # Reload all items
        details_text.set("Item deleted!")  # Update message
        clothing_image_label.config(image="", text="No Image")  # Clear image
    except IndexError:
        messagebox.showerror("Error", "Please select an item to delete.")


        # Refresh the list properly
        search_entry.delete(0, tk.END)  # Clear search bar
        update_clothing_list()  # Reload all items

        details_text.set("Item deleted!")  # Update details text
        clothing_image_label.config(image="", text="No Image")  # Remove image
    except IndexError:
        messagebox.showerror("Error", "Please select an item to delete.")



# Function to add a new clothing item
def add_new_clothing():
    def save_new_item():
        name = name_entry.get()
        category = category_entry.get()
        color = color_entry.get()
        brand = brand_entry.get()
        material = material_entry.get()
        image_path = image_path_entry.get()

        if not name or not category or not color:
            messagebox.showerror("Error", "Please fill in all required fields (Name, Category, Color).")
            return

        conn = sqlite3.connect("closet_inventory.db")
        cursor = conn.cursor()
        cursor.execute("""
        INSERT INTO clothing (name, category, color, brand, material, image_path)
        VALUES (?, ?, ?, ?, ?, ?)
        """, (name, category, color, brand, material, image_path))
        conn.commit()
        conn.close()

        messagebox.showinfo("Success", "New clothing item added!")
        add_window.destroy()
        update_clothing_list()

    add_window = tk.Toplevel(root)
    add_window.title("Add New Clothing Item")
    add_window.geometry("400x300")

    tk.Label(add_window, text="Name:").grid(row=0, column=0, padx=10, pady=5)
    name_entry = tk.Entry(add_window)
    name_entry.grid(row=0, column=1, padx=10, pady=5)

    tk.Label(add_window, text="Category:").grid(row=1, column=0, padx=10, pady=5)
    category_entry = tk.Entry(add_window)
    category_entry.grid(row=1, column=1, padx=10, pady=5)

    tk.Label(add_window, text="Color:").grid(row=2, column=0, padx=10, pady=5)
    color_entry = tk.Entry(add_window)
    color_entry.grid(row=2, column=1, padx=10, pady=5)

    tk.Label(add_window, text="Brand:").grid(row=3, column=0, padx=10, pady=5)
    brand_entry = tk.Entry(add_window)
    brand_entry.grid(row=3, column=1, padx=10, pady=5)

    tk.Label(add_window, text="Material:").grid(row=4, column=0, padx=10, pady=5)
    material_entry = tk.Entry(add_window)
    material_entry.grid(row=4, column=1, padx=10, pady=5)

    tk.Label(add_window, text="Image URL:").grid(row=5, column=0, padx=10, pady=5)
    image_path_entry = tk.Entry(add_window)
    image_path_entry.grid(row=5, column=1, padx=10, pady=5)

    save_button = ttk.Button(add_window, text="Save", command=save_new_item)
    save_button.grid(row=6, column=0, columnspan=2, pady=10)

# UI Elements
frame = tk.Frame(root)
frame.pack(pady=10)

search_label = tk.Label(root, text="Search:")
search_label.pack()
search_entry = tk.Entry(root, width=40)
search_entry.pack()
search_button = ttk.Button(root, text="Search", command=update_clothing_list)
search_button.pack()

clothing_list = tk.Listbox(frame, width=50, height=10)
clothing_list.pack(side=tk.LEFT, padx=10)
clothing_list.bind("<<ListboxSelect>>", show_item_details)

scrollbar = tk.Scrollbar(frame, orient=tk.VERTICAL, command=clothing_list.yview)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
clothing_list.config(yscrollcommand=scrollbar.set)

details_text = tk.StringVar()
details_label = tk.Label(root, textvariable=details_text, justify=tk.LEFT, padx=10)
details_label.pack()

clothing_image_label = tk.Label(root)
clothing_image_label.pack(pady=10)

delete_button = ttk.Button(root, text="Delete Selected Item", command=delete_selected_item)
delete_button.pack(pady=5)

add_button = ttk.Button(root, text="Add New Clothing Item", command=add_new_clothing)
add_button.pack(pady=5)

# Initialize List
update_clothing_list()

# Run the UI
root.mainloop()
