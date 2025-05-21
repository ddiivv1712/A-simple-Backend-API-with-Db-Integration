from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from enum import Enum
from datetime import date, time
import sqlite3
import os

app = FastAPI(title="Remind Me Later API")                 # Initialize FastAPI app
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) # Define the base directory and database path
DB_DIR = os.path.join(BASE_DIR, "db")
DB_PATH = os.path.join(DB_DIR, "reminders.db")

print(f"Base directory: {BASE_DIR}")
print(f"Database directory: {DB_DIR}")
print(f"Database path: {DB_PATH}")

os.makedirs(DB_DIR, exist_ok=True)                         # Create database directory if it doesn't exist
conn = sqlite3.connect(DB_PATH)                            # Initialize SQLite database
cursor = conn.cursor()
cursor.execute('''
CREATE TABLE IF NOT EXISTS reminders (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    date TEXT NOT NULL,
    time TEXT NOT NULL,
    message TEXT NOT NULL,
    remind_via TEXT NOT NULL
)
''')
conn.commit()
conn.close()

class ReminderMethod(str, Enum):                          # Define enum for reminder methods
    EMAIL = "email"
    SMS = "sms"
    PUSH_NOTIFICATION = "push_notification"

class ReminderRequest(BaseModel):                         # Define request model
    date: date
    time: time
    message: str
    remind_via: ReminderMethod

class ReminderResponse(BaseModel):                         # Define response model
    id: int
    date: date
    time: time
    message: str
    remind_via: str

@app.post("/reminders", response_model=ReminderResponse)
def create_reminder(reminder: ReminderRequest):
    """
    Create a new reminder with the given date, time, message, and reminder method.
    """
    try:
        conn = sqlite3.connect(DB_PATH)                        # Connect to database
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO reminders (date, time, message, remind_via) VALUES (?, ?, ?, ?)",                     # Insert reminder into database
            (
                reminder.date.isoformat(),
                reminder.time.isoformat(),
                reminder.message,
                reminder.remind_via
            )
        )
        conn.commit()
        reminder_id = cursor.lastrowid                           # Get the ID of the inserted reminder
        response = ReminderResponse(                            # Create response
            id=reminder_id,
            date=reminder.date,
            time=reminder.time,
            message=reminder.message,
            remind_via=reminder.remind_via
        )
        conn.close()
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")