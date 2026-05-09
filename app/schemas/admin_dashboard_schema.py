from pydantic import BaseModel, ConfigDict


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
