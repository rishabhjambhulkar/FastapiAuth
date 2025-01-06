from user.models import UserModel
from fastapi.exceptions import HTTPException
from core.security import verify_password
from core.config import get_settings
from datetime import timedelta
from auth.responses import TokenResponse
from core.security import create_access_token, create_refresh_token, get_token_payload

settings = get_settings()

async def get_token(data, db):
    user = db.query(UserModel).filter(UserModel.email == data.email).first()
    
    if not user:
        raise HTTPException(
            status_code=400,
            detail="Email is not registered with us.",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    if not verify_password(data.password, user.password):
        raise HTTPException(
            status_code=400,
            detail="Invalid Login Credentials.",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
   
    
    return await get_user_token(user=user)
    
    

async def get_refresh_token(token, db):   
    payload =  get_token_payload(token=token)
    user_id = payload.get('id', None)
    if not user_id:
        raise HTTPException(
            status_code=401,
            detail="Invalid refresh token.",
            headers={"WWW-Authenticate": "Bearer"},
        )
    user = db.query(UserModel).filter(UserModel.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=401,
            detail="Invalid refresh token.",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return await get_user_token(user=user, refresh_token=token)

    

        
        
async def get_user_token(user: UserModel, refresh_token = None):
    payload = {"id": user.id}
    
    access_token_expiry = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    
    access_token = await create_access_token(payload, access_token_expiry)
    if not refresh_token:
        refresh_token = await create_refresh_token(payload)
    return TokenResponse(
        access_token=access_token,
        refresh_token=refresh_token,
        expires_in=access_token_expiry.seconds  
    )