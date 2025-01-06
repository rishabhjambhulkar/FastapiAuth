from passlib.context import CryptContext
from starlette.authentication import AuthCredentials, UnauthenticatedUser
from datetime import timedelta, datetime, timezone
from jose import jwt, JWTError
from core.config import get_settings
from fastapi import Depends
from core.db import getDb
from user.models import UserModel

settings = get_settings()

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_password_hash(password):
    return pwd_context.hash(password)

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


async def create_access_token(data,  expiry: timedelta):
    payload = data.copy()
    expire_in = datetime.utcnow() + expiry
    payload.update({"exp": expire_in})
    return jwt.encode(payload, settings.JWT_SECRET, algorithm=settings.JWT_ALGORITHM)


async def create_refresh_token(data,expiry: timedelta):
    
    payload = data.copy()
    expire_in = datetime.utcnow() + expiry
    payload.update({"exp": expire_in})
    return jwt.encode(payload, settings.JWT_SECRET, algorithm=settings.JWT_ALGORITHM)


def get_token_payload(token):
    try:
        payload = jwt.decode(token, settings.JWT_SECRET, algorithms=[settings.JWT_ALGORITHM])
    except JWTError:
        return None
    return payload



def get_current_user(token: str, db=None):
    payload = get_token_payload(token)
    print("payload: ", payload)
    if not payload or type(payload) is not dict:
        return None
    print("Current user", payload)
   
    exp = payload.get('exp', None)
    print('exp',exp)
    if exp:
       
        exp_time = datetime.fromtimestamp(exp, tz=timezone.utc)
        if datetime.now(timezone.utc) > exp_time:
            return None

    user_id = payload.get('id', None)
    if not user_id:
        return None

    if not db:
        db = next(getDb())

    user = db.query(UserModel).filter(UserModel.id == user_id).first()
    return user




class JWTAuth:
    
    async def authenticate(self, conn):
        guest = AuthCredentials(['unauthenticated']), UnauthenticatedUser()
        
        if 'authorization' not in conn.headers:
            return guest
        
        token = conn.headers.get('authorization').split(' ')[1]  # Bearer token_hash
        if not token:
            return guest
        
        user = get_current_user(token=token)
        
        if not user:
            return guest
        
        return AuthCredentials('authenticated'), user