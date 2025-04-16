from sqlalchemy import Column, Integer, String, Text, ForeignKey, Enum, Boolean, Date
from sqlalchemy.orm import relationship
from .database import Base

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    full_name = Column(String(100))
    age = Column(Integer)
    email = Column(String(100), unique=True)
    password = Column(String(255))
    profile_icon = Column(String(255))
    preferences = relationship("UserPreference", back_populates="user", uselist=False)

class UserPreference(Base):
    __tablename__ = "user_preferences"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    allergy = Column(Text)
    dietary_preference = Column(Text)
    fitness_goal = Column(Text)
    user = relationship("User", back_populates="preferences")

class Meal(Base):
    __tablename__ = "meals"
    id = Column(Integer, primary_key=True)
    name = Column(String(100))
    meal_type = Column(Enum('Breakfast', 'Lunch', 'Dinner', 'Snack'))
    description = Column(Text)
    default_ingredients = Column(Text)

class MealPlan(Base):
    __tablename__ = "meal_plans"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    meal_id = Column(Integer, ForeignKey("meals.id"))
    plan_date = Column(Date)

class ShoppingList(Base):
    __tablename__ = "shopping_list"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    item_name = Column(String(100))
    quantity = Column(String(50))
    purchased = Column(Boolean, default=False)

class MealLog(Base):
    __tablename__ = "meal_logs"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    meal_id = Column(Integer, ForeignKey("meals.id"))
    log_date = Column(Date)
    adherence = Column(Boolean, default=True)
