from fastapi import APIRouter, HTTPException
from database import db
from auth_utils import verify_password, create_access_token, get_password_hash
from pydantic import BaseModel

router = APIRouter(prefix="/auth", tags=["Auth"])

class LoginRequest(BaseModel):
    username: str
    password: str

class RegisterRequest(BaseModel):
    username: str
    email: str
    password: str

@router.post("/login")
def login(user: LoginRequest):
    db_user = db["users"].find_one({"username": user.username})

    if not db_user:
        raise HTTPException(status_code=400, detail="Invalid username")

    if not verify_password(user.password, db_user["password"]):
        raise HTTPException(status_code=400, detail="Invalid password")

    token = create_access_token({"sub": db_user["username"]})

    # Return user info including role
    return {
        "access_token": token,
        "token_type": "bearer",
        "user": {
            "username": db_user["username"],
            "email": db_user.get("email", ""),
            "role": db_user.get("role", "user")
        }
    }

@router.post("/register")
def register(user: RegisterRequest):
    # Check if username already exists
    existing_user = db["users"].find_one({"username": user.username})
    if existing_user:
        raise HTTPException(status_code=400, detail="Username already exists")
    
    # Check if email already exists
    existing_email = db["users"].find_one({"email": user.email})
    if existing_email:
        raise HTTPException(status_code=400, detail="Email already exists")
    
    # Hash password
    hashed_password = get_password_hash(user.password)
    
    # Create new user (default role is "user")
    new_user = {
        "username": user.username,
        "email": user.email,
        "password": hashed_password,
        "role": "user"
    }
    
    db["users"].insert_one(new_user)
    
    return {"message": "User registered successfully"}
