import sqlite3

# Connect to (or create) the database
conn = sqlite3.connect("database/trial1.db")
cursor = conn.cursor()

# Create the table with detailed fields for farming equipment
cursor.execute("""
CREATE TABLE IF NOT EXISTS farming_equipment (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    category TEXT,
    price_range TEXT,
    usage TEXT,
    maintenance_frequency TEXT,
    power_source TEXT,
    location_hint TEXT,
    keywords TEXT
)
""")

# Sample data to insert for farming equipment
equipment_items = [
    {
        "name": "Tractor",
        "category": "Heavy Machinery",
        "price_range": "₹5,00,000 - ₹15,00,000",
        "usage": "Plowing, tilling, transportation",
        "maintenance_frequency": "Every 100 hours",
        "power_source": "Diesel",
        "location_hint": "Main equipment shed, near fuel storage",
        "keywords": "tractor,plow,till,transport,farming machine"
    },
    {
        "name": "Seed Drill",
        "category": "Planting Equipment",
        "price_range": "₹25,000 - ₹75,000",
        "usage": "Precise seed sowing",
        "maintenance_frequency": "Before each season",
        "power_source": "Tractor PTO",
        "location_hint": "Equipment storage area, with other planting tools",
        "keywords": "seed drill,planting,sowing,seeds,precision"
    },
    {
        "name": "Harvester",
        "category": "Harvesting Equipment",
        "price_range": "₹8,00,000 - ₹25,00,000",
        "usage": "Crop harvesting and threshing",
        "maintenance_frequency": "Every 50 hours",
        "power_source": "Diesel",
        "location_hint": "Large equipment bay, near grain storage",
        "keywords": "harvester,harvest,thresh,grain,combine"
    },
    {
        "name": "Drip Irrigation System",
        "category": "Irrigation Equipment",
        "price_range": "₹15,000 - ₹50,000",
        "usage": "Efficient water delivery to crops",
        "maintenance_frequency": "Monthly cleaning",
        "power_source": "Water pressure",
        "location_hint": "Field installation, near water source",
        "keywords": "drip irrigation,water,irrigation,efficient,conservation"
    },
    {
        "name": "Sprayer",
        "category": "Crop Protection",
        "price_range": "₹8,000 - ₹25,000",
        "usage": "Pesticide and fertilizer application",
        "maintenance_frequency": "After each use",
        "power_source": "Battery/Manual",
        "location_hint": "Tool storage area, with safety equipment",
        "keywords": "sprayer,pesticide,fertilizer,crop protection,application"
    },
    {
        "name": "Plow",
        "category": "Soil Preparation",
        "price_range": "₹5,000 - ₹15,000",
        "usage": "Soil turning and preparation",
        "maintenance_frequency": "Before each use",
        "power_source": "Tractor",
        "location_hint": "Equipment storage, with other soil tools",
        "keywords": "plow,soil preparation,tilling,land preparation"
    },
    {
        "name": "Cultivator",
        "category": "Soil Preparation",
        "price_range": "₹12,000 - ₹35,000",
        "usage": "Soil cultivation and weed control",
        "maintenance_frequency": "Before each season",
        "power_source": "Tractor PTO",
        "location_hint": "Equipment storage area, near tractor",
        "keywords": "cultivator,soil cultivation,weed control,soil preparation"
    },
    {
        "name": "Thresher",
        "category": "Post-Harvest",
        "price_range": "₹30,000 - ₹80,000",
        "usage": "Grain separation from crop",
        "maintenance_frequency": "Before harvest season",
        "power_source": "Electric/Diesel",
        "location_hint": "Post-harvest processing area",
        "keywords": "thresher,grain separation,post-harvest,processing"
    },
    {
        "name": "Water Pump",
        "category": "Irrigation Equipment",
        "price_range": "₹8,000 - ₹25,000",
        "usage": "Water pumping for irrigation",
        "maintenance_frequency": "Every 6 months",
        "power_source": "Electric/Diesel",
        "location_hint": "Near water source, pump house",
        "keywords": "water pump,irrigation,water supply,pumping"
    },
    {
        "name": "Greenhouse",
        "category": "Protected Cultivation",
        "price_range": "₹50,000 - ₹2,00,000",
        "usage": "Controlled environment farming",
        "maintenance_frequency": "Seasonal cleaning",
        "power_source": "Solar/Electric",
        "location_hint": "Designated greenhouse area",
        "keywords": "greenhouse,protected cultivation,controlled environment"
    }
]

# Insert data into the table
for item in equipment_items:
    cursor.execute("""
    INSERT INTO farming_equipment (name, category, price_range, usage, maintenance_frequency, power_source, location_hint, keywords)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        item["name"],
        item["category"],
        item["price_range"],
        item["usage"],
        item["maintenance_frequency"],
        item["power_source"],
        item["location_hint"],
        item["keywords"]
    ))

# Save and close
conn.commit()
conn.close()

print("Farming equipment data inserted successfully.")
