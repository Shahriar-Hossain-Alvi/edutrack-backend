from app.db.base import Base
from sqlalchemy.orm import mapped_column, Mapped, relationship
from sqlalchemy import Integer, String, ForeignKey

class Student(Base):
    __tablename__ = "students"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)

    name: Mapped[str] = mapped_column(String(100), nullable=False)

    registration: Mapped[str] = mapped_column(String(100), nullable=False, unique=True)

    session: Mapped[str] = mapped_column(String(50), nullable=False)

    # Relationship with Department
    department_id: Mapped[int] = mapped_column(Integer, ForeignKey("departments.id", ondelete="SET NULL")) # set null if department is deleted

    department:Mapped["Department"] = relationship(back_populates="students") #type: ignore 


    # Relationship with semester
    semester_id: Mapped[int] = mapped_column(Integer, ForeignKey("semesters.id", ondelete="SET NULL")) # set null if department is deleted

    # each student has one semester (current semester)
    semester:Mapped["Semester"] = relationship(back_populates="students") #type: ignore 


    # Relationship with user
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id", ondelete="CASCADE")) # delete student record if user is deleted

    user:Mapped["User"] = relationship(back_populates="student") #type: ignore 


    # relationship with marks
    # one student can have many marks
    marks: Mapped[list["Mark"]] = relationship(back_populates="student") #type: ignore 