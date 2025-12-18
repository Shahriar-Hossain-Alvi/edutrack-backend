from app.db.base import Base
from sqlalchemy.orm import mapped_column, Mapped, relationship
from sqlalchemy import Integer, ForeignKey


class SubjectOfferings(Base):
    __tablename__ = "subject_offerings"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)

    # TODO: use teacher_id from teachers table

    # relationship with user(teacher)
    taught_by_id: Mapped[int | None] = mapped_column(
        Integer, ForeignKey("users.id", ondelete="SET NULL"))

    taught_by: Mapped["User"] = relationship(  # type: ignore
        back_populates="subject_offerings")

    # relationship with subject
    subject_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("subjects.id", ondelete="CASCADE"))

    subject: Mapped["Subject"] = relationship(  # type: ignore
        back_populates="subject_offerings")

    # relationship with department
    department_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("departments.id", ondelete="CASCADE"))

    department: Mapped["Department"] = relationship(  # type: ignore
        back_populates="subject_offerings")
