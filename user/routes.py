from fastapi import APIRouter, status, Depends, Request
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from core.db import getDb
from user.schemas import CreateUserRequest
from user.services import createAccount
from user.responses import UserResponse;
from auth.services import get_token, get_refresh_token
from core.security import get_current_user
from fastapi.exceptions import HTTPException

router = APIRouter(
    prefix="/users",
    tags=["Users"],
    responses={404: {"description": "Not found"}},
)


@router.post('', status_code=status.HTTP_201_CREATED)
async def create_user(data: CreateUserRequest, db: Session = Depends(getDb)):
    pass
    await createAccount(data=data, db=db)
    payload = {"message": "User account has been succesfully created."}
    return JSONResponse(content=payload)



@router.post('/details', status_code=status.HTTP_200_OK)
async def get_user_detail(token: str, db: Session = Depends(getDb)):
    user = get_current_user(token=token, db=db)
    
    if not user:
        raise HTTPException(
            status_code=401,
            detail="Invalid access token.",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    return user