# Municipal Incident Management System
### INF 395 – Phase 2 | Institutional Information System Project

---

## 📌 Project Overview

The Municipal Incident Management System is an institutional backend system designed to support city authorities in managing urban infrastructure incidents.

The system enables:
- Citizens to report municipal problems
- Operators to update incident statuses
- Administrators to monitor audit logs
- Geographic zoning and spatial filtering using H3 indexing

This project demonstrates institutional system design, role-based security, audit logging, and geospatial indexing.

---

## 🛠 Technology Stack

- Python 3.10+
- FastAPI
- SQLite
- H3 (Uber Hexagonal Spatial Index)
- Uvicorn

---

## 🚀 How to Run the System

### 1️⃣ Install Dependencies

pip install fastapi uvicorn h3


### 2️⃣ Run the Application

uvicorn main:app --reload


### 3️⃣ Open API Documentation

Open your browser and navigate to:

http://127.0.0.1:8000/docs


---

## 👥 Default Users (Pre-seeded)

The system automatically creates default users if the database is empty.

| ID | Name  | Role     |
|----|-------|----------|
| 1  | Alice | CITIZEN  |
| 2  | Bob   | OPERATOR |
| 3  | Admin | ADMIN    |

> Authentication is simplified for academic purposes. Users pass user_id as a query parameter.

Example:

POST /incidents?title=Water pipe broken&lat=43.23&lon=76.88&severity=HIGH&user_id=1


---

## 🔌 Implemented Endpoints

### Incident Management

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | /incidents | Create new incident *(CITIZEN only)* |
| GET | /incidents | Retrieve all incidents |
| PATCH | /incidents/{incident_id} | Update status *(OPERATOR only)* |
| GET | /incidents/h3/{h3_index} | Filter incidents by H3 cell |
| GET | /incidents/near | Retrieve incidents near a location |

### Audit

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | /audit | View audit logs *(ADMIN only)* |

---

## 🗺 How H3 Is Used in the System

H3 (Uber's Hexagonal Hierarchical Spatial Index) is used for geographic partitioning and institutional zoning.

### 1️⃣ Incident Creation

When a citizen submits coordinates, the system converts them into an H3 cell:

h3_index = h3.latlng_to_cell(lat, lon, 9)


> Resolution 9 provides city-level granularity. The H3 index is stored in the database.

### 2️⃣ Spatial Filtering

GET /incidents/h3/{h3_index}
GET /incidents/near?lat=...&lon=...


### 3️⃣ Institutional Benefits of H3

- Geographic aggregation
- Zoning responsibility for operators
- Efficient spatial queries
- Urban region partitioning
- Scalable city-level analytics

---

## 🔐 Security Model

The system implements Role-Based Access Control (RBAC):

| Role | Permission |
|------|------------|
| CITIZEN | Can create incidents |
| OPERATOR | Can update incident status |
| ADMIN | Can view audit logs |

> Unauthorized access returns HTTP 403 Forbidden. All critical actions are recorded in the audit log.

---

## 📊 Audit Logging

Audit logs are created automatically when:
- An incident is created
- An incident status is updated

This ensures institutional traceability and accountability.

---

## 👨‍💻 Group Member Roles

| Name | Role in Project | Responsibilities |
|------|----------------|-----------------|
| Dosymzhan Seisen | Backend Developer | API development, database design, H3 integration |
| Bexultan Nessipbekov | Frontend Developer | API testing, interface design (Phase 1 concept) |
| Meruyert Askar | QA / Tester | Role verification, endpoint testing, validation scenarios |
| Arailym Aidarbek | Project Manager | Documentation, planning, system framing |
