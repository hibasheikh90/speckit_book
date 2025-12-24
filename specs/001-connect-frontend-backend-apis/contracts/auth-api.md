# Authentication API Contract

**Endpoint**: `/auth/login`
**Method**: POST
**Purpose**: Authenticate user with email and password, return JWT access token
**Backend Implementation**: `backend/src/auth/routes/login.py`
**Rate Limit**: 5 requests per 15 minutes (per IP address)

---

## Request

### Headers
```http
Content-Type: application/json
Accept: application/json
```

### Body Schema
```json
{
  "email": "string (required)",
  "password": "string (required)"
}
```

**TypeScript Interface**:
```typescript
interface LoginRequest {
  email: string;       // Valid email format
  password: string;    // Min 8 characters (enforced by backend)
}
```

### Validation Rules (Backend)
- `email`: Required, must be valid email format
- `password`: Required, minimum 8 characters, must contain uppercase, lowercase, and number

### Example Request
```bash
curl -X POST "http://localhost:8000/auth/login" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "student@example.com",
    "password": "SecurePass123"
  }'
```

---

## Successful Response (200 OK)

### Body Schema
```json
{
  "access_token": "string (JWT token)",
  "user_id": "string (UUID)",
  "token_type": "string (always 'bearer')"
}
```

**TypeScript Interface**:
```typescript
interface LoginResponse {
  access_token: string;  // JWT bearer token (24-hour validity)
  user_id: string;       // User UUID from database
  token_type: string;    // Literal: "bearer"
}
```

### Example Response
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJhMWIyYzNkNC1lNWY2LTc4OTAtYWJjZC1lZjEyMzQ1Njc4OTAiLCJleHAiOjE3MDMzNDMwMDB9.signature",
  "user_id": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
  "token_type": "bearer"
}
```

### Frontend Handling
```typescript
const response = await fetch('/auth/login', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({ email, password })
});

if (response.ok) {
  const data: LoginResponse = await response.json();
  localStorage.setItem('authToken', data.access_token);
  localStorage.setItem('user', JSON.stringify({
    id: data.user_id,
    email
  }));
  // Redirect to dashboard or enable chat
}
```

---

## Error Responses

### 401 Unauthorized (Invalid Credentials)

**Trigger**: Incorrect email or password

**Body**:
```json
{
  "detail": "Invalid email or password"
}
```

**Frontend Handling**:
```typescript
if (response.status === 401) {
  const error = await response.json();
  setErrorMessage('Invalid email or password. Please try again.');
  console.error('[Auth Error]', {
    timestamp: new Date().toISOString(),
    status: 401,
    detail: error.detail
  });
}
```

---

### 422 Unprocessable Entity (Validation Error)

**Trigger**: Invalid request body (missing fields, wrong format)

**Body**:
```json
{
  "detail": [
    {
      "loc": ["body", "email"],
      "msg": "value is not a valid email address",
      "type": "value_error.email"
    }
  ]
}
```

**Frontend Handling**:
```typescript
if (response.status === 422) {
  const error = await response.json();
  setErrorMessage('Invalid email or password format. Please check your input.');
  console.error('[Validation Error]', {
    timestamp: new Date().toISOString(),
    status: 422,
    detail: error.detail
  });
}
```

---

### 429 Too Many Requests (Rate Limit Exceeded)

**Trigger**: More than 5 login attempts within 15 minutes

**Body**:
```json
{
  "detail": "Rate limit exceeded: 5 per 15 minute"
}
```

**Headers**:
```http
Retry-After: 900  # Seconds until rate limit resets
```

**Frontend Handling**:
```typescript
if (response.status === 429) {
  const retryAfter = response.headers.get('Retry-After');
  const minutes = retryAfter ? Math.ceil(parseInt(retryAfter) / 60) : 15;
  setErrorMessage(`Too many login attempts. Please try again in ${minutes} minutes.`);
}
```

---

### 500 Internal Server Error

**Trigger**: Backend exception (database error, unexpected error)

**Body**:
```json
{
  "detail": "An unexpected error occurred during login"
}
```

**Frontend Handling**:
```typescript
if (response.status === 500) {
  setErrorMessage('The service is temporarily unavailable. Please try again later.');
  console.error('[Server Error]', {
    timestamp: new Date().toISOString(),
    status: 500
  });
}
```

---

## Security Considerations

### Password Transmission
- Passwords sent in **plain text over HTTPS** (encrypted in transit)
- Backend hashes passwords with **bcrypt** before database storage
- **Never log passwords** in frontend console or error messages

### Token Storage
- Store `access_token` in **localStorage** (acceptable for MVP)
- **Future Enhancement**: Migrate to HttpOnly cookies to prevent XSS attacks (see ADR placeholder)

### CORS
- Backend must allow frontend origin: `http://localhost:3000` (dev) and production domain
- Credentials not included in requests (stateless JWT auth)

### Rate Limiting
- **Backend enforced**: 5 attempts per 15 minutes per IP (slowapi middleware)
- **Frontend suggestion**: Disable login button after 3 failed attempts until manual retry

---

## Contract Invariants

1. **Response Format**: Always returns JSON (never HTML error pages)
2. **Token Type**: Always "bearer" (never changes)
3. **User ID Format**: Always UUID v4 (36 characters with hyphens)
4. **Token Validity**: 24 hours from issuance (per backend settings)
5. **Backward Compatibility**: No breaking changes to request/response schema without versioning

---

## Testing Checklist

- [ ] Valid credentials return 200 with access_token
- [ ] Invalid email format returns 422
- [ ] Incorrect password returns 401
- [ ] Non-existent user returns 401 (same as incorrect password, for security)
- [ ] Missing email or password returns 422
- [ ] 6th request within 15 minutes returns 429
- [ ] access_token is valid JWT (can be decoded)
- [ ] user_id matches database record
- [ ] Token works for protected endpoints (if applicable in future)
- [ ] Network timeout handled gracefully (30s timeout)
