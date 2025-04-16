from pydantic import BaseModel
from typing import Optional

class UserCreate(BaseModel):
    full_name: str
    age: int
    email: str
    password: str
    profile_icon: Optional[str]

class PreferencesCreate(BaseModel):
    user_id: int
    allergy: Optional[str]
    dietary_preference: Optional[str]
    fitness_goal: Optional[str]
