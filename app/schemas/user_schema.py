from pydantic import BaseModel, ConfigDict, EmailStr
from app.models import UserRole


class UserCreateSchema(BaseModel):
    username: EmailStr
    email: EmailStr
    password: str
    role: UserRole


class UserOutSchema(BaseModel):
    id: int
    username: EmailStr
    email: EmailStr
    role: UserRole

    model_config = ConfigDict(from_attributes=True)
    # this is required for response models. 
    # pydantic expects DICTs or JSON but sqlalchemy returns objects.
    # So, from_attributes = True tells  pydantic to look for attributes on the source object (like user_object.id, user_object.username) rather than dictionary keys.
    # This allows the UserOutSchema to be initialized directly from a SQLAlchemy without having to convert it to a dictionary or throw an error