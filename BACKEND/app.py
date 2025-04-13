from fastapi import HTTPException
from fastapi import FastAPI
from pydantic import BaseModel
from motor.motor_asyncio import AsyncIOMotorClient
from passlib.context import CryptContext
import os
from dotenv import load_dotenv
import logging

# Load environment variables
load_dotenv()

# Initialize FastAPI app
app = FastAPI()

# Password hashing setup using Passlib (bcrypt)
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# MongoDB connection setup with Motor
MONGO_URI = os.getenv("MONGO_URI")
client = AsyncIOMotorClient(MONGO_URI)
db = client.get_database()  # Default database (based on URI)
users_collection = db.get_collection("users")  # Collection for users

# Define Pydantic model for request body validation
class User(BaseModel):
    username: str
    email: str
    password: str

# Utility function to hash password
def hash_password(password: str):
    return pwd_context.hash(password)

# Endpoint for signup
@app.post("/signup")
async def signup(user: User):
    # Check if the user already exists
    existing_user = await users_collection.find_one({"email": user.email})
    if existing_user:
        raise HTTPException(status_code=400, detail="User already exists")

    # Hash password
    hashed_password = hash_password(user.password)

    # Create a new user document
    new_user = {
        "username": user.username,
        "email": user.email,
        "password": hashed_password
    }

    # Insert the new user into the database
    result = await users_collection.insert_one(new_user)
    if result.acknowledged:
        return {"message": "User created successfully"}
    else:
        raise HTTPException(status_code=500, detail="Server error")

# Basic test route
@app.get("/")
async def read_root():
    return {"message": "Hello World"}
