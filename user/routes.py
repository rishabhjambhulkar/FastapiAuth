from fastapi import APIRouter, status, Depends, Header, HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from core.db import getDb
from user.schemas import CreateUserRequest
from user.services import UserService
from core.security import get_current_user

router = APIRouter(
    prefix="/users",
    tags=["Users"],
    responses={404: {"description": "Not found"}},
)

@router.post("", status_code=status.HTTP_201_CREATED)
async def create_user(data: CreateUserRequest, db: Session = Depends(getDb)):
    """
    Creates a new user account.
    """
    try:
        user_service = UserService(db=db)
        await user_service.create_account(data=data)
        return JSONResponse(
            content={"message": "User account has been successfully created."},
            status_code=status.HTTP_201_CREATED,
        )
    except HTTPException as e:
        # Forward any HTTP exceptions
        raise e
    except Exception as e:
        # Handle unexpected errors
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e),
        )

@router.post("/details", status_code=status.HTTP_200_OK)
async def get_user_detail(access_token: str = Header(), db: Session = Depends(getDb)):
    """
    Retrieves the details of the currently authenticated user.
    """
    user = get_current_user(token=access_token, db=db)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid access token.",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return {"user": user}










# from fastapi import APIRouter, status, Depends, Request, Header
# from fastapi.responses import JSONResponse
# from sqlalchemy.orm import Session
# from core.db import getDb
# from user.schemas import CreateUserRequest
# from user.services import createAccount
# from user.responses import UserResponse;
# from core.security import get_current_user
# from fastapi.exceptions import HTTPException

# router = APIRouter(
#     prefix="/users",
#     tags=["Users"],
#     responses={404: {"description": "Not found"}},
# )


# @router.post('', status_code=status.HTTP_201_CREATED)
# async def create_user(data: CreateUserRequest, db: Session = Depends(getDb)):
#     pass
#     await createAccount(data=data, db=db)
#     payload = {"message": "User account has been succesfully created."}
#     return JSONResponse(content=payload)



# @router.post('/details', status_code=status.HTTP_200_OK)
# async def get_user_detail(access_token: str = Header(), db: Session = Depends(getDb)):
#     user = get_current_user(token=access_token, db=db)
    
#     if not user:
#         raise HTTPException(
#             status_code=401,
#             detail="Invalid access token.",
#             headers={"WWW-Authenticate": "Bearer"},
#         )
    
#     return user