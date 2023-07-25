# import uuid
# import bcrypt
# import datetime
# from typing import List, Optional
# from pydantic import EmailStr
# from sqlmodel import Field, Relationship, SQLModel
# from sqlalchemy import UniqueConstraint
# from app.models.base_model import BaseModel


# class LoginUser(SQLModel):
#     name: str
#     email: EmailStr


# class UserDetail(LoginUser):
#     id: uuid.UUID
#     name: str
#     is_active: bool = True
#     is_staff: bool = False
#     is_superuser: bool = False
#     is_verified: bool = False
#     last_login: datetime.datetime = None
#     def __str__(self):
#         return self.name


# class User(BaseModel, UserDetail, table=True):
#     __tablename__ = "users"
#     __table_args__ = (UniqueConstraint("email"),)
#     accounts: List[Account] = Relationship(
#         link_model=AccountUser,
#         back_populates='users'
#     )

#     def __init__(self, name, email, password):
#         self.name = name
#         self.email = email
#         self.password = self.hash_password(password)

#     def set_password(self, password):
#         self.password = self.hash_password(password)

#     @classmethod
#     def hash_password(cls, password: str) -> str:
#         salt = bcrypt.gensalt()
#         hashed_password = bcrypt.hashpw(password.encode("utf-8"), salt)
#         return hashed_password.decode("utf-8")

#     @classmethod
#     def verify_password(cls, plain_password: str, hashed_password: str) -> bool:
#         return bcrypt.checkpw(plain_password.encode("utf-8"), hashed_password.encode("utf-8"))


# class UserList(UserDetail):
#     roles: List[ListRole]


from .base_model import BaseModel
from enum import Enum
from datetime import datetime
from sqlmodel import Field

class Status(str, Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"


class Store_Status(BaseModel, table=True):
    store_id: str = Field(index=True)
    status: Status
    timestamp_utc: datetime



















