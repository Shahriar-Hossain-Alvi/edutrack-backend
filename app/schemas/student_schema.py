from pydantic import BaseModel, ConfigDict
from datetime import datetime

from pydantic_partial import create_partial_model
from app.schemas.user_schema import UserCreateSchema, UserOutSchema


class StudentBaseSchema(BaseModel):
    name: str
    registration: str
    session: str
    department_id: int
    semester_id: int
    # user_id: int # Don't need this because user and student will be created in same service function
    present_address: str = ""
    permanent_address: str = ""
    date_of_birth: datetime | None = None
    mobile_number: str = ""
    photo_url: str = ""
    photo_public_id: str = ""


class StudentCreateSchema(StudentBaseSchema):
    user: UserCreateSchema


class StudentOutSchema(StudentBaseSchema):
    id: int
    model_config = ConfigDict(from_attributes=True)


class StudentResponseSchemaNested(StudentBaseSchema):
    id: int
    user: UserOutSchema
    model_config = ConfigDict(from_attributes=True)


class StudentUpdateSchema(BaseModel):
    name: str | None = None
    present_address: str | None = None
    permanent_address: str | None = None
    date_of_birth: datetime | None = None
    mobile_number: str | None = None
    photo_url: str | None = None


_Partial_Student = create_partial_model(StudentBaseSchema)


class StudentUpdateByAdminSchema(_Partial_Student):
    pass
