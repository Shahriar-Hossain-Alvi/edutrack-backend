from app.db.base import Base
from sqlalchemy.orm import mapped_column, Mapped, relationship
from sqlalchemy import Integer, String

# Department = id, name


class Department(Base):
    __tablename__ = "departments"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)

    department_name: Mapped[str] = mapped_column(
        String(100), nullable=False, unique=True)

    # Relationships
    students: Mapped[list["Student"]] = relationship(  # type: ignore
        back_populates="department")

    teachers: Mapped[list["Teacher"]] = relationship(  # type: ignore
        back_populates="department")

    # many subjects can belong to many department
    subject_offerings: Mapped[list["SubjectOfferings"]] = relationship(  # type: ignore
        "SubjectOfferings", back_populates="department")
