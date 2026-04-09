# Result Processing System

This project generates student results. It uses **FastAPI** for the backend, **Docker** for containerization, **PostgreSQL** for the database, **SQLAlchemy** for ORM and Database models and **Alembic** for database migrations.

---

## Prerequisites

Before you begin, ensure you have the following installed on your system:

- **Docker** or **Docker Desktop**
- **Python 3.12** (this version is needed to suppress pylance and vscode warnings in editor - specifically in windows)
- **Git**

> Python is not used to run the backend — it's only needed so VSCode can provide IntelliSense and suppress import warnings.

---

# How to run this project

## 1. Clone this repository
```
windows: git clone https://github.com/Shahriar-Hossain-Alvi/edutrack-backend.git
or
Linux: git clone git@github.com:Shahriar-Hossain-Alvi/edutrack-backend.git
cd [project-folder]
```

## 2. Create a `.env` 
Copy `.env.example` -> `.env` and fill in the required values

---

## 3. Optional but Recommended: Create a Virtual Environment

This is ONLY for editor (VSCode) dependencies — Docker does not use this venv. Open a terminal and run the following commands:
```
Windows: python -m venv venv 
Linux: python3 -m venv venv    # for linux
Version specific: py -3.12 -m venv venv   # version specific venv
```

- Activate the virtual environment:
```
Windows: venv\Scripts\activate  
Linux: source venv/bin/activate 
Gitbash terminal: source venv/Scripts/activate
```

- Install dependencies locally(for editor only):
After activating the venv, run the following command in (venv) terminal:
```
pip install -r requirements.txt
```
---



# Run the Backend with Docker

## 4. Development Mode (hot reload)

Build and run the docker containers (make sure you are inside the backend project folder)
```
docker compose -f docker-compose.dev.yml up --build
```

<!-- ## 5. Production Mode -->
<!-- ``` -->
<!-- docker compose -f docker-compose.prod.yml up --build -d -->
<!-- ``` -->

---

## 6. Database Migrations (Alembic)

### Apply migrations without Docker
- When you modify the models:

Generate migration:
```
alembic revision --autogenerate -m "message"
```

- Apply migrations:
```
alembic upgrade head
```


### OR Apply migrations inside Docker (dev container) -> Best way:

- Generate Migrations (if local migration fails or directly use migration using docker container):

```
docker exec -it edutrack_backend_dev alembic revision --autogenerate -m "message"  
```

- Apply Migrations
```
docker exec -it edutrack_backend_dev alembic upgrade head
```
> Note: Also run this apply migration command the first time you run the dev mode container(**step 4**). Otherwise there will be no tables in the database.


- Create Initial Users: Run seed_admin file to create initial admin in database inside Docker

```
docker exec -it edutrack_backend_dev python app/db/seed_admin.py
```

- If the previous command fails then run the following:

```
docker exec -it edutrack_backend_dev /bin/bash -c "PYTHONPATH=/app python app/db/seed_admin.py"
```


--- 

## 7. Stopping a Container
```
Keeps DB data: docker compose -f docker-compose.dev.yml down OR ctrl+c

Deletes DB data: docker compose -f docker-compose.dev.yml down -v  
```

# Updating Dependencies
- To install new depedencies, activate the venv and run the following command:

```
pip install package-name
```

After installing/removing/upgrading Python dependencies, run the following commands:
```
pip freeze > requirements.txt
```

- Then rebuild the container (**step 4**) to install the dependencies in the container.

---


# API Endpoints
- Backend starts at: http://localhost:8000/api
- Swagger UI(Docs): http://localhost:8000/docs


# What I explored in this project

- Production Deployment: How to deploy in render. Render spins down the container when there is no traffic so a health-check endpoint is added to wake the server.

- Database Management: Howto connect SQLAlchemy(ORM) to PostgreSQL and use Alembic to save database changes.

- Dockerization: How to dockerize a FastAPI backend.

- Middleware creation: How to inject token from cookie to header and add error logs to database using middleware.
