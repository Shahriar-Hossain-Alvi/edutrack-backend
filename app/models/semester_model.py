from app.db.base import Base
from sqlalchemy.orm import mapped_column, Mapped, relationship
from sqlalchemy import Integer, String


class Semester(Base):
    __tablename__ = "semesters"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)

    semester_name: Mapped[str] = mapped_column(String(50), nullable=False, unique=True)

    semester_number: Mapped[int] = mapped_column(Integer, nullable=False, unique=True)


    # Relationships

    # many subjects can belong to one semester
    subjects: Mapped[list["Subject"]] = relationship(back_populates="semester") #type: ignore 

    # many students can belong to one semester
    students: Mapped[list["Student"]] = relationship(back_populates="semester") #type: ignore 

    # many marks can belong to one semester
    marks: Mapped[list["Mark"]] = relationship(back_populates="semester") #type: ignore 