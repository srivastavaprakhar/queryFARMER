import sqlite3

# Connect to the database
conn = sqlite3.connect("database/trial1.db")
cursor = conn.cursor()

# Create the plant_diseases table
cursor.execute('''
CREATE TABLE IF NOT EXISTS plant_diseases (
    disease_id INTEGER PRIMARY KEY AUTOINCREMENT,
    disease_name TEXT NOT NULL,
    crop_affected TEXT,
    symptoms TEXT,
    causes TEXT,
    treatment TEXT,
    prevention TEXT,
    severity TEXT
)
''')

# Create the pests table
cursor.execute('''
CREATE TABLE IF NOT EXISTS pests (
    pest_id INTEGER PRIMARY KEY AUTOINCREMENT,
    pest_name TEXT NOT NULL,
    crop_affected TEXT,
    damage_description TEXT,
    control_methods TEXT,
    natural_predators TEXT,
    season_active TEXT
)
''')

# Define PlantDisease class
class PlantDisease:
    def __init__(self, disease_name, crop_affected, symptoms, causes, treatment, prevention, severity):
        self.disease_name = disease_name
        self.crop_affected = crop_affected
        self.symptoms = symptoms
        self.causes = causes
        self.treatment = treatment
        self.prevention = prevention
        self.severity = severity

    def save_to_db(self, cursor):
        cursor.execute('''
            INSERT INTO plant_diseases (disease_name, crop_affected, symptoms, causes, treatment, prevention, severity)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (self.disease_name, self.crop_affected, self.symptoms, self.causes, 
              self.treatment, self.prevention, self.severity))

# Define Pest class
class Pest:
    def __init__(self, pest_name, crop_affected, damage_description, control_methods, natural_predators, season_active):
        self.pest_name = pest_name
        self.crop_affected = crop_affected
        self.damage_description = damage_description
        self.control_methods = control_methods
        self.natural_predators = natural_predators
        self.season_active = season_active

    def save_to_db(self, cursor):
        cursor.execute('''
            INSERT INTO pests (pest_name, crop_affected, damage_description, control_methods, natural_predators, season_active)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (self.pest_name, self.crop_affected, self.damage_description, 
              self.control_methods, self.natural_predators, self.season_active))

# Insert plant diseases
plant_diseases = [
    PlantDisease(
        "Bacterial Blight",
        "Rice, Cotton",
        "Water-soaked lesions, yellowing leaves, wilting",
        "Bacteria, contaminated seeds, poor drainage",
        "Remove infected plants, apply copper-based fungicides",
        "Use disease-free seeds, proper field drainage, crop rotation",
        "High"
    ),
    PlantDisease(
        "Powdery Mildew",
        "Wheat, Grapes, Cucumber",
        "White powdery spots on leaves, stunted growth",
        "Fungal infection, high humidity, poor air circulation",
        "Apply sulfur-based fungicides, improve air circulation",
        "Plant resistant varieties, proper spacing, avoid overhead irrigation",
        "Medium"
    ),
    PlantDisease(
        "Root Rot",
        "Tomato, Potato, Cotton",
        "Wilting, yellow leaves, brown/black roots",
        "Fungal pathogens, overwatering, poor drainage",
        "Remove infected plants, improve drainage, apply fungicides",
        "Well-drained soil, avoid overwatering, crop rotation",
        "High"
    ),
    PlantDisease(
        "Leaf Spot",
        "Maize, Soybean, Vegetables",
        "Brown spots with yellow halos, leaf drop",
        "Fungal infection, wet conditions, poor hygiene",
        "Remove infected leaves, apply fungicides",
        "Clean field debris, proper spacing, avoid overhead watering",
        "Medium"
    ),
    PlantDisease(
        "Viral Mosaic",
        "Tobacco, Tomato, Cucumber",
        "Mottled leaves, stunted growth, distorted fruits",
        "Virus transmission by insects, contaminated tools",
        "Remove infected plants, control insect vectors",
        "Use virus-free seeds, control aphids, clean tools",
        "High"
    ),
    PlantDisease(
        "Downy Mildew",
        "Grapes, Cucumber, Onion",
        "Yellow spots on upper leaves, white mold underneath",
        "Fungal infection, cool wet weather",
        "Apply copper fungicides, improve air circulation",
        "Resistant varieties, proper spacing, avoid overhead irrigation",
        "Medium"
    ),
    PlantDisease(
        "Anthracnose",
        "Mango, Beans, Tomato",
        "Dark sunken lesions on fruits and stems",
        "Fungal infection, warm humid conditions",
        "Prune infected parts, apply fungicides",
        "Clean field debris, proper spacing, avoid overhead watering",
        "Medium"
    ),
    PlantDisease(
        "Fusarium Wilt",
        "Banana, Tomato, Cotton",
        "Yellowing leaves, wilting, vascular discoloration",
        "Soil-borne fungus, contaminated soil",
        "Remove infected plants, soil fumigation",
        "Use resistant varieties, crop rotation, clean equipment",
        "High"
    )
]

# Insert pests
pests = [
    Pest(
        "Aphids",
        "Multiple crops",
        "Suck sap from leaves, transmit viruses, cause leaf curling",
        "Insecticidal soap, neem oil, beneficial insects",
        "Ladybugs, lacewings, parasitic wasps",
        "Spring to Fall"
    ),
    Pest(
        "Armyworms",
        "Maize, Rice, Wheat",
        "Feed on leaves, can defoliate entire fields",
        "Bacillus thuringiensis, hand picking, insecticides",
        "Birds, parasitic wasps, predatory beetles",
        "Monsoon season"
    ),
    Pest(
        "Bollworms",
        "Cotton, Maize, Tomato",
        "Feed on flowers and fruits, reduce yield",
        "Bacillus thuringiensis, pheromone traps, insecticides",
        "Birds, parasitic wasps, predatory bugs",
        "Flowering season"
    ),
    Pest(
        "Thrips",
        "Onion, Garlic, Cotton",
        "Scar leaves and flowers, transmit viruses",
        "Neem oil, insecticidal soap, reflective mulch",
        "Predatory mites, minute pirate bugs",
        "Dry seasons"
    ),
    Pest(
        "Whiteflies",
        "Tomato, Cotton, Vegetables",
        "Suck sap, secrete honeydew, transmit viruses",
        "Yellow sticky traps, neem oil, insecticides",
        "Parasitic wasps, predatory beetles",
        "Warm seasons"
    ),
    Pest(
        "Mealybugs",
        "Fruits, Vegetables, Ornamentals",
        "Suck sap, secrete honeydew, cause sooty mold",
        "Alcohol swabs, neem oil, systemic insecticides",
        "Ladybugs, parasitic wasps",
        "All year"
    ),
    Pest(
        "Spider Mites",
        "Multiple crops",
        "Suck cell contents, cause stippling and webbing",
        "Water sprays, neem oil, miticides",
        "Predatory mites, ladybugs",
        "Hot dry weather"
    ),
    Pest(
        "Cutworms",
        "Seedlings, young plants",
        "Cut stems at soil level, feed at night",
        "Collars around plants, hand picking, insecticides",
        "Birds, parasitic wasps, ground beetles",
        "Spring planting"
    )
]

# Save diseases and pests
for disease in plant_diseases:
    disease.save_to_db(cursor)

for pest in pests:
    pest.save_to_db(cursor)

# Commit and close
conn.commit()
conn.close()

print("Plant diseases and pests data inserted successfully.")
