# Quickstart: Authentication Backend Service

## Prerequisites
- Python 3.11+
- Poetry or pip for dependency management
- NeonDB database instance
- Environment variables configured (see .env.example)

## Setup

1. **Install dependencies**:
   ```bash
   cd backend
   poetry install  # or pip install -r requirements.txt
   ```

2. **Configure environment**:
   ```bash
   cp .env.example .env
   # Edit .env with your database URL and JWT secret
   ```

3. **Run database migrations** (if applicable):
   ```bash
   # Set up your database tables
   ```

## Running the Service

```bash
cd backend
poetry run uvicorn src.main:app --reload --port 8000
```

The authentication endpoints will be available at:
- Register: `POST /api/v1/auth/register`
- Login: `POST /api/v1/auth/login`
- Verify: `POST /api/v1/auth/verify`

## Testing the API

### Register a new user:
```bash
curl -X POST http://localhost:8000/api/v1/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "password": "MySecurePass123"
  }'
```

### Login:
```bash
curl -X POST http://localhost:8000/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "password": "MySecurePass123"
  }'
```

### Use JWT token with protected endpoint:
```bash
curl -X GET http://localhost:8000/api/v1/chat \
  -H "Authorization: Bearer YOUR_JWT_TOKEN_HERE"
```

## Integration with Existing Services

To protect existing endpoints with JWT authentication, add the JWT dependency:

```python
from src.auth.middleware import get_current_user

@app.get("/api/v1/protected-endpoint")
async def protected_route(current_user: User = Depends(get_current_user)):
    return {"user_id": current_user.id, "message": "Access granted"}
```