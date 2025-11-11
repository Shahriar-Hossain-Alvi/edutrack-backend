from sqlalchemy.orm import DeclarativeBase

# declarative base. It will be used to create tables for models
class Base(DeclarativeBase):
    pass

# import models here so that alembic can find them
# from app.models import Department, Semester, Subject, Student, Mark, User, SubjectOfferings