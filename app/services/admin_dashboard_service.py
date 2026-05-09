from typing import Any
from loguru import logger
from sqlalchemy import func, or_, select
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.exceptions import DomainIntegrityError
from app.core.integrity_error_parser import parse_integrity_error
from app.models import User
from app.models import Department, Mark, Semester, Student, Subject, SubjectOfferings, Teacher
from sqlalchemy.exc import IntegrityError
from fastapi import Request
import re

from app.models.audit_log_model import AuditLog


class AdminDashboardService:

    @staticmethod
    async def get_all_table_data_count(
        db: AsyncSession,
        request: Request | None = None
    ):

        try:
            # 1. Build a single query that wraps multiple subqueries
            query = select(
                select(func.count(User.id)).scalar_subquery().label("users"),
                select(func.count(User.id)).where(User.role.in_(
                    ["admin", "super_admin"])).scalar_subquery().label("admins"),
                select(func.count(Teacher.id)
                       ).scalar_subquery().label("teachers"),
                select(func.count(Student.id)
                       ).scalar_subquery().label("students"),
                select(func.count(Department.id)
                       ).scalar_subquery().label("departments"),
                select(func.count(Semester.id)
                       ).scalar_subquery().label("semesters"),
                select(func.count(Subject.id)
                       ).scalar_subquery().label("subjects"),
                select(func.count(SubjectOfferings.id)
                       ).scalar_subquery().label("assigned_courses"),
                select(func.count(Mark.id)).scalar_subquery().label("marks")
            )

            # 2. Execute the query
            result = await db.execute(query)

            # 3. Fetch the first row
            row = result.fetchone()

            # 4. Critical Check: If row is None, return zeros instead of crashing
            if row is None:
                return {k: 0 for k in ["users", "admins", "teachers", "students", "departments", "semesters", "subjects", "assigned_courses", "marks"]}

            # 5. Return the mapped data
            return {
                "users": row.users,
                "admins": row.admins,
                "teachers": row.teachers,
                "students": row.students,
                "departments": row.departments,
                "semesters": row.semesters,
                "subjects": row.subjects,
                "assigned_courses": row.assigned_courses,
                "marks": row.marks
            }
        except IntegrityError as e:
            # Important: rollback as soon as an error occurs. It recovers the session from 'failed' state and puts it back in 'clean' state to save the Audit Log
            await db.rollback()

            # generally the PostgreSQL's error message will be in e.orig.args
            raw_error_message = str(e.orig) if e.orig else str(e)
            readable_error = parse_integrity_error(raw_error_message)

            logger.error(f"Integrity error while getting all table count: {e}")
            logger.error(f"Readable Error: {readable_error}")

            # attach audit payload safely
            if request:
                payload: dict[str, Any] = {
                    "raw_error": raw_error_message,
                    "readable_error": readable_error,
                }

                request.state.audit_payload = payload

            raise DomainIntegrityError(
                error_message=readable_error, raw_error=raw_error_message
            )

    @staticmethod
    def format_chart_data(pie_chart_data):
        formatted_labels = []

        for item in pie_chart_data:
            raw_name = item["department_name"]
            parts = re.split(r'[-–—:]', raw_name)

            abbr = parts[0].strip().upper()
            formatted_labels.append(abbr)

        return {
            "labels": formatted_labels,
            "values": [item["count"] for item in pie_chart_data]
        }

    @staticmethod
    async def get_chart_data(
        db: AsyncSession,
        request: Request | None = None
    ):

        try:
            # Get department names with count of students
            query = select(
                Department.department_name,
                func.count(Student.id)).join(Student, Department.id == Student.department_id).group_by(Department.department_name)

            # Execute the query
            result = await db.execute(query)

            pie_chart_data = result.mappings().all()

            # group departments in an array and counts in another array
            student_pie_chart_data = AdminDashboardService.format_chart_data(
                pie_chart_data)

            # Get department names with count of students
            query = select(
                Department.department_name,
                func.count(Teacher.id)).join(Teacher, Department.id == Teacher.department_id).group_by(Department.department_name)

            # Execute the query
            result = await db.execute(query)

            pie_chart_data = result.mappings().all()

            # group departments in an array and counts in another array
            teacher_pie_chart_data = AdminDashboardService.format_chart_data(
                pie_chart_data)

            return {
                "student_pie_chart_data": student_pie_chart_data,
                "teacher_pie_chart_data": teacher_pie_chart_data
            }

        except IntegrityError as e:
            # Important: rollback as soon as an error occurs. It recovers the session from 'failed' state and puts it back in 'clean' state to save the Audit Log
            await db.rollback()

            # generally the PostgreSQL's error message will be in e.orig.args
            raw_error_message = str(e.orig) if e.orig else str(e)
            readable_error = parse_integrity_error(raw_error_message)

            logger.error(f"Integrity error while getting all table count: {e}")
            logger.error(f"Readable Error: {readable_error}")

            # attach audit payload safely
            if request:
                payload: dict[str, Any] = {
                    "raw_error": raw_error_message,
                    "readable_error": readable_error,
                }

                request.state.audit_payload = payload

            raise DomainIntegrityError(
                error_message=readable_error, raw_error=raw_error_message
            )

    # get audit log
    @staticmethod
    async def get_recent_audit_logs(
        db: AsyncSession,
        request: Request | None = None
    ):

        try:
            # Get department names with count of students
            query = select(AuditLog)

            # Execute the query
            result = await db.execute(query)

            pie_chart_data = result.mappings().all()

            # group departments in an array and counts in another array
            student_pie_chart_data = AdminDashboardService.format_chart_data(
                pie_chart_data)

            # Get department names with count of students
            query = select(
                Department.department_name,
                func.count(Teacher.id)).join(Teacher, Department.id == Teacher.department_id).group_by(Department.department_name)

            # Execute the query
            result = await db.execute(query)

            pie_chart_data = result.mappings().all()

            # group departments in an array and counts in another array
            teacher_pie_chart_data = AdminDashboardService.format_chart_data(
                pie_chart_data)

            return {
                "student_pie_chart_data": student_pie_chart_data,
                "teacher_pie_chart_data": teacher_pie_chart_data
            }

        except IntegrityError as e:
            # Important: rollback as soon as an error occurs. It recovers the session from 'failed' state and puts it back in 'clean' state to save the Audit Log
            await db.rollback()

            # generally the PostgreSQL's error message will be in e.orig.args
            raw_error_message = str(e.orig) if e.orig else str(e)
            readable_error = parse_integrity_error(raw_error_message)

            logger.error(f"Integrity error while getting all table count: {e}")
            logger.error(f"Readable Error: {readable_error}")

            # attach audit payload safely
            if request:
                payload: dict[str, Any] = {
                    "raw_error": raw_error_message,
                    "readable_error": readable_error,
                }

                request.state.audit_payload = payload

            raise DomainIntegrityError(
                error_message=readable_error, raw_error=raw_error_message
            )
