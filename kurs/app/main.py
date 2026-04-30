import os
import csv
from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from datetime import datetime
from pydantic import BaseModel

app = FastAPI()

# Получаем путь к текущему файлу (main.py)
current_dir = os.path.dirname(os.path.abspath(__file__))
CSV_FILE = os.path.join(current_dir, 'calendar_data.csv')



class CalendarEvent(BaseModel):
    user_id: int
    date: str
    title: str
    description: str = ""

def init_csv():
    if not os.path.exists(CSV_FILE):
        with open(CSV_FILE, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(['user_id', 'date', 'title', 'description'])

init_csv()

@app.get("/")
async def read_index():
    return FileResponse('static/index.html')

@app.get("/api/events/{user_id}")
async def get_events(user_id: int):
    events = []
    try:
        with open(CSV_FILE, mode='r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                if int(row['user_id']) == user_id:
                    events.append(row)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    return events

@app.post("/api/events/")
async def create_event(event: CalendarEvent):
    try:
        with open(CSV_FILE, mode='a', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow([
                event.user_id,
                event.date,
                event.title,
                event.description
            ])
        return {"status": "success"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.delete("/api/events/{user_id}")
async def delete_event(user_id: int, date: str, title: str):
    try:
        rows = []
        found = False
        
        with open(CSV_FILE, mode='r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                if (int(row['user_id']) == user_id and 
                    row['date'] == date and 
                    row['title'] == title):
                    found = True
                else:
                    rows.append(row)
        
        if found:
            with open(CSV_FILE, mode='w', newline='', encoding='utf-8') as file:
                writer = csv.writer(file)
                writer.writerow(['user_id', 'date', 'title', 'description'])
                for row in rows:
                    writer.writerow([row['user_id'], row['date'], row['title'], row['description']])
            return {"status": "deleted"}
        else:
            raise HTTPException(status_code=404, detail="Event not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

app.mount("/static", StaticFiles(directory="static"), name="static")