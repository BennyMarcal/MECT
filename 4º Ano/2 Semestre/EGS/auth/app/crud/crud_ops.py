from pymongo import MongoClient
from app.resp_models.model import UserInDB, User
from app.auth.authorization import get_password_hash, verify_password
import os

def conn_db():
    uri = os.getenv("DATABASE_URL")
    client = MongoClient(uri)
    return client

def get_db():
    client = conn_db()
    db = client.users  # Assuming you are using a 'users' database
    return db

def authenticate_user(username: str, password: str):
    user = get_user(username)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user

def insert_user(user: UserInDB):
    db = get_db()
    coll = db.users
    cursor_user = coll.find({"$or": [{"username": user.username}, {"email": user.email}]})
    for p in cursor_user:
        if p:
            return {"message": "User already created"}
    user.id = coll.count_documents({})
    user.hashed_password = get_password_hash(user.hashed_password)
    user_dict = user.dict()
    result = coll.insert_one(user_dict)
    return User(**user_dict)

def get_user(username: str):
    db = get_db()
    coll = db.users
    cursor_user = coll.find({"username": username})
    for user in cursor_user:
        if user:
            return UserInDB(**user)
