# Edutrack

This project generates student results. It uses **FastAPI** for the backend, **Docker** for containerization, **PostgreSQL** for the database, **SQLAlchemy** for ORM and Database models and **Alembic** for database migrations.

Edutrack, a result management system I built to learn about FastAPI, PostgreSQL, SqlAlchemy and React.
It is not a startup-product not a polished one but it helped me learn a lot. The goal was not to launch a product but to see how FastAPI, React and Docker behave in production.

Here's what genuinely challenged me:

*  **Middleware**: Middleware that actually works. 
    - I built an Audit Log middleware that intercepts create, update and delete requests and saves them to the database. 
    - It also stores error information.
   	- I also built an token injection middleware that takes JWT from HttpOnly cookies and adds it to the authorization header (The OAuth2PasswordBearer requires the token in the header).

*  **Httponly Cookie:** Moving JWT out of localStorage was a mindset shift. Cookies that JavaScript can't touch provide XSS protection by design.

*  **Alembic Migration:** Alembic for database migrations. I used it to track schema changes and apply them to the database. It solved the problem of updating the table without touching the database.

*  **Docker:**  Wired the backend and PostgreSQL into a shared network with one config file. One command, full environment. Killed the "works on my machine" problem immediately.

*  **Cold Starts and Real Latency:** Deploying to Render (free tier) and NeonDB was a reality check. That 2-second delay on first login taught me more about connection pooling and geographic latency than any tutorial ever did. I also built a frontend polling system just to wake the server before users hit it — hacky, but it worked.

*  **Role-Based Access Control via Dependency Injection:** Used dependency injection to give read/write permissions to different types of users eg: Admin, Teacher, Student.
	- **Admins:** 
        * Inserts and updates student and teachers data, 
        * See logs, 
        * Insert marks, 
        * publish bulk results (push result related notification via websokcet and email), 
        * inset and update subjects and assign them to various departments, 
        * assign courses to teachers
    - **Teacher:** 
        * View their assigned subjects, 
        * Insert marks to the subjects they teach, 
        * view results
	- **Student:** 
        * View their course subjects and results. 
        * Challenge published results.

* **Resource Monitoring:** Running everything in Docker let me watch CPU and RAM in real-time. Idle sat around 0.14%, average load hovered between 10–15%. Seeing your own code's baseline cost is oddly humbling.

**Live Link**: https://edutrack-ams.vercel.app
---

# How to run this project

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
