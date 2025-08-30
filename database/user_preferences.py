import sqlite3
import os

def create_user_preferences_table():
    """Create user preferences table for language and voice settings"""
    
    # Ensure database directory exists
    os.makedirs("database", exist_ok=True)
    
    # Connect to database
    conn = sqlite3.connect("database/trial1.db")
    cursor = conn.cursor()
    
    try:
        # Create user_preferences table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS user_preferences (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                preferred_language TEXT DEFAULT 'en',
                voice_enabled BOOLEAN DEFAULT 0,
                voice_language TEXT DEFAULT 'en-IN',
                voice_speed REAL DEFAULT 1.0,
                voice_pitch REAL DEFAULT 1.0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Create index on username for faster lookups
        cursor.execute('''
            CREATE INDEX IF NOT EXISTS idx_user_preferences_username 
            ON user_preferences(username)
        ''')
        
        # Insert default preferences for existing users (if any)
        cursor.execute('''
            INSERT OR IGNORE INTO user_preferences (username, preferred_language, voice_enabled)
            SELECT username, 'en', 0 FROM users
        ''')
        
        conn.commit()
        print("SUCCESS: User preferences table created successfully")
        
    except Exception as e:
        print(f"ERROR: Error creating user preferences table: {e}")
        conn.rollback()
    
    finally:
        conn.close()

if __name__ == "__main__":
    create_user_preferences_table()
