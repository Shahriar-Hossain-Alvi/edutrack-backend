## Tables
1. users = id, username, email, hashed_password, is_active, role ✅
2. Department = id, dept_name ✅
3. semester = id, semester_name, semester_number ✅
4. students = id, name, registration, session, department_id, semester_id ✅
5. subject = id, subject_title, subject_code, semester_id, credits ✅
6. marks = id, student_id, subject_id, semester_id, assignmet_mark, midterm_mark, final_mark, class_test_mark, GPA, total_mark grade(GPA), user_id(teacher_id/Admin_id)
7. subject_offerings = id, subject_id, department_id, taught_by


## Relationships
Department → Students                       | 1:N  | Each department has many students           
Department ↔ Subject (via subject_offerings)| M:N  | Subjects can belong to multiple departments 
Semester → Subjects                         | 1:N  | Each semester has many subjects             
Students → Marks                            | 1:N  | Each student can have many marks            
Subject → Marks                             | 1:N  | Each subject can have many marks            
Semester → Marks                            | 1:N  | multiple marks of different subjects belongs to one semester           
Users → Students                            | 1:1  | Each student has one user account           




after creation hooks

## Folder Structure

result-processing-fastapi/
├─ alembic/
│  ├─ versions/
│  │  ├─ 16e1b50bd50a_fixed_and_refactored_all_the_sql_models.py
│  ├─ env.py
│  ├─ README
│  └─ script.py.mako
├─ app/
│  ├─ core/
│  │  ├─ __init__.py
│  │  ├─ authenticated_user.py
│  │  ├─ config.py
│  │  ├─ jwt.py
│  │  └─ pw_hash.py
│  ├─ db/
│  │  ├─ base.py
│  │  └─ db.py
│  ├─ models/
│  │  ├─ __init__.py
│  │  ├─ department_model.py
│  │  ├─ mark_model.py
│  │  ├─ semester_model.py
│  │  ├─ student_model.py
│  │  ├─ subject_model.py
│  │  ├─ subject_offerings_model.py
│  │  └─ user_model.py
│  ├─ permissions/
│  │  ├─ demo_permission.py
│  │  └─ role_checks.py
│  ├─ routes/
│  │  ├─ department_routes.py
│  │  ├─ login.py
│  │  ├─ semester_routes.py
│  │  ├─ student_routes.py
│  │  ├─ subject_routes.py
│  │  └─ user_routes.py
│  ├─ schemas/
│  │  ├─ department_schema.py
│  │  ├─ jwt_schema.py
│  │  ├─ semester_schema.py
│  │  ├─ student_schema.py
│  │  ├─ subject_offering_schema.py
│  │  ├─ subject_schema.py
│  │  └─ user_schema.py
│  ├─ services/
│  │  ├─ department_service.py
│  │  ├─ semester_service.py
│  │  ├─ student_service.py
│  │  ├─ subject_offering_service.py
│  │  ├─ subject_service.py
│  │  ├─ user_login.py
│  │  └─ user_service.py
│  └─ main.py
├─ .env
├─ .env.example
├─ .gitignore
├─ alembic.ini
├─ create.md
├─ planning.md
├─ readme.md
└─ requirements.txt
