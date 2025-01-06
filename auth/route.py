from fastapi import APIRouter, status, Depends, Header, Response
from sqlalchemy.orm import Session
from core.db import getDb
from auth.services import get_token, get_refresh_token
from user.schemas import LoginRequest
from fastapi.exceptions import HTTPException

router = APIRouter(
    prefix="/auth",
    tags=["Auth"],
    responses={404: {"description": "Not found"}},
)

async def set_tokens_in_cookies(response: Response, access_token: str, refresh_token: str, access_token_expires_in: int):
    # Set access token cookie
    response.set_cookie(
        key="access_token",
        value=access_token,
        httponly=True,
        expires=access_token_expires_in  # Set the expiration time using access_token_expires_in
    )
    # Set refresh token cookie
    response.set_cookie(
        key="refresh_token",
        value=refresh_token,
        httponly=True
    )
    return response

@router.post("/login", status_code=status.HTTP_200_OK)
async def authenticate_user(data: LoginRequest,response: Response, db: Session = Depends(getDb)):
    # Pass data to the get_token function
    token = await get_token(data=data, db=db)
    if not token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid email or password")
    print("Setting Access Token Cookie:", token.access_token)
    print("Setting Refresh Token Cookie:", token.refresh_token)

   
    response.set_cookie(
        key="access_token",
        value=token.access_token,
        httponly=True,
        expires=token.expires_in
    )
    response.set_cookie(
        key="refresh_token",
        value=token.refresh_token,
        httponly=True
    )

    return {
        "token": token
    }



@router.post("/refresh", status_code=status.HTTP_200_OK)
async def refresh_access_token(response: Response,refresh_token: str = Header(), db: Session = Depends(getDb)):
     
    token = await get_refresh_token(token=refresh_token, db=db)
    if not token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid email or password")
    print("Setting Access Token Cookie:", token.access_token)
    print("Setting Refresh Token Cookie:", token.refresh_token)

   
    response.set_cookie(
        key="access_token",
        value=token.access_token,
        httponly=True,
        expires=token.expires_in
    )
    response.set_cookie(
        key="refresh_token",
        value=token.refresh_token,
        httponly=True
    )

    return {
        "token": token
    }


