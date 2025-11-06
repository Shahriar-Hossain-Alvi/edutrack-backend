from app.db.base import Base
from sqlalchemy.orm import mapped_column, Mapped, relationship
from sqlalchemy import Integer, String, Float, ForeignKey


class Mark(Base):
    __tablename__ = "marks"


    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)

    assignment_mark: Mapped[float | None] = mapped_column(Float, default=0.0)

    midterm_mark: Mapped[float | None] = mapped_column(Float, default=0.0)
    
    class_test_mark: Mapped[float | None] = mapped_column(Float, default=0.0)
    
    final_exam_mark: Mapped[float | None] = mapped_column(Float, default=0.0)

    total_mark: Mapped[float | None] = mapped_column(Float, default=0.0)

    GPA: Mapped[float | None] = mapped_column(String(5), default=0.0)


    # relationship with student
    student_id: Mapped[int] = mapped_column(Integer, ForeignKey("students.id", ondelete="CASCADE"))

    student: Mapped["Student"] = relationship(back_populates="marks") #type: ignore 


    # relationship with subject
    subject_id: Mapped[int] = mapped_column(Integer, ForeignKey("subjects.id", ondelete="CASCADE"))

    subject: Mapped["Subject"] = relationship(back_populates="marks") #type: ignore 


    # relationship with semester
    semester_id: Mapped[int] = mapped_column(Integer, ForeignKey("semesters.id", ondelete="CASCADE"))

    semester: Mapped["Semester"] = relationship(back_populates="marks") #type: ignore 
    
