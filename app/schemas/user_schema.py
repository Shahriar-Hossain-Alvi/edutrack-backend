from pydantic import BaseModel, ConfigDict, EmailStr
from app.models import UserRole


class UserBaseSchema(BaseModel):
    username: EmailStr = "student1@gmail.com"
    email: EmailStr = "student1@gmail.com"
    role: UserRole = UserRole.STUDENT
    is_active: bool = True


class UserCreateSchema(UserBaseSchema):
    password: str = "123456"


class UserUpdateSchemaByAdmin(BaseModel):
    role: UserRole | None = None
    email: EmailStr | None = None
    username: EmailStr | None = None
    is_active: bool | None = None

class UserUpdateSchemaByUser(BaseModel):
    password: str


class UserOutSchema(UserBaseSchema):
    id: int

    model_config = ConfigDict(from_attributes=True)
    # this is required for response models. 
    # pydantic expects DICTs or JSON but sqlalchemy returns objects.
    # So, from_attributes = True tells  pydantic to look for attributes on the source object (like user_object.id, user_object.username) rather than dictionary keys.
    # This allows the UserOutSchema to be initialized directly from a SQLAlchemy without having to convert it to a dictionary or throw an error