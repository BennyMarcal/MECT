from fastapi import APIRouter, Depends, HTTPException, Response, status
from fastapi.security import OAuth2PasswordRequestForm, OAuth2AuthorizationCodeBearer
from sqlalchemy.orm import Session
from app.crud.crud_ops import insert_user, get_user, authenticate_user, get_db
from app.resp_models.model import Token, UserInDB, User
from app.auth.gen_tokens import create_access_token
from app.auth.gen_tokens import oauth2_scheme, TokenData
from jose import jwt, JWTError
from datetime import timedelta
from fastapi.responses import RedirectResponse
import requests
import base64

router = APIRouter(
    prefix="/auth",
    tags=["auth"]
)

JWT_EXPIRY = 30
JWT_SECRET = "48dd53b11f29fe0aceeb80a83b921b9fda93974121546cd8400eac7c2cc27c41"
JWT_ALGORITHM = "HS256"

oauth2_scheme_ua = OAuth2AuthorizationCodeBearer(
    authorizationUrl="https://wso2-gw.ua.pt/authorize",
    tokenUrl="https://wso2-gw.ua.pt/token",
    scopes={"openid": "OpenID authentication"}
)

oauth2_scheme_github = OAuth2AuthorizationCodeBearer(
    authorizationUrl="https://github.com/login/oauth/authorize",
    tokenUrl="https://github.com/login/oauth/access_token",
    scopes={"user": "User details"}
)

@router.get("/verify")
async def verify_user(token: str):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception
    user = get_user(username=token_data.username)
    if user is None:
        raise credentials_exception
    return User(**(user.dict()))


@router.post("/login", response_model=Token)
async def login(response: Response,
                form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=int(JWT_EXPIRY))
    token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    response.set_cookie(key="access_token", value = token.access_token, httponly=True, secure=True)
    return token

@router.post("/register", )
def register(user : UserInDB):
    return insert_user(user)

@router.get("/signin/ua")
async def signin():
    redirect_uri = "http://localhost:5000"
    client_id = "agh44RajMJcYvCIq3lSMrutfPJ0a"
    state = "1234567890"
    scope = "openid"
    authorization_url = f"https://wso2-gw.ua.pt/authorize?response_type=code&client_id={client_id}&state={state}&scope={scope}&redirect_uri={redirect_uri}"
    return RedirectResponse(url=authorization_url)

@router.get("/signin/github")
async def signin_github():
    redirect_uri = "http://localhost:8000/index"
    client_id = "ed07148229986602e861"
    state = "1234567890"
    scope = "user"
    authorization_url = f"https://github.com/login/oauth/authorize?client_id={client_id}&redirect_uri={redirect_uri}&state={state}&scope={scope}"
    return RedirectResponse(url=authorization_url)

@router.get("/callback/ua")
async def callback_ua(code: str, db: Session = Depends(get_db)):
    client_id = "agh44RajMJcYvCIq3lSMrutfPJ0a"
    client_secret = "WJckU0FSb41rsJHLnFPYqBFvSZoa"
    redirect_uri = "http://localhost:8080"
    data = {
        "grant_type": "authorization_code",
        "code": code,
        "redirect_uri": redirect_uri,
    }
    headers = {
        "Authorization": f"Basic {base64.b64encode(f'{client_id}:{client_secret}'.encode()).decode()}"
    }
    response = requests.post("https://wso2-gw.ua.pt/token", data=data, headers=headers)
    if response.status_code == 200:
        token_data = response.json()
        access_token = token_data.get("access_token")
        refresh_token = token_data.get("refresh_token")
        token_type = token_data.get("token_type")
        
        # Store user information in the database
        db.add(User(email="example@example.com", access_token=access_token, provider='ua'))
        db.commit()
        
        return {"access_token": access_token}
    else:
        raise HTTPException(status_code=response.status_code, detail="Failed to obtain access token")

@router.get("/callback/github")
async def callback_github(code: str, db: Session = Depends(get_db)):
    client_id = "ed07148229986602e861"
    client_secret = "5d7e5a7849a396f44c2dfd4cc59bf490fed0348b"
    redirect_uri = "http://localhost:8000/index"
    data = {
        "client_id": client_id,
        "client_secret": client_secret,
        "code": code,
        "redirect_uri": redirect_uri,
    }
    headers = {"Accept": "application/json"}
    response = requests.post("https://github.com/login/oauth/access_token", data=data, headers=headers)
    if response.status_code == 200:
        token_data = response.json()
        access_token = token_data.get("access_token")

        # Fetch user details
        headers = {"Authorization": f"token {access_token}"}
        user_response = requests.get("https://api.github.com/user", headers=headers)
        user_data = user_response.json()
        
        # Store user information in the database
        email = user_data.get('email', f"{user_data['login']}@github.com")  # Handle cases where email is not provided
        user = db.query(User).filter(User.email == email).first()
        if not user:
            db.add(User(email=email, access_token=access_token, provider='github'))
            db.commit()
        
        return {"access_token": access_token}
    else:
        raise HTTPException(status_code=response.status_code, detail="Failed to obtain access token")
