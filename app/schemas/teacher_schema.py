from pydantic import BaseModel, ConfigDict
from datetime import date, datetime
from app.schemas.user_schema import UserCreateSchema, UserOutSchema
from pydantic_partial import create_partial_model


class TeacherBaseSchema(BaseModel):
    name: str
    department_id: int | None = None
    # user_id: int # Don't need this because user and teacher will be created in same service function
    present_address: str = ""
    permanent_address: str = ""
    date_of_birth: date | None = None
    photo_url: str = ""
    photo_public_id: str = ""


# used in create_teacher_record router function
class TeacherCreateSchema(TeacherBaseSchema):
    user: UserCreateSchema


# currently not needed
# class TeacherResponseSchema(TeacherBaseSchema):
#     id: int
#     created_at: datetime
#     updated_at: datetime
#     user_id: int
#     model_config = ConfigDict(from_attributes=True)

# currently not needed
# class TeacherResponseSchemaNested(TeacherResponseSchema):
#     id: int
#     user: UserOutSchema
#     model_config = ConfigDict(from_attributes=True)


# used in get_all_teachers_with_minimal_data for subject offering
class DepartmentDataForMinimalTeacher(BaseModel):
    id: int
    department_name: str
    model_config = ConfigDict(from_attributes=True)


# used in get_all_teachers_with_minimal_data for subject offering
class TeacherResponseSchemaForSubjectOfferingSearch(BaseModel):
    id: int
    name: str
    department_id: int | None
    department: DepartmentDataForMinimalTeacher | None

    model_config = ConfigDict(from_attributes=True)


class TeacherProfileResponseSchemaNested(TeacherBaseSchema):
    id: int
    created_at: datetime
    updated_at: datetime
    user: UserOutSchema
    department: DepartmentDataForMinimalTeacher | None
    model_config = ConfigDict(from_attributes=True)


class TeacherProfileResponseSchemaWithCourseCount(BaseModel):
    user_data: TeacherProfileResponseSchemaNested
    total_assigned_courses: int


class TeachersPublicDataResponse(BaseModel):
    name: str
    photo_url: str
    model_config = ConfigDict(from_attributes=True)


# used in update_teacher_by_admin router function
# 1. dynamic partial base beacuse directly using create_partial_model is giving warning in service functions parameter
_PartialTeacher = create_partial_model(TeacherBaseSchema)


class TeacherUpdateByAdminSchema(_PartialTeacher):
    pass
