from datetime import datetime
from pydantic import BaseModel, ConfigDict
from app.schemas.subject_schema import SubjectBaseSchema


class SubjectOfferingBase(BaseModel):
    taught_by_id: int
    subject_id: int
    department_id: int


class SubjectOfferingCreateSchema(SubjectOfferingBase):
    pass


class SubjectOfferingUpdateSchema(BaseModel):
    taught_by_id: int | None = None
    subject_id: int | None = None
    department_id: int | None = None


class SubjectOfferingResponseSchema(SubjectOfferingBase):
    id: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
