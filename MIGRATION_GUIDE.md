# Migration from NoSQL to PostgreSQL (Supabase) Guide

## Changes Made

### 1. Database Connection (`app/db/database.py`)
- Replaced MongoDB Motor client with SQLModel engine
- Added `create_db_and_tables()` function to initialize tables
- Added `get_session()` dependency for database sessions

### 2. Models (`app/models/user.py`)
- Migrated from Pydantic BaseModel to SQLModel
- Created proper table model: `Student` (with `table=True`)
- Created schemas: `StudentCreate`, `StudentUpdate`, `StudentRead`
- Added proper field constraints and indexes

### 3. Services (`app/services/user_service.py`)
- Replaced async MongoDB operations with synchronous SQLModel queries
- Updated all CRUD operations to use SQLModel Session
- Changed from dict-based to model-based operations

### 4. Router (`app/routers/users.py`)
- Changed from `/users` to `/students` prefix
- Added proper dependency injection for database session
- Updated to use HTTPException for error handling
- Added all CRUD endpoints (GET all, GET one, POST, PATCH, DELETE)
- Removed async/await (SQLModel uses sync operations)

### 5. Dependencies
- Removed: `motor`, `pymongo`
- Added: `psycopg2-binary` (PostgreSQL driver)
- Kept: `sqlmodel` (already in requirements)

## Setup Instructions

### 1. Get Supabase Connection String

1. Go to your Supabase project dashboard
2. Navigate to Settings → Database
3. Find "Connection string" section
4. Copy the URI format connection string
5. It should look like: `postgresql://postgres:[YOUR-PASSWORD]@db.[YOUR-PROJECT-REF].supabase.co:5432/postgres`

### 2. Update .env File

Replace the DATABASE_URL in your `.env` file:

```env
DATABASE_URL=postgresql://postgres:your_password@db.your_project_ref.supabase.co:5432/postgres
PORT=8000
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Run the Application

```bash
python app/main.py
```

Or with uvicorn:

```bash
uvicorn app.main:app --reload --port 8000
```

### 5. Test the API

The database tables will be created automatically on startup.

#### Create a student:
```bash
POST http://localhost:8000/students/
{
  "fullname": "John Doe",
  "email": "jdoe@x.edu.ng",
  "course_of_study": "Computer Science",
  "year": 2,
  "gpa": 3.5
}
```

#### Get all students:
```bash
GET http://localhost:8000/students/
```

#### Get a specific student:
```bash
GET http://localhost:8000/students/1
```

#### Update a student:
```bash
PATCH http://localhost:8000/students/1
{
  "gpa": 3.8
}
```

#### Delete a student:
```bash
DELETE http://localhost:8000/students/1
```

## Key Differences

### NoSQL (MongoDB) → SQL (PostgreSQL)
- `_id` (ObjectId) → `id` (Integer, auto-increment)
- Async operations → Sync operations
- Collection queries → SQL queries via SQLModel
- Document-based → Table-based with relationships support

### API Changes
- Endpoint prefix: `/users` → `/students`
- Error handling: Custom ResponseModel → HTTPException
- Response format: Wrapped responses → Direct model responses
- ID type: String (ObjectId) → Integer

## Benefits of SQLModel + PostgreSQL

1. Type safety with Python type hints
2. Automatic data validation
3. Better query performance with indexes
4. ACID compliance for data integrity
5. Easy to add relationships between tables
6. Supabase provides real-time subscriptions, auth, and storage
