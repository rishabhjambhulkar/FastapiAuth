from fastapi import APIRouter, status, Depends, Header, Response
from sqlalchemy.orm import Session
from core.db import getDb
from auth.services import AuthService
from user.schemas import LoginRequest
from fastapi.exceptions import HTTPException
from core.config import get_settings

# Initialize the settings and AuthService instance
settings = get_settings()
auth_service = AuthService(settings=settings)

router = APIRouter(
    prefix="/auth",
    tags=["Auth"],
    responses={404: {"description": "Not found"}},
)

def set_cookies(response: Response, access_token: str, refresh_token: str, expires_in: int):
    response.set_cookie(
        key="access_token",
        value=access_token,
        httponly=True,
        expires=expires_in,
    )
    response.set_cookie(
        key="refresh_token",
        value=refresh_token,
        httponly=True,
    )

@router.post("/login", status_code=status.HTTP_200_OK)
async def authenticate_user(data: LoginRequest, response: Response, db: Session = Depends(getDb)):
    # Use AuthService to get the token
    token = await auth_service.get_token(data=data, db=db)
    if not token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid email or password")

    print("Setting Access Token Cookie:", token.access_token)
    print("Setting Refresh Token Cookie:", token.refresh_token)

    # Use the utility function to set cookies
    set_cookies(response, access_token=token.access_token, refresh_token=token.refresh_token, expires_in=token.expires_in)

    return {"token": token}

@router.post("/refresh", status_code=status.HTTP_200_OK)
async def refresh_access_token(response: Response, refresh_token: str = Header(), db: Session = Depends(getDb)):
    # Use AuthService to refresh the token
    token = await auth_service.get_refresh_token(token=refresh_token, db=db)
    if not token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid refresh token")

    print("Setting Access Token Cookie:", token.access_token)
    print("Setting Refresh Token Cookie:", token.refresh_token)

    # Use the utility function to set cookies
    set_cookies(response, access_token=token.access_token, refresh_token=token.refresh_token, expires_in=token.expires_in)

    return {"token": token}










# from fastapi import APIRouter, status, Depends, Header, Response
# from sqlalchemy.orm import Session
# from core.db import getDb
# from auth.services import get_token, get_refresh_token
# from user.schemas import LoginRequest
# from fastapi.exceptions import HTTPException

# router = APIRouter(
#     prefix="/auth",
#     tags=["Auth"],
#     responses={404: {"description": "Not found"}},
# )

# def set_cookies(response: Response, access_token: str, refresh_token: str, expires_in: int):
 
#     response.set_cookie(
#         key="access_token",
#         value=access_token,
#         httponly=True,
#         expires=expires_in
#     )
#     response.set_cookie(
#         key="refresh_token",
#         value=refresh_token,
#         httponly=True
#     )



# @router.post("/login", status_code=status.HTTP_200_OK)
# async def authenticate_user(data: LoginRequest, response: Response, db: Session = Depends(getDb)):
#     token = await get_token(data=data, db=db)
#     if not token:
#         raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid email or password")

#     print("Setting Access Token Cookie:", token.access_token)
#     print("Setting Refresh Token Cookie:", token.refresh_token)

#     # Use the utility function to set cookies
#     set_cookies(response, access_token=token.access_token, refresh_token=token.refresh_token, expires_in=token.expires_in)

#     return {"token": token}

# @router.post("/refresh", status_code=status.HTTP_200_OK)
# async def refresh_access_token(response: Response, refresh_token: str = Header(), db: Session = Depends(getDb)):
#     token = await get_refresh_token(token=refresh_token, db=db)
#     if not token:
#         raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid refresh token")

#     print("Setting Access Token Cookie:", token.access_token)
#     print("Setting Refresh Token Cookie:", token.refresh_token)

#     # Use the utility function to set cookies
#     set_cookies(response, access_token=token.access_token, refresh_token=token.refresh_token, expires_in=token.expires_in)

#     return {"token": token}


