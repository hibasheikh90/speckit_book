# Data Model: Authentication Backend Service

## User Entity

### Fields
- **id** (UUID/Integer): Primary key, unique identifier for the user
- **email** (String, unique): User's email address, used for login
- **hashed_password** (String): Bcrypt-hashed password (60 characters for bcrypt)
- **created_at** (DateTime): Timestamp when user account was created
- **updated_at** (DateTime): Timestamp when user account was last updated

### Validation Rules
- email: Must be valid email format, unique across all users
- hashed_password: Required, stored as bcrypt hash (never plain text)
- email: Required, minimum length 5 characters, maximum length 255 characters

### Relationships
- No direct relationships needed for basic authentication (may be extended later for user profiles)

### State Transitions
- User account created during registration (active immediately as per spec)
- User data updated only when password is changed

## JWT Token Structure

### Claims
- **sub** (Subject): user_id from the users table
- **exp** (Expiration Time): Unix timestamp for token expiration (24 hours from creation)
- **iat** (Issued At): Unix timestamp when token was created
- **jti** (JWT ID): Optional unique identifier for token (for potential revocation)

### Validation Rules
- Token must be signed with HS256 algorithm
- Token must not be expired at time of validation
- Token signature must be valid against stored secret key

## Database Schema (NeonDB/PostgreSQL)

```sql
CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    email VARCHAR(255) UNIQUE NOT NULL,
    hashed_password VARCHAR(255) NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_users_email ON users(email);

-- Update trigger for updated_at
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ language 'plpgsql';

CREATE TRIGGER update_users_updated_at
    BEFORE UPDATE ON users
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();
```