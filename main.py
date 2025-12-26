from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Annotated
import models
import schemas
import database
import json 
import redis 

models.Base.metadata.create_all(bind=database.engine)
app = FastAPI()

def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/home")
def home():
    return {'message':'This is f1 habit tracker app. Database is connected'}

@app.post("/habits", response_model = schemas.HabitResponse)

def create_habit(habit: schemas.HabitCreate, db: Session = Depends (get_db)):
    new_habit = models.Habit(
        name=habit.name,
        description = habit.description
    )
    db.add(new_habit)
    db.commit()
    db.refresh(new_habit)

    return new_habit

@app.get("/habits", response_model = List[schemas.HabitResponse])
def get_habits(db: Session = Depends(get_db)):
    habits = db.query(models.Habit).all()
    return habits

@app.get("/habits", response_model = List[schemas.HabitResponse])
def get_habits(db: Session = Depends(get_db)):

    cached_habits = r.get("all_habits")

    if cached_habits:
        print('loaded fromm redis cache')
        return json.loads(cached_habits)
    
    print('Loaded from database')
    habits = db.query(models.Habit).all()

    habits_list = [
        {
            "id": h.id,
            "name": h.name,
            "description": h.description,
            "created_at": h.created_at.isoformat(),
            "is_completed_today" : h.is_completed_today        
        }
        for h in habits
    ]
    r.setex('all_habits', 60, json.dumps(habits_list))

    return habits

@app.patch('/habits/{habit_id}/complete', response_model = schemas. HabitResponse)
def complete_habit(habit_id: int, db: Session = Depends(get_db)):

    habit = db.query (models.habit). filter(models.Habit.id == habit_id).first()

    if not habit:
        raise HTTPException (status_code = 404, detail="Habit not found")
    
    habit.is_completed_today = True

    db.commit()
    db.refresh(habit)

    r.delete("all_habits")
    print('Habit updated and Redis cache cleared')

    return habit