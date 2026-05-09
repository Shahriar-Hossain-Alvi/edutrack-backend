from pydantic import BaseModel, ConfigDict
from datetime import date, datetime

from app.models.audit_log_model import LogLevel


class AllTablesDataCount(BaseModel):
    users: int
    admins: int
    teachers: int
    students: int
    departments: int
    semesters: int
    subjects: int
    assigned_courses: int
    marks: int
    model_config = ConfigDict(from_attributes=True)


class PieChartBaseSchema(BaseModel):
    labels: list
    values: list


class PieChartResponseSchema(BaseModel):
    student_pie_chart_data: PieChartBaseSchema
    teacher_pie_chart_data: PieChartBaseSchema

    model_config = ConfigDict(from_attributes=True)


class AuditLogsResponseSchema(BaseModel):
    id: int
    action: str
    created_by: int | None = None
    action: str
    level: LogLevel = LogLevel.INFO
    path: str
    details: str | None = None
    created_at: datetime
    method: str
    ip_address: str | None = None
    payload: dict | None = None
    updated_at: datetime | None = None

    model_config = ConfigDict(from_attributes=True)
