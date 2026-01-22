from datetime import datetime
from pydantic import BaseModel, ConfigDict
from app.schemas.subject_schema import SubjectBaseSchema


class SubjectOfferingBase(BaseModel):
    taught_by_id: int
    subject_id: int
    department_id: int

#  used in create_new_subject_offering router function


class SubjectOfferingCreateSchema(SubjectOfferingBase):
    pass


# used in update_subject_offering router function (admin, super admin)
class SubjectOfferingUpdateSchema(BaseModel):
    taught_by_id: int | None = None
    subject_id: int | None = None
    department_id: int | None = None


# Get All Subject Offerings: below schemas are used in get_all_subject_offerings router function
class SubjectOfferingDepartmentResponseSchema(BaseModel):
    id: int
    department_name: str
    model_config = ConfigDict(from_attributes=True)


class SubjectOfferingSemesterResponseSchema(BaseModel):
    id: int
    semester_name: str
    model_config = ConfigDict(from_attributes=True)


class SubjectOfferingSubjectResponseSchema(BaseModel):
    id: int
    subject_title: str
    subject_code: str
    credits: float
    is_general: bool
    semester: SubjectOfferingSemesterResponseSchema
    model_config = ConfigDict(from_attributes=True)


class SubjectOfferingTaughtByResponseSchema(BaseModel):
    id: int
    name: str
    department_id: int
    department: SubjectOfferingDepartmentResponseSchema

    model_config = ConfigDict(from_attributes=True)


class AllSubjectOfferingsResponseSchema(BaseModel):
    id: int
    taught_by_id: int | None
    subject_id: int
    department_id: int
    created_at: datetime
    updated_at: datetime
    taught_by: SubjectOfferingTaughtByResponseSchema | None
    department: SubjectOfferingDepartmentResponseSchema
    subject: SubjectOfferingSubjectResponseSchema

    model_config = ConfigDict(from_attributes=True)


# Get all offerered subject based on students current semester, department and teachers id: below schemas are used in get_offered_subject_lists_for_marking router function
class SubjectOfferingForMarkingTaughtByResponseSchema(BaseModel):
    id: int
    name: str
    department_id: int

    model_config = ConfigDict(from_attributes=True)


class SubjectOfferingForMarkingSubjectResponseSchema(BaseModel):
    id: int
    semester_id: int
    subject_title: str
    subject_code: str
    semester: SubjectOfferingSemesterResponseSchema
    model_config = ConfigDict(from_attributes=True)


class SubjectOfferingListForMarkingResponseSchema(BaseModel):
    id: int
    taught_by_id: int | None
    taught_by: SubjectOfferingForMarkingTaughtByResponseSchema | None

    subject_id: int
    subject: SubjectOfferingForMarkingSubjectResponseSchema

    department_id: int
    department: SubjectOfferingDepartmentResponseSchema

    model_config = ConfigDict(from_attributes=True)

    """
      {
    "id": 18,
    "taught_by_id": 7,
    "taught_by": {
      "id": 7,
      "name": "Dr. Ariful Islam",
      "department_id": 2,
    },

    "subject_id": 9,

    "department_id": 2,
    "department": {
      "id": 2,
      "department_name": "cse - computer science & engineering",
    },

    "subject": {
      "id": 9,
      "semester_id": 2,
      "subject_title": "Structured Programming",
      "subject_code": "CSE-1101",
      "semester": {
        "id": 2,
        "semester_name": "first",
        "semester_number": 1
      }
    }
  },
    """
