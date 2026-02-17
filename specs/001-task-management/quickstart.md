# Quickstart Guide: Task Management Backend

## Setup Instructions

### Prerequisites
- Python 3.11+
- pip package manager
- Access to Neon PostgreSQL database

### Installation Steps

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd <repository-directory>
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r backend/requirements.txt
   ```

4. **Configure environment variables**
   ```bash
   cp backend/.env.example backend/.env
   # Edit backend/.env with your database connection details
   ```

5. **Run the application**
   ```bash
   cd backend
   uvicorn src.main:app --reload --port 8000
   ```

## API Usage Examples

### Create a Task
```bash
curl -X POST http://localhost:8000/api/user123/tasks \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Buy groceries",
    "description": "Milk, eggs, bread",
    "completed": false
  }'
```

### Get All Tasks for a User
```bash
curl -X GET http://localhost:8000/api/user123/tasks
```

### Get a Specific Task
```bash
curl -X GET http://localhost:8000/api/user123/tasks/1
```

### Update a Task
```bash
curl -X PUT http://localhost:8000/api/user123/tasks/1 \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Buy groceries (urgent)",
    "description": "Milk, eggs, bread - needed today",
    "completed": false
  }'
```

### Delete a Task
```bash
curl -X DELETE http://localhost:8000/api/user123/tasks/1
```

### Mark Task as Complete
```bash
curl -X PATCH http://localhost:8000/api/user123/tasks/1/complete
```

## Running Tests

```bash
cd backend
pytest tests/ -v
```

## Database Migrations

Apply migrations:
```bash
cd backend
alembic upgrade head
```

Create new migration:
```bash
alembic revision --autogenerate -m "Description of changes"
```