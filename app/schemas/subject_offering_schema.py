from pydantic import BaseModel, ConfigDict


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

    model_config = ConfigDict(from_attributes=True)