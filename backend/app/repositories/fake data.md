uvicorn app.main:app --reload


From backend run:

Get-Content app/db/database.py

Also run:

Get-Content app/main.py

And:

Get-Content app/models/task.py



Run this from backend:

python -c "from app.db.database import engine; print(engine.pool); print(type(engine.pool))"

Then:

python -c "from app.db.database import SessionLocal; db=SessionLocal(); print(db); db.close(); print('Session closed')"

You should get information about the SQLAlchemy pool and a successful session creation.


Run this one:

python -c "from app.db.database import engine; print(engine.pool); print(type(engine.pool))"

Then run:

python -c "from app.db.database import POSTGRES_HOST, POSTGRES_PORT, POSTGRES_DB, POSTGRES_USER; print('HOST:', POSTGRES_HOST); print('PORT:', POSTGRES_PORT); print('DB:', POSTGRES_DB); print('USER:', POSTGRES_USER)"

Send m



python -c "from app.db.database import SessionLocal; from app.models.task import Task; db=SessionLocal(); print(db.query(Task).filter(Task.title == 'Transaction Test').all()); db.close()"




Part 1 — Clean the temporary file

Run:

Remove-Item test_transaction.py

Then:

Get-ChildItem
Part 2 — Inspect your existing Alembic configuration

Run these one at a time:

Get-ChildItem alembic -Recurse
Get-Content alembic/env.py
Get-Content alembic.ini


Get-Content alembic/env.py

Get-Content alembic/versions/444644bc7d1e_create_tasks_table.py



alembic revision --autogenerate -m "add task priority"


python -c "from app.db.database import SessionLocal; from app.models.task import Task; db=SessionLocal(); tasks=db.query(Task).all(); print([(t.id, t.title, t.priority) for t in tasks]); db.close()"


Then send me the output of:

alembic current

and:

python -c "from app.db.database import SessionLocal; from app.models.task import Task; db=SessionLocal(); tasks=db.query(Task).all(); print([(t.id, t.title, t.priority) for t in tasks]); db.close()"

Then we'll finish the API side of priority.


python -c "from app.db.database import SessionLocal; from app.models.task import Task; db=SessionLocal(); tasks=db.query(Task).all(); print([(t.id, t.title, t.priority) for t in tasks]); db.close()"




Run:

Get-Content app/schemas/task.py

Also:

Get-Content app/api/tasks.py

And:

Get-Content app/services/task_service.py


docker exec -it task_manager_postgres psql -U task_manager -d task_manager


.\.venv\Scripts\Activate.ps1


Get-ChildItem Env: | Where-Object {$_.Name -match "proxy"}


[Environment]::GetEnvironmentVariables("User").GetEnumerator() | Where-Object { $_.Key -match "proxy" }



[Environment]::GetEnvironmentVariables("Machine").GetEnumerator() | Where-Object { $_.Key -match "proxy" }



Get-ChildItem "$env:APPDATA\Docker" -Recurse -File -ErrorAction SilentlyContinue |Select-String -Pattern "http.docker.internal|https.docker.internal|proxy" -SimpleMatch


Get-Content backend\requirements.txt
Get-ChildItem "$env:LOCALAPPDATA\Docker\log" -Recurse -File -ErrorAction SilentlyContinue | Where-Object { $_.Name -match "proxy|http" } | Select-Object FullName