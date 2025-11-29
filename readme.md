## AFTER CLONING RUN THIS PROJECT with the following command
```
docker compose build
docker compose up
or
docker compose up -d

```
- Backend Starts at: http://localhost:8000
- Swagger UI Starts at: http://localhost:8000/docs
- DB persists at: postgres_data

## Start Virtual Environmnt
```
# for windows
venv\Scripts\activate

# for linux mint
source venv/bin/activate
```

## Run Application
```
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

## Alembic Commands for migrations
```
alembic revision --autogenerate -m "message"
alembic upgrade head
```

## Create VENV
```
# for windows
python -m venv venv

# for linux mint
python3 -m venv venv
```

## Install, Save, Restore, Upgrade, Uninstall
```
# INSTALL
pip install requests

# SAVE DEPENDENCIES
pip freeze > requirements.txt

# RESTORE LATER
pip install -r requirements.txt

# UPGRADE
pip install --upgrade requests

# UNINSTALL
pip uninstall requests
```