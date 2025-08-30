import sqlite3

# Connect to the database (or create it if it doesn't exist)
conn = sqlite3.connect("database/trial1.db")
cursor = conn.cursor()

# Create the farming_events table (replacing events)
cursor.execute('''
CREATE TABLE IF NOT EXISTS farming_events (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT,
    description TEXT,
    event_date TEXT,
    season TEXT,
    crop_related TEXT,
    location TEXT
)
''')

# Create farming_calendar table (replacing academic_calendar)
cursor.execute('''
CREATE TABLE IF NOT EXISTS farming_calendar (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    start_date TEXT,
    end_date TEXT,
    season TEXT,
    activity_type TEXT,
    description TEXT
)
''')

# Define FarmingEvent class
class FarmingEvent:
    def __init__(self, title, description, event_date, season, crop_related, location):
        self.title = title
        self.description = description
        self.event_date = event_date
        self.season = season
        self.crop_related = crop_related
        self.location = location

    def save_to_db(self, cursor):
        cursor.execute('''
            INSERT INTO farming_events (title, description, event_date, season, crop_related, location)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (self.title, self.description, self.event_date, self.season, 
              self.crop_related, self.location))

# Define FarmingActivity class
class FarmingActivity:
    def __init__(self, title, start_date, end_date, season, activity_type, description):
        self.title = title
        self.start_date = start_date
        self.end_date = end_date
        self.season = season
        self.activity_type = activity_type
        self.description = description

    def save_to_db(self, cursor):
        cursor.execute('''
            INSERT INTO farming_calendar (title, start_date, end_date, season, activity_type, description)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (self.title, self.start_date, self.end_date, self.season, 
              self.activity_type, self.description))

# Insert farming calendar activities
farming_activities = [
    FarmingActivity("Kharif Season Preparation", "2024-06-01", "2024-06-30", "Kharif", "Preparation", "Prepare fields for monsoon crops like rice, maize, cotton"),
    FarmingActivity("Monsoon Sowing", "2024-07-01", "2024-08-15", "Kharif", "Sowing", "Sow kharif crops with the onset of monsoon"),
    FarmingActivity("Kharif Crop Care", "2024-08-16", "2024-09-30", "Kharif", "Maintenance", "Weeding, pest control, and irrigation for kharif crops"),
    FarmingActivity("Kharif Harvest", "2024-10-01", "2024-11-30", "Kharif", "Harvest", "Harvest kharif crops and prepare for rabi season"),
    FarmingActivity("Rabi Season Preparation", "2024-11-01", "2024-11-30", "Rabi", "Preparation", "Prepare fields for winter crops like wheat, barley"),
    FarmingActivity("Rabi Sowing", "2024-12-01", "2024-12-31", "Rabi", "Sowing", "Sow rabi crops in winter season"),
    FarmingActivity("Rabi Crop Care", "2025-01-01", "2025-02-28", "Rabi", "Maintenance", "Fertilization, irrigation, and pest control for rabi crops"),
    FarmingActivity("Rabi Harvest", "2025-03-01", "2025-04-30", "Rabi", "Harvest", "Harvest rabi crops and prepare for summer"),
    FarmingActivity("Summer Vegetable Sowing", "2025-03-15", "2025-04-15", "Summer", "Sowing", "Sow summer vegetables like okra, cucumber, bitter gourd"),
    FarmingActivity("Summer Crop Care", "2025-04-16", "2025-05-31", "Summer", "Maintenance", "Irrigation and pest control for summer crops"),
    FarmingActivity("Summer Harvest", "2025-06-01", "2025-06-30", "Summer", "Harvest", "Harvest summer vegetables and prepare for kharif")
]

# Insert farming events
farming_events = [
    FarmingEvent("Kisan Mela 2024", "Annual farmers fair with latest farming technology and equipment", "2024-09-15", "Kharif", "General", "Agricultural University Ground"),
    FarmingEvent("Organic Farming Workshop", "Learn organic farming techniques and certification", "2024-10-20", "Kharif", "Education", "Community Hall"),
    FarmingEvent("Seed Distribution Program", "Government sponsored quality seed distribution", "2024-06-10", "Kharif", "Seeds", "Block Office"),
    FarmingEvent("Fertilizer Subsidy Camp", "Subsidized fertilizer distribution for farmers", "2024-11-05", "Rabi", "Fertilizer", "Krishi Vigyan Kendra"),
    FarmingEvent("Crop Insurance Registration", "Register for crop insurance coverage", "2024-06-20", "Kharif", "Insurance", "Bank Branch"),
    FarmingEvent("Soil Testing Camp", "Free soil testing and recommendations", "2024-07-05", "Kharif", "Soil Health", "Village Panchayat"),
    FarmingEvent("Pest Management Training", "Integrated pest management techniques", "2024-08-25", "Kharif", "Pest Control", "Agricultural Extension Office"),
    FarmingEvent("Water Conservation Workshop", "Efficient irrigation and water management", "2024-12-10", "Rabi", "Water Management", "Water Resources Department"),
    FarmingEvent("Market Linkage Program", "Connect farmers directly to markets", "2025-01-15", "Rabi", "Marketing", "Agricultural Marketing Board"),
    FarmingEvent("Climate Smart Farming", "Adapting to climate change in agriculture", "2025-02-20", "Rabi", "Climate", "Meteorological Department"),
    FarmingEvent("Harvest Festival", "Celebration of successful harvest season", "2025-04-15", "Summer", "Celebration", "Village Ground")
]

# Save both event types
for e in farming_activities:
    e.save_to_db(cursor)
for e in farming_events:
    e.save_to_db(cursor)

# Commit changes and close connection
conn.commit()
conn.close()

print("Farming events and calendar activities inserted successfully.")
