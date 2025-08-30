import sqlite3

# Connect to the database
conn = sqlite3.connect("database/trial1.db")
cursor = conn.cursor()

# Create the farming_techniques table (replacing subjects)
cursor.execute('''
CREATE TABLE IF NOT EXISTS farming_techniques (
    technique_id INTEGER PRIMARY KEY AUTOINCREMENT,
    technique_name TEXT UNIQUE NOT NULL,
    category TEXT,
    description TEXT
)
''')

# Create the farming_resources table (replacing playlists)
cursor.execute('''
CREATE TABLE IF NOT EXISTS farming_resources (
    resource_id INTEGER PRIMARY KEY AUTOINCREMENT,
    technique_id INTEGER,
    resource_type TEXT,
    title TEXT,
    url TEXT,
    description TEXT,
    FOREIGN KEY (technique_id) REFERENCES farming_techniques(technique_id)
)
''')

# Define FarmingTechnique class
class FarmingTechnique:
    def __init__(self, technique_name, category, description=""):
        self.technique_name = technique_name
        self.category = category
        self.description = description

    def save_to_db(self, cursor):
        try:
            cursor.execute('''
                INSERT INTO farming_techniques (technique_name, category, description)
                VALUES (?, ?, ?)
            ''', (self.technique_name, self.category, self.description))
        except sqlite3.IntegrityError:
            print(f"Technique '{self.technique_name}' already exists, skipping insert.")

    def get_id(self, cursor):
        cursor.execute('''
            SELECT technique_id FROM farming_techniques WHERE technique_name = ?
        ''', (self.technique_name,))
        return cursor.fetchone()[0]

# Define FarmingResource class
class FarmingResource:
    def __init__(self, technique_id, resource_type, title, url, description=""):
        self.technique_id = technique_id
        self.resource_type = resource_type
        self.title = title
        self.url = url
        self.description = description

    def save_to_db(self, cursor):
        cursor.execute('''
            INSERT INTO farming_resources (technique_id, resource_type, title, url, description)
            VALUES (?, ?, ?, ?, ?)
        ''', (self.technique_id, self.resource_type, self.title, self.url, self.description))

# Insert farming techniques
farming_techniques = [
    FarmingTechnique("Organic Farming", "Sustainable Agriculture", "Natural farming methods without synthetic chemicals"),
    FarmingTechnique("Hydroponics", "Modern Farming", "Growing plants without soil using nutrient-rich water"),
    FarmingTechnique("Crop Rotation", "Traditional Farming", "Systematic planting of different crops in sequence"),
    FarmingTechnique("Integrated Pest Management", "Pest Control", "Combined approach to pest control using multiple methods"),
    FarmingTechnique("Precision Agriculture", "Technology", "Using technology for precise farming operations"),
    FarmingTechnique("Vertical Farming", "Urban Agriculture", "Growing crops in vertically stacked layers"),
    FarmingTechnique("Aquaponics", "Aquaculture", "Combining fish farming with hydroponic plant cultivation"),
    FarmingTechnique("Natural Farming", "Traditional", "Farming methods that work with natural ecosystems"),
    FarmingTechnique("Greenhouse Farming", "Protected Cultivation", "Growing crops in controlled environment structures"),
    FarmingTechnique("Drip Irrigation", "Water Management", "Efficient water delivery system for crops")
]

for technique in farming_techniques:
    technique.save_to_db(cursor)

# Define resource data (replace URLs with real ones)
farming_resources = {
    "Organic Farming": [
        ("Video", "Complete Guide to Organic Farming", "https://youtube.com/watch?v=organic_farming_guide", "Step-by-step organic farming tutorial"),
        ("Article", "Organic Certification Process", "https://agriculture.gov.in/organic-certification", "Government guidelines for organic certification"),
        ("Video", "Natural Pest Control Methods", "https://youtube.com/watch?v=natural_pest_control", "Chemical-free pest management techniques")
    ],
    "Hydroponics": [
        ("Video", "Hydroponics for Beginners", "https://youtube.com/watch?v=hydroponics_basics", "Introduction to soil-less farming"),
        ("Article", "Hydroponic System Types", "https://hydroponics.com/system-types", "Different hydroponic system configurations"),
        ("Video", "Nutrient Solution Preparation", "https://youtube.com/watch?v=nutrient_solutions", "Making nutrient solutions for hydroponics")
    ],
    "Crop Rotation": [
        ("Video", "Crop Rotation Planning", "https://youtube.com/watch?v=crop_rotation_planning", "How to plan crop rotation cycles"),
        ("Article", "Crop Rotation Benefits", "https://farming.com/crop-rotation-benefits", "Scientific benefits of crop rotation"),
        ("Video", "Seasonal Crop Planning", "https://youtube.com/watch?v=seasonal_planning", "Planning crops based on seasons")
    ],
    "Integrated Pest Management": [
        ("Video", "IPM Strategies", "https://youtube.com/watch?v=ipm_strategies", "Integrated pest management approaches"),
        ("Article", "Beneficial Insects", "https://pestcontrol.com/beneficial-insects", "Using beneficial insects for pest control"),
        ("Video", "Biological Pest Control", "https://youtube.com/watch?v=biological_control", "Natural pest control methods")
    ],
    "Precision Agriculture": [
        ("Video", "GPS in Farming", "https://youtube.com/watch?v=gps_farming", "Using GPS technology in agriculture"),
        ("Article", "Smart Farming Sensors", "https://smartfarming.com/sensors", "IoT sensors for precision agriculture"),
        ("Video", "Drone Technology in Farming", "https://youtube.com/watch?v=drones_farming", "Using drones for crop monitoring")
    ],
    "Vertical Farming": [
        ("Video", "Vertical Farm Setup", "https://youtube.com/watch?v=vertical_farm_setup", "Building vertical farming systems"),
        ("Article", "Urban Agriculture Guide", "https://urbanfarming.com/guide", "Farming in urban environments"),
        ("Video", "Indoor Farming Techniques", "https://youtube.com/watch?v=indoor_farming", "Growing crops indoors")
    ],
    "Aquaponics": [
        ("Video", "Aquaponics System Design", "https://youtube.com/watch?v=aquaponics_design", "Designing aquaponics systems"),
        ("Article", "Fish Selection for Aquaponics", "https://aquaponics.com/fish-selection", "Choosing fish species for aquaponics"),
        ("Video", "Aquaponics Maintenance", "https://youtube.com/watch?v=aquaponics_maintenance", "Maintaining aquaponics systems")
    ],
    "Natural Farming": [
        ("Video", "Natural Farming Principles", "https://youtube.com/watch?v=natural_farming_principles", "Core principles of natural farming"),
        ("Article", "Zero Budget Natural Farming", "https://naturalfarming.com/zero-budget", "Low-cost natural farming methods"),
        ("Video", "Natural Fertilizer Making", "https://youtube.com/watch?v=natural_fertilizer", "Making organic fertilizers at home")
    ],
    "Greenhouse Farming": [
        ("Video", "Greenhouse Construction", "https://youtube.com/watch?v=greenhouse_construction", "Building greenhouse structures"),
        ("Article", "Climate Control in Greenhouses", "https://greenhouse.com/climate-control", "Managing temperature and humidity"),
        ("Video", "Greenhouse Crop Management", "https://youtube.com/watch?v=greenhouse_management", "Managing crops in greenhouses")
    ],
    "Drip Irrigation": [
        ("Video", "Drip System Installation", "https://youtube.com/watch?v=drip_installation", "Installing drip irrigation systems"),
        ("Article", "Water Conservation in Farming", "https://waterconservation.com/farming", "Water-saving farming techniques"),
        ("Video", "Drip System Maintenance", "https://youtube.com/watch?v=drip_maintenance", "Maintaining drip irrigation systems")
    ]
}

# Insert farming resources
for technique_name, resources in farming_resources.items():
    technique = FarmingTechnique(technique_name, "")
    technique_id = technique.get_id(cursor)
    for resource_type, title, url, description in resources:
        resource = FarmingResource(technique_id, resource_type, title, url, description)
        resource.save_to_db(cursor)

# Commit and close
conn.commit()
conn.close()

print("Farming techniques and resources inserted successfully.")
