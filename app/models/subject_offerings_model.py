from app.db.base import Base
from sqlalchemy.orm import mapped_column, Mapped, relationship
from sqlalchemy import Integer, ForeignKey


class SubjectOfferings(Base):
    __tablename__ = "subject_offerings"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)

    # relationship with subject
    subject_id: Mapped[int] = mapped_column(Integer, ForeignKey("subjects.id", ondelete="CASCADE"))

    subject: Mapped["Subject"] = relationship(back_populates="subject_offerings") #type: ignore 

   
   
    # relationship with department
    department_id: Mapped[int] = mapped_column(Integer, ForeignKey("departments.id", ondelete="CASCADE"))

    department: Mapped["Department"] = relationship(back_populates="subject_offerings") #type: ignore 