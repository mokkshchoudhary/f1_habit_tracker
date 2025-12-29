from fastapi import FastAPI
from pydantic import BaseModel, Field
import json

app = FastAPI()

class Habits(BaseModel):
    id : int
    name : str = Field(..., min_length = 3)
    description : str | None = None

def load_data():
    with open('habits.json', 'r') as f:
        data = json.load(f)
    return data

def save_data(data):
    with open('habits.json', 'w') as f:
        json.dump(data, f)

@app.get("/progress")
def home():
    return {'Message':'Starting from basic'}

@app.get("/about")
def home():
    return {'Title':'F1 based habit tracker'}

@app.post('/create_habit')
def CreateHabit(habits: Habits):
    return habits

@app.get('all_habits')
def all_habits(habits:Habits):
    data = load_data()
    return data