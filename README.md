# Remind Me Later – Simple Reminder API

This is a small, focused REST API for the "Remind Me Later" app. It's very simple: the frontend already lets users set a reminder by choosing a date, time, a message, and how they want to be reminded (like by SMS or email). This backend API just saves that info to a database.

That's it. No message sending, no scheduling engines—just clean input, validation, and storage.

## Features
- Single POST endpoint to receive and store reminder data
- Supports SMS and Email reminder methods
- Input validation using Pydantic
- SQLite database for data storage

## Requirements
- Python 3.7+
- FastAPI
- Uvicorn (for running the server)

## Installation
1. Install the required packages:
```bash
pip install fastapi uvicorn
```

## Running the Application
1. Start the FastAPI server:
```bash
uvicorn app.main:app --reload
```
2. The API will be available at http://localhost:8000
3. Interactive API documentation is available at http://localhost:8000/docs

## API Endpoint
### Create a Reminder
**POST** `/reminders`

Request body:
```json
{
  "date": "2023-05-21",
  "time": "15:30:00",
  "message": "Don't forget to submit your assignment!",
  "remind_via": "sms"
}
```

Response:
```json
{
  "id": 1,
  "date": "2023-05-21",
  "time": "15:30:00",
  "message": "Don't forget to submit your assignment!",
  "remind_via": "sms"
}
```