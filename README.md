# 🎓 UTB File Upload Portal

A Flask-based web application for UTB students to upload and manage academic documents. Files are stored in MinIO (S3-compatible object storage), with metadata persisted in a PostgreSQL database.

---

# 📋 Project Status & Roadmap

## ✅ Completed

- [x] **Planning & Tech Stack**
  - [x] Defined project goal (Document Management App for UTB students)
  - [x] Selected full stack (Flask, PostgreSQL, MinIO, Docker)
  - [x] Chosen tools (PyCharm, DBeaver, Postman)

- [x] **Environment Setup**
  - [x] Installed Docker Desktop
  - [x] Created PyCharm project (Pure Python + Virtual Environment)
  - [x] Installed required Python packages (`flask`, `flask-sqlalchemy`, `flask-migrate`, `flask-bcrypt`, `minio`, `boto3`, `psycopg2-binary`, `python-dotenv`)

- [x] **Infrastructure (Docker)**
  - [x] Created `docker-compose.yml` for PostgreSQL & MinIO
  - [x] Started containers successfully
  - [x] Verified MinIO Web UI access (`localhost:9001`)

- [x] **Project Structure**
  - [x] Created folder hierarchy (`app/`, `static/`, `templates/`)
  - [x] Created core files (`app.py`, `main.py`, `.env`, `.flaskenv`)

- [x] **Backend Configuration**
  - [x] Configured `.env` with secure credentials
  - [x] Connected Flask to PostgreSQL via SQLAlchemy
  - [x] Connected Flask to MinIO via boto3 & Minio client
  - [x] Added health check endpoints (`/health`, `/db-check`, `/minio-check`)

- [x] **Database & Models**
  - [x] Defined `Faculty` model (name, code, active flag)
  - [x] Defined `Subject` model (name, code, faculty link)
  - [x] Defined `User` model (email, hashed password, lockout tracking)
  - [x] Defined `File` model (original name, UUID stored name, MinIO path, subject/user links)
  - [x] Configured Flask-Migrate for database migrations

- [x] **Authentication**
  - [x] Implemented User Registration with UTB email validation (`x_surname@utb.cz`)
  - [x] Implemented Login / Logout
  - [x] Password hashing with bcrypt (never stored in plain text)
  - [x] Account lockout after 10 failed attempts (20-minute lock)
  - [x] Password complexity rules (min 8 chars, 1 uppercase, 1 number)

- [x] **Security**
  - [x] UUID-based filename sanitisation to prevent path traversal attacks
  - [x] Soft-delete support for files (hidden from users, retained in MinIO)
  - [x] `is_active` flag on users for account disabling without deletion

---

## 🚧 In Progress / Next Steps

- [ ] **Core Features**
  - [ ] File Upload Logic (stream to MinIO)
  - [ ] File Listing Page (fetch metadata from DB)
  - [ ] File Categorisation by Subject & Faculty
  - [ ] File Download & Delete (with soft-delete)

- [ ] **Frontend & UI**
  - [ ] Integrate Bootstrap
  - [ ] Build Dashboard Template
  - [ ] Build Login / Register Forms
  - [ ] File browser UI with search and filters

- [ ] **Route Protection**
  - [ ] Secure routes with `@login_required`
  - [ ] Role-based access (student vs admin)

- [ ] **Testing & Deployment**
  - [ ] API Testing with Postman
  - [ ] Write unit tests for auth and file logic
  - [ ] Final scalability check (3000+ users simulation)
  - [ ] Disable `debug=True` and harden for production
  - [ ] Deploy with Gunicorn + Nginx

---

## 🗂️ Project Structure

