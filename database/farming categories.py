import sqlite3

# Connect to SQLite database
conn = sqlite3.connect("database/trial1.db")
cursor = conn.cursor()

# Create farming_categories table (replacing departments)
cursor.execute('''
CREATE TABLE IF NOT EXISTS farming_categories (
    category_id INTEGER PRIMARY KEY AUTOINCREMENT,
    category_name TEXT UNIQUE NOT NULL,
    description TEXT
)
''')

# Create crops table (replacing faculty)
cursor.execute('''
CREATE TABLE IF NOT EXISTS crops (
    crop_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    category_id INTEGER,
    season TEXT NOT NULL,
    growth_period_days INTEGER,
    water_requirements TEXT,
    soil_type TEXT,
    FOREIGN KEY (category_id) REFERENCES farming_categories(category_id)
)
''')

# Classes
class FarmingCategory:
    def __init__(self, name, description=""):
        self.name = name
        self.description = description

    def save(self, cursor):
        cursor.execute("INSERT OR IGNORE INTO farming_categories (category_name, description) VALUES (?, ?)", 
                      (self.name, self.description))

    def get_id(self, cursor):
        cursor.execute("SELECT category_id FROM farming_categories WHERE category_name = ?", (self.name,))
        return cursor.fetchone()[0]

class Crop:
    def __init__(self, name, category_id, season, growth_period_days, water_requirements, soil_type):
        self.name = name
        self.category_id = category_id
        self.season = season
        self.growth_period_days = growth_period_days
        self.water_requirements = water_requirements
        self.soil_type = soil_type

    def save(self, cursor):
        cursor.execute('''
            INSERT INTO crops (name, category_id, season, growth_period_days, water_requirements, soil_type)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (self.name, self.category_id, self.season, self.growth_period_days, 
              self.water_requirements, self.soil_type))
        
# Insert farming categories
farming_categories = [
    ("Grains & Cereals", "Basic food crops like rice, wheat, corn"),
    ("Vegetables", "Leafy greens, root vegetables, and other vegetables"),
    ("Fruits", "Tree fruits, berries, and other fruit crops"),
    ("Pulses & Legumes", "Protein-rich crops like beans, lentils, peas"),
    ("Cash Crops", "Commercial crops like cotton, sugarcane, tobacco"),
    ("Medicinal Plants", "Herbs and plants with medicinal properties")
]

cursor.executemany("INSERT OR IGNORE INTO farming_categories (category_name, description) VALUES (?, ?)", farming_categories)

# Data for crops
crops_data = [
    # Grains & Cereals
    ("Rice", "Grains & Cereals", "Kharif", 120, "High", "Clay loam"),
    ("Wheat", "Grains & Cereals", "Rabi", 150, "Medium", "Loamy soil"),
    ("Maize", "Grains & Cereals", "Kharif", 90, "High", "Well-drained soil"),
    ("Barley", "Grains & Cereals", "Rabi", 120, "Low", "Sandy loam"),
    
    # Vegetables
    ("Tomato", "Vegetables", "All seasons", 75, "Medium", "Sandy loam"),
    ("Potato", "Vegetables", "Rabi", 100, "Medium", "Loamy soil"),
    ("Onion", "Vegetables", "Rabi", 120, "Low", "Sandy soil"),
    ("Carrot", "Vegetables", "Rabi", 80, "Medium", "Sandy loam"),
    ("Spinach", "Vegetables", "Winter", 45, "High", "Rich loam"),
    ("Cabbage", "Vegetables", "Winter", 90, "High", "Loamy soil"),
    
    # Fruits
    ("Mango", "Fruits", "Summer", 1095, "Medium", "Deep loamy soil"),
    ("Banana", "Fruits", "All seasons", 365, "High", "Rich loam"),
    ("Apple", "Fruits", "Autumn", 1825, "Medium", "Well-drained soil"),
    ("Orange", "Fruits", "Winter", 1095, "Medium", "Sandy loam"),
    ("Grapes", "Fruits", "Summer", 180, "Medium", "Clay loam"),
    
    # Pulses & Legumes
    ("Chickpea", "Pulses & Legumes", "Rabi", 120, "Low", "Well-drained soil"),
    ("Lentil", "Pulses & Legumes", "Rabi", 110, "Low", "Loamy soil"),
    ("Black Gram", "Pulses & Legumes", "Kharif", 90, "Medium", "Clay loam"),
    ("Green Gram", "Pulses & Legumes", "Kharif", 75, "Medium", "Sandy loam"),
    
    # Cash Crops
    ("Cotton", "Cash Crops", "Kharif", 180, "Medium", "Black soil"),
    ("Sugarcane", "Cash Crops", "All seasons", 365, "High", "Heavy soil"),
    ("Tobacco", "Cash Crops", "Rabi", 120, "Medium", "Sandy loam"),
    ("Jute", "Cash Crops", "Kharif", 120, "High", "Clay loam"),
    
    # Medicinal Plants
    ("Aloe Vera", "Medicinal Plants", "All seasons", 365, "Low", "Sandy soil"),
    ("Tulsi", "Medicinal Plants", "All seasons", 90, "Medium", "Well-drained soil"),
    ("Neem", "Medicinal Plants", "All seasons", 1825, "Low", "Sandy loam"),
    ("Turmeric", "Medicinal Plants", "Kharif", 270, "Medium", "Loamy soil")
]

# Insert crops
for name, category_name, season, growth_period, water, soil in crops_data:
    category = FarmingCategory(category_name)
    category.save(cursor)
    category_id = category.get_id(cursor)
    crop = Crop(name, category_id, season, growth_period, water, soil)
    crop.save(cursor)

# Commit and close
conn.commit()
conn.close()

print("Farming categories and crops inserted successfully.")