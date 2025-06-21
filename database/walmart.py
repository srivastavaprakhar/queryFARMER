import sqlite3

# Connect to (or create) the database
conn = sqlite3.connect("database/trial1.db")
cursor = conn.cursor()

# Create the table with detailed fields
cursor.execute("""
CREATE TABLE IF NOT EXISTS walmart_items (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    category TEXT,
    aisle INTEGER,
    side TEXT,
    shelf TEXT,
    department TEXT,
    location_hint TEXT,
    keywords TEXT
)
""")

# Sample data to insert
items = [
    {
        "name": "Milk",
        "category": "Dairy",
        "aisle": 12,
        "side": "Left",
        "shelf": "Middle",
        "department": "Grocery",
        "location_hint": "Near the cold storage at the back-left of the store",
        "keywords": "milk,whole milk,2% milk,dairy milk"
    },
    {
        "name": "Toothpaste",
        "category": "Personal Care",
        "aisle": 5,
        "side": "Right",
        "shelf": "Top",
        "department": "Health & Beauty",
        "location_hint": "Next to toothbrushes and mouthwash, center-right side of store",
        "keywords": "toothpaste,oral care,colgate,sensodyne"
    },
    {
        "name": "Chicken Breast",
        "category": "Meat",
        "aisle": 14,
        "side": "Back Wall",
        "shelf": "Refrigerated Bin",
        "department": "Meat & Seafood",
        "location_hint": "Back wall, refrigerated section, near packaged fish",
        "keywords": "chicken,chicken breast,meat,poultry"
    },
    {
        "name": "Bananas",
        "category": "Fruits",
        "aisle": 3,
        "side": "Left",
        "shelf": "Produce Table",
        "department": "Produce",
        "location_hint": "Front-left produce section, near apples",
        "keywords": "banana,bananas,fruit"
    },
    {
        "name": "Shampoo",
        "category": "Personal Care",
        "aisle": 6,
        "side": "Left",
        "shelf": "Middle",
        "department": "Health & Beauty",
        "location_hint": "Middle-left section, next to conditioners",
        "keywords": "shampoo,hair care,dove,pantene"
    },
    {
        "name": "Batteries",
        "category": "Electronics",
        "aisle": 10,
        "side": "Endcap",
        "shelf": "Eye-level",
        "department": "Electronics",
        "location_hint": "Aisle end near checkout, eye-level shelf",
        "keywords": "battery,batteries,AA,AAA,energizer,duracell"
    }
]

# Insert data into the table
for item in items:
    cursor.execute("""
    INSERT INTO walmart_items (name, category, aisle, side, shelf, department, location_hint, keywords)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        item["name"],
        item["category"],
        item["aisle"],
        item["side"],
        item["shelf"],
        item["department"],
        item["location_hint"],
        item["keywords"]
    ))

# Save and close
conn.commit()
conn.close()

print("Data inserted into walmart_items table successfully.")
