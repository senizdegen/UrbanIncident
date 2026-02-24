# Municipal Incident Management System

Institutional Information System for managing municipal incidents  
with role-based access control, audit logging, and H3 spatial indexing.

This project was developed as part of **INF 395 – Phase 2 (Institutional Information System)**.

---

## 📌 Overview

The system models how real municipal institutions handle critical incidents such as:
- utility failures
- public infrastructure problems
- emergency reports

It enforces **institutional constraints**, supports **multiple user roles**, and uses  
**H3 spatial indexing** to group incidents geographically.

---

## 🏗️ System Features

- Role-based access control (Citizen, Operator, Admin)
- Immutable audit logs
- No deletion of critical data
- Geographic aggregation using **H3**
- REST API with interactive Swagger documentation
- Realistic backend implementation (FastAPI + SQLite)

---

## 👥 User Roles

| Role | Permissions |
|----|----|
| **CITIZEN** | Create incidents |
| **OPERATOR** | Update incident status |
| **ADMIN** | View audit logs |

> Authentication is simplified for educational purposes using `user_id` as a query parameter.

---

## 🧱 Technology Stack

- **Python 3.9+**
- **FastAPI**
- **SQLite**
- **H3 (Uber Hexagonal Spatial Indexing)**
- **Uvicorn**

---

---

## ⚙️ Installation & Setup

### 1️⃣ Clone the repository

```bash
git clone https://github.com/senizdegen/UrbanIncident
cd UrbanIncident

python -m venv venv

pip install fastapi uvicorn h3

uvicorn main:app --reload

http://127.0.0.1:8000/docs
