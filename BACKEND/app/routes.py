from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from .database import get_db
from . import schemas, crud, models

router = APIRouter()

@router.post("/register/")
def register(user: schemas.UserCreate, db: Session = Depends(get_db)):
    return crud.create_user(db, user)

@router.post("/preferences/")
def set_preferences(prefs: schemas.PreferencesCreate, db: Session = Depends(get_db)):
    return crud.add_preferences(db, prefs)

@router.post("/login/")
def login_user(email: str, password: str, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.email == email).first()
    if not user or user.password != password:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    return {"id": user.id, "name": user.full_name}

@router.post("/generate-meal-plan/{user_id}")
def generate_plan(user_id: int, db: Session = Depends(get_db)):
    return crud.generate_meal_plan(db, user_id)
