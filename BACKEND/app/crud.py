from sqlalchemy.orm import Session
from . import models, schemas
from datetime import date
import random

def create_user(db: Session, user: schemas.UserCreate):
    db_user = models.User(**user.dict())
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def add_preferences(db: Session, prefs: schemas.PreferencesCreate):
    db_prefs = models.UserPreference(**prefs.dict())
    db.add(db_prefs)
    db.commit()
    db.refresh(db_prefs)
    return db_prefs

def generate_meal_plan(db: Session, user_id: int):
    meals = db.query(models.Meal).all()
    meal_types = ['Breakfast', 'Lunch', 'Dinner']
    today = date.today()

    for meal_type in meal_types:
        meal_options = [m for m in meals if m.meal_type == meal_type]
        if meal_options:
            chosen = random.choice(meal_options)
            db_plan = models.MealPlan(user_id=user_id, meal_id=chosen.id, plan_date=today)
            db.add(db_plan)
    db.commit()
    return {"message": "Meal plan generated."}
