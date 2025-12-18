from pydantic import BaseModel, ConfigDict
from datetime import datetime
from app.schemas.user_schema import UserOutSchema


class TeacherBaseSchema(BaseModel):
    name: str
    department_id: int
    user_id: int
    present_address: str = ""
    permanent_address: str = ""
    date_of_birth: datetime | None = None
    mobile_number: str = ""
    photo_url: str = ""


class TeacherCreateSchema(TeacherBaseSchema):
    pass


class TeacherResponseSchema(TeacherBaseSchema):
    id: int
    model_config = ConfigDict(from_attributes=True)


class TeacherResponseSchemaNested(TeacherResponseSchema):
    id: int
    user: UserOutSchema
    model_config = ConfigDict(from_attributes=True)


# TODO: Add teacher update schema
