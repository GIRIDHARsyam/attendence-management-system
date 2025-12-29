import face_recognition
import pickle
import cv2
import os
import sqlite3 # <-- This is the database library
from datetime import datetime

# --- Database Setup ---
DB_FILE = 'attendance.db'

def setup_database():
    """Creates the database and tables if they don't exist."""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    
    # Create the main attendance log table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS attendance_log (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        roll_no TEXT NOT NULL,
        date TEXT NOT NULL,
        time TEXT NOT NULL,
        UNIQUE(roll_no, date) 
    )
    ''')
    # UNIQUE(roll_no, date) ensures a person is only marked once per day
    
    conn.commit()
    conn.close()
    print(f"[INFO] Database '{DB_FILE}' is ready.")
# ----------------------

# --- Attendance Logging Function (Now with SQL) ---
def markAttendance(name_rollno):
    try:
        name, roll_no = name_rollno.rsplit('_', 1)
    except ValueError:
        print(f"[WARNING] Skipping unrecognized name format: {name_rollno}")
        return

    today_date = datetime.now().strftime('%Y-%m-%d')
    time_string = datetime.now().strftime('%H:%M:%S')
    
    try:
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        
        # Try to insert the new attendance record
        # The UNIQUE constraint will cause an error if the person is already marked
        cursor.execute(
            "INSERT INTO attendance_log (name, roll_no, date, time) VALUES (?, ?, ?, ?)",
            (name, roll_no, today_date, time_string)
        )
        conn.commit()
        print(f"[ATTENDANCE] Marked {name} ({roll_no}) as present at {time_string}")
        
    except sqlite3.IntegrityError:
        # This error means the (roll_no, date) combination already exists
        # So, the person is already marked. We can just ignore it.
        pass
    except Exception as e:
        print(f"[ERROR] Database error: {e}")
    finally:
        if conn:
            conn.close()
# ---------------------------------

# --- Main Program ---

# 1. Setup the database first
setup_database()

# 2. Load Encodings
print("[INFO] Loading encodings...")
try:
    with open("encodings.pickle", "rb") as f:
        data = pickle.load(f)
except FileNotFoundError:
    print("[ERROR] Encodings file not found. Please run train_model.py first.")
    exit()

knownEncodings = data["encodings"]
knownNames = data["names"] # These are "Name_RollNo"

# 3. Initialize Webcam
print("[INFO] Starting video stream...")
cam = cv2.VideoCapture(0)

while True:
    ret, frame = cam.read()
    if not ret:
        print("[ERROR] Failed to grab frame")
        break

    # We are using 'hog' model, which needs RGB
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    small_frame = cv2.resize(rgb_frame, (0, 0), fx=0.25, fy=0.25)

    face_locations = face_recognition.face_locations(small_frame, model="hog")
    face_encodings = face_recognition.face_encodings(small_frame, face_locations)

    current_names = []

    for face_encoding in face_encodings:
        matches = face_recognition.compare_faces(knownEncodings, face_encoding)
        name_rollno = "Unknown" 

        face_distances = face_recognition.face_distance(knownEncodings, face_encoding)
        best_match_index = face_distances.argmin()
        if matches[best_match_index]:
            name_rollno = knownNames[best_match_index] 

        current_names.append(name_rollno)

    # --- Draw rectangles and Mark Attendance ---
    for (top, right, bottom, left), name_rollno in zip(face_locations, current_names):
        # Scale back up face locations
        top *= 4
        right *= 4
        bottom *= 4
        left *= 4

        cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)
        cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 255, 0), cv2.FILLED)
        font = cv2.FONT_HERSHEY_DUPLEX
        cv2.putText(frame, name_rollno, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)

        if name_rollno != "Unknown":
            markAttendance(name_rollno) # This now calls our SQL function
    
    cv2.imshow('Attendance System - Press "q" to quit', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Clean up
print("[INFO] Cleaning up...")
cam.release()
cv2.destroyAllWindows()