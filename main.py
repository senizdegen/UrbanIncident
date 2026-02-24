from fastapi import FastAPI, HTTPException, Depends
import sqlite3
import h3
from datetime import datetime, timezone

app = FastAPI(title="Municipal Incident Management System")

db = sqlite3.connect("db.sqlite", check_same_thread=False)
cur = db.cursor()

cur.execute("""
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY,
    name TEXT,
    role TEXT CHECK(role IN ('CITIZEN','OPERATOR','ADMIN'))
)
""")

cur.execute("""
CREATE TABLE IF NOT EXISTS incidents (
    id INTEGER PRIMARY KEY,
    title TEXT,
    lat REAL,
    lon REAL,
    h3_index TEXT,
    severity TEXT CHECK(severity IN ('LOW','MEDIUM','HIGH')),
    status TEXT
)
""")

cur.execute("""
CREATE TABLE IF NOT EXISTS audit_logs (
    id INTEGER PRIMARY KEY,
    action TEXT,
    user_id INTEGER,
    incident_id INTEGER,
    time TEXT
)
""")

db.commit()

cur.execute("SELECT COUNT(*) FROM users")
if cur.fetchone()[0] == 0:
    cur.executemany(
        "INSERT INTO users VALUES (NULL, ?, ?)",
        [
            ("Alice", "CITIZEN"),
            ("Bob", "OPERATOR"),
            ("Admin", "ADMIN")
        ]
    )
    db.commit()

def get_user(user_id: int):
    user = cur.execute(
        "SELECT id, name, role FROM users WHERE id=?",
        (user_id,)
    ).fetchone()
    if not user:
        raise HTTPException(status_code=401, detail="Invalid user")
    return {"id": user[0], "name": user[1], "role": user[2]}

def require_role(role: str):
    def checker(user=Depends(get_user)):
        if user["role"] != role:
            raise HTTPException(
                status_code=403,
                detail=f"Requires role {role}"
            )
        return user
    return checker

@app.post("/incidents")
def create_incident(
    title: str,
    lat: float,
    lon: float,
    severity: str,
    user=Depends(require_role("CITIZEN"))
):
    h3_index = h3.latlng_to_cell(lat, lon, 9)

    cur.execute(
        "INSERT INTO incidents VALUES (NULL, ?, ?, ?, ?, ?, 'OPEN')",
        (title, lat, lon, h3_index, severity)
    )
    incident_id = cur.lastrowid

    cur.execute(
        "INSERT INTO audit_logs VALUES (NULL, 'CREATE', ?, ?, ?)",
        (user["id"], incident_id, datetime.now(timezone.utc).isoformat())
    )

    db.commit()
    return {
        "incident_id": incident_id,
        "h3": h3_index,
        "status": "OPEN"
    }

@app.get("/incidents")
def get_incidents():
    return cur.execute("SELECT * FROM incidents").fetchall()

@app.patch("/incidents/{incident_id}")
def update_status(
    incident_id: int,
    status: str,
    user=Depends(require_role("OPERATOR"))
):
    cur.execute(
        "UPDATE incidents SET status=? WHERE id=?",
        (status, incident_id)
    )

    if cur.rowcount == 0:
        raise HTTPException(status_code=404, detail="Incident not found")

    cur.execute(
        "INSERT INTO audit_logs VALUES (NULL, 'UPDATE', ?, ?, ?)",
        (user["id"], incident_id, datetime.now(timezone.utc).isoformat())
    )

    db.commit()
    return {"status": "updated"}

@app.get("/audit")
def get_audit_logs(user=Depends(require_role("ADMIN"))):
    return cur.execute("SELECT * FROM audit_logs").fetchall()

@app.get("/incidents/h3/{h3_index}")
def incidents_by_h3(h3_index: str):
    return cur.execute(
        "SELECT * FROM incidents WHERE h3_index=?",
        (h3_index,)
    ).fetchall()

@app.get("/incidents/near")
def incidents_near(lat: float, lon: float):
    cell = h3.latlng_to_cell(lat, lon, 9)
    return cur.execute(
        "SELECT * FROM incidents WHERE h3_index=?",
        (cell,)
    ).fetchall()