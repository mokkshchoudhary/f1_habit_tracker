from fastapi import FastAPI, HTTPException, Path
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
from typing import Annotated
import json

app = FastAPI()

class Habits(BaseModel):
    id : Annotated[str, Field(...,description = 'The id of the habit', examples = ['001'])]
    name : Annotated[str, Field (..., description = 'Name of Habit')]
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
def CreateHabit(habit: Habits):
    data = load_data()

    if habit.id in data:
        raise HTTPException (status_code = 400, description = 'Habit exist/ Bad request')
    
    data[habit.id] = habit.model_dump(exclude = ['id'])
    
    save_data(data)

    return JSONResponse(status_code = 201, content = {'message':'Habit Created Successfully'})

@app.get('/get_habit/{habit_id}')
def view_habit(habit_id : str = Path (...,description = "ID of the habit in our Database", example ='1,2,3')):
    data = load_data()

    if habit_id in data:
        return data[habit_id]
    raise HTTPException(status_code = 404,detail = 'Invalid ID/page request')