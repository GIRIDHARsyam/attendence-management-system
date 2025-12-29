import sqlite3
import os

# --- Configuration ---
DB_FILE = 'attendance.db'
TABLE_NAME = 'attendance_log'
# ---------------------

print(f"Attempting to clear history from {DB_FILE}...")

# Check if the database file exists before trying to connect
if os.path.exists(DB_FILE):
    try:
        # Connect to the database
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        
        # --- This is the main command to delete all data ---
        cursor.execute(f"DELETE FROM {TABLE_NAME}")
        
        # --- This command resets the auto-incrementing ID back to 1 ---
        cursor.execute(f"DELETE FROM sqlite_sequence WHERE name='{TABLE_NAME}'")
        
        # Save the changes
        conn.commit()
        
        print(f"✅ Successfully cleared all records from the '{TABLE_NAME}' table.")
        
    except Exception as e:
        print(f"❌ An error occurred: {e}")
    finally:
        # Always close the connection
        if conn:
            conn.close()
else:
    print(f"⚠️ Database file '{DB_FILE}' not found. Nothing to clear.")