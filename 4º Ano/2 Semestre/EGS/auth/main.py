from fastapi import Depends, FastAPI, HTTPException, Response, status
from fastapi.security import OAuth2PasswordRequestForm, OAuth2AuthorizationCodeBearer
from sqlalchemy.orm import Session
from app.auth.auth_routes import router as auth_router


app = FastAPI()

app.include_router(auth_router)



