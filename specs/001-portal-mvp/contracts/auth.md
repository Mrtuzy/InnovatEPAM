# Authentication API Contracts

**Base Path**: `/api/v1/auth`  
**Purpose**: User registration, login, logout, and session management

---

## POST /api/v1/auth/register

**Description**: Register a new user account

**Authorization**: Public (no authentication required)

**Request Body**:
```json
{
  "email": "user@example.com",
  "password": "SecurePass123!",
  "full_name": "John Doe"
}
```

**Request Schema**:
| Field | Type | Required | Constraints |
|-------|------|----------|-------------|
| `email` | string | Yes | Valid email format, unique, max 255 chars |
| `password` | string | Yes | Min 8 chars, 1 uppercase, 1 lowercase, 1 number, 1 special char |
| `full_name` | string | Yes | 2-100 chars, letters/spaces/hyphens/apostrophes only |

**Success Response** (201 Created):
```json
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "email": "user@example.com",
  "full_name": "John Doe",
  "role": "submitter",
  "created_at": "2026-02-24T10:30:00Z"
}
```

**Error Responses**:

400 Bad Request - Validation failure:
```json
{
  "error": "validation_error",
  "details": {
    "email": ["Invalid email format"],
    "password": ["Password must contain at least one uppercase letter"]
  }
}
```

409 Conflict - Email already exists:
```json
{
  "error": "email_already_exists",
  "message": "An account with this email already exists"
}
```

---

## POST /api/v1/auth/login

**Description**: Authenticate user and receive access token

**Authorization**: Public (no authentication required)

**Request Body**:
```json
{
  "email": "user@example.com",
  "password": "SecurePass123!"
}
```

**Request Schema**:
| Field | Type | Required | Constraints |
|-------|------|----------|-------------|
| `email` | string | Yes | Valid email format |
| `password` | string | Yes | Any string |

**Success Response** (200 OK):
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer",
  "expires_in": 900,
  "user": {
    "id": "550e8400-e29b-41d4-a716-446655440000",
    "email": "user@example.com",
    "full_name": "John Doe",
    "role": "submitter"
  }
}
```

**Response Headers**:
```
Set-Cookie: refresh_token=<token>; HttpOnly; Secure; SameSite=Strict; Max-Age=604800
```

**Response Schema**:
| Field | Type | Description |
|-------|------|-------------|
| `access_token` | string | JWT access token (15 min expiry) |
| `token_type` | string | Always "bearer" |
| `expires_in` | integer | Seconds until token expiry (900 = 15 min) |
| `user` | object | Authenticated user details |

**Error Responses**:

401 Unauthorized - Invalid credentials:
```json
{
  "error": "invalid_credentials",
  "message": "Invalid email or password"
}
```

403 Forbidden - Account deactivated:
```json
{
  "error": "account_inactive",
  "message": "This account has been deactivated"
}
```

**Security Notes**:
- Generic error message prevents email enumeration
- Password rate limiting should be implemented (5 attempts per 15 min)
- Refresh token stored in HTTP-only cookie (prevents XSS)

---

## POST /api/v1/auth/logout

**Description**: Invalidate current session

**Authorization**: Required (Bearer token)

**Request Body**: None

**Success Response** (200 OK):
```json
{
  "message": "Logged out successfully"
}
```

**Response Headers**:
```
Set-Cookie: refresh_token=; HttpOnly; Secure; SameSite=Strict; Max-Age=0
```

**Error Responses**:

401 Unauthorized - No valid token:
```json
{
  "error": "unauthorized",
  "message": "Authentication required"
}
```

---

## POST /api/v1/auth/refresh

**Description**: Obtain new access token using refresh token

**Authorization**: Refresh token (from HTTP-only cookie)

**Request Body**: None

**Success Response** (200 OK):
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer",
  "expires_in": 900
}
```

**Error Responses**:

401 Unauthorized - Invalid/expired refresh token:
```json
{
  "error": "invalid_refresh_token",
  "message": "Refresh token is invalid or expired"
}
```

---

## GET /api/v1/auth/me

**Description**: Get current authenticated user profile

**Authorization**: Required (Bearer token)

**Request Body**: None

**Success Response** (200 OK):
```json
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "email": "user@example.com",
  "full_name": "John Doe",
  "role": "submitter",
  "created_at": "2026-02-24T10:30:00Z"
}
```

**Error Responses**:

401 Unauthorized:
```json
{
  "error": "unauthorized",
  "message": "Authentication required"
}
```

---

## Authentication Header Format

All authenticated requests must include:

```
Authorization: Bearer <access_token>
```

**Token Structure** (JWT payload):
```json
{
  "sub": "550e8400-e29b-41d4-a716-446655440000",
  "email": "user@example.com",
  "role": "submitter",
  "exp": 1709034600,
  "iat": 1709033700
}
```

| Field | Description |
|-------|-------------|
| `sub` | User ID (subject) |
| `email` | User email |
| `role` | User role (submitter/admin) |
| `exp` | Expiration timestamp (Unix epoch) |
| `iat` | Issued at timestamp (Unix epoch) |

---

## Rate Limiting

| Endpoint | Limit | Window |
|----------|-------|--------|
| `/auth/register` | 3 requests | 1 hour per IP |
| `/auth/login` | 5 requests | 15 minutes per email |
| `/auth/refresh` | 10 requests | 1 hour per user |

---

## Common Error Response Format

All error responses follow this structure:

```json
{
  "error": "error_code_snake_case",
  "message": "Human-readable error description",
  "details": {
    "field_name": ["Error message 1", "Error message 2"]
  }
}
```

Where `details` is optional and used for validation errors.
