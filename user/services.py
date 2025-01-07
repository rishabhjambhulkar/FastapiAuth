from user.models import UserModel
from fastapi.exceptions import HTTPException
from core.security import get_password_hash
from sqlalchemy.orm import Session
from datetime import datetime

class UserService:
    def __init__(self, db: Session):
        self.db = db

    async def create_account(self, data):
        # Check if the email is already registered
        user = self.db.query(UserModel).filter(UserModel.email == data.email).first()
        if user:
            raise HTTPException(status_code=422, detail="Email is already registered with us.")

        # Create and save the new user
        new_user = UserModel(
            name=data.name,
            email=data.email,
            password=get_password_hash(data.password),
        )
        self.db.add(new_user)
        self.db.commit()
        self.db.refresh(new_user)
        return new_user





# from user.models import UserModel
# from fastapi.exceptions import HTTPException
# from core.security import get_password_hash
# from datetime import datetime


# async def createAccount(data, db):
#     user = db.query(UserModel).filter(UserModel.email == data.email).first()
#     if user:
#         raise HTTPException(status_code=422, detail="Email is already registered with us.")

#     new_user = UserModel(
#         name=data.name,
#         email=data.email,
#         password=get_password_hash(data.password),
#     )
#     db.add(new_user)
#     db.commit()
#     db.refresh(new_user)
#     return new_user
