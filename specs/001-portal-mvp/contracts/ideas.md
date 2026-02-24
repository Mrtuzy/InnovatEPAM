# Ideas API Contracts

**Base Path**: `/api/v1/ideas`  
**Purpose**: Idea submission, listing, viewing, and file attachment management

---

## POST /api/v1/ideas

**Description**: Create a new idea

**Authorization**: Required - Role: submitter or admin

**Request Body** (multipart/form-data):
```
title: "Automated Code Review System"
description: "Implement an automated system that reviews code quality..."
category_id: "650e8400-e29b-41d4-a716-446655440001"
attachment: [file] (optional)
```

**Request Schema**:
| Field | Type | Required | Constraints |
|-------|------|----------|-------------|
| `title` | string | Yes | 10-200 chars |
| `description` | string | Yes | 50-5000 chars |
| `category_id` | UUID | Yes | Must exist in categories table |
| `attachment` | file | No | Max 10MB, allowed types: PDF, DOCX, XLSX, JPG, PNG |

**Success Response** (201 Created):
```json
{
  "id": "750e8400-e29b-41d4-a716-446655440002",
  "title": "Automated Code Review System",
  "description": "Implement an automated system that reviews code quality...",
  "category": {
    "id": "650e8400-e29b-41d4-a716-446655440001",
    "name": "Technology Innovation"
  },
  "status": "submitted",
  "attachment": {
    "filename": "architecture-diagram.pdf",
    "size": 2458624,
    "mimetype": "application/pdf",
    "download_url": "/api/v1/ideas/750e8400-e29b-41d4-a716-446655440002/attachment"
  },
  "submitter": {
    "id": "550e8400-e29b-41d4-a716-446655440000",
    "full_name": "John Doe",
    "email": "john.doe@example.com"
  },
  "created_at": "2026-02-24T14:30:00Z",
  "updated_at": "2026-02-24T14:30:00Z"
}
```

**Error Responses**:

400 Bad Request - Validation error:
```json
{
  "error": "validation_error",
  "details": {
    "title": ["Title must be at least 10 characters"],
    "description": ["Description is required"],
    "attachment": ["File size exceeds 10MB limit"]
  }
}
```

404 Not Found - Invalid category:
```json
{
  "error": "category_not_found",
  "message": "Category with ID 650e8400... does not exist"
}
```

413 Payload Too Large - File too large:
```json
{
  "error": "file_too_large",
  "message": "File size exceeds maximum allowed size of 10MB"
}
```

415 Unsupported Media Type - Invalid file type:
```json
{
  "error": "unsupported_file_type",
  "message": "File type .exe is not allowed. Supported types: PDF, DOCX, XLSX, JPG, PNG"
}
```

---

## GET /api/v1/ideas

**Description**: List ideas (filtered by user role)

**Authorization**: Required
- **Submitters**: See only their own ideas
- **Admins**: See all ideas from all users

**Query Parameters**:
| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `status` | string | No | all | Filter by status: submitted, under_review, accepted, rejected, all |
| `category_id` | UUID | No | - | Filter by category |
| `page` | integer | No | 1 | Page number (1-based) |
| `limit` | integer | No | 20 | Items per page (max 100) |
| `sort` | string | No | created_at_desc | Sort order: created_at_desc, created_at_asc, title_asc |

**Example Request**:
```
GET /api/v1/ideas?status=submitted&page=1&limit=20&sort=created_at_desc
```

**Success Response** (200 OK):
```json
{
  "items": [
    {
      "id": "750e8400-e29b-41d4-a716-446655440002",
      "title": "Automated Code Review System",
      "status": "submitted",
      "category": {
        "id": "650e8400-e29b-41d4-a716-446655440001",
        "name": "Technology Innovation"
      },
      "has_attachment": true,
      "submitter": {
        "id": "550e8400-e29b-41d4-a716-446655440000",
        "full_name": "John Doe"
      },
      "evaluation_count": 0,
      "created_at": "2026-02-24T14:30:00Z"
    }
  ],
  "pagination": {
    "total": 45,
    "page": 1,
    "limit": 20,
    "pages": 3
  }
}
```

**Response Schema**:
| Field | Type | Description |
|-------|------|-------------|
| `items` | array | Array of idea summary objects |
| `pagination.total` | integer | Total number of ideas matching filter |
| `pagination.page` | integer | Current page number |
| `pagination.limit` | integer | Items per page |
| `pagination.pages` | integer | Total number of pages |

**Note**: Description field is NOT included in list view for performance

**Error Responses**:

400 Bad Request - Invalid parameters:
```json
{
  "error": "invalid_parameters",
  "details": {
    "status": ["Invalid status value. Must be: submitted, under_review, accepted, rejected, or all"],
    "limit": ["Limit must be between 1 and 100"]
  }
}
```

---

## GET /api/v1/ideas/{id}

**Description**: Get detailed idea information

**Authorization**: Required
- **Submitters**: Can view only their own ideas
- **Admins**: Can view any idea

**Path Parameters**:
| Parameter | Type | Description |
|-----------|------|-------------|
| `id` | UUID | Idea identifier |

**Success Response** (200 OK):
```json
{
  "id": "750e8400-e29b-41d4-a716-446655440002",
  "title": "Automated Code Review System",
  "description": "Implement an automated system that reviews code quality, detects common issues, and suggests improvements. The system would integrate with our Git workflow and provide real-time feedback to developers.",
  "category": {
    "id": "650e8400-e29b-41d4-a716-446655440001",
    "name": "Technology Innovation",
    "description": "New tools, platforms, or technical solutions"
  },
  "status": "under_review",
  "attachment": {
    "filename": "architecture-diagram.pdf",
    "size": 2458624,
    "mimetype": "application/pdf",
    "download_url": "/api/v1/ideas/750e8400-e29b-41d4-a716-446655440002/attachment"
  },
  "submitter": {
    "id": "550e8400-e29b-41d4-a716-446655440000",
    "full_name": "John Doe",
    "email": "john.doe@example.com"
  },
  "latest_evaluation": {
    "evaluator": {
      "id": "450e8400-e29b-41d4-a716-446655440099",
      "full_name": "Admin User"
    },
    "comment": "This looks promising. We're reviewing technical feasibility with the dev team.",
    "previous_status": "submitted",
    "new_status": "under_review",
    "created_at": "2026-02-24T16:00:00Z"
  },
  "evaluation_count": 1,
  "created_at": "2026-02-24T14:30:00Z",
  "updated_at": "2026-02-24T16:00:00Z"
}
```

**Note**: `latest_evaluation` is null if no evaluations exist yet

**Error Responses**:

404 Not Found - Idea doesn't exist:
```json
{
  "error": "idea_not_found",
  "message": "Idea with ID 750e8400... not found"
}
```

403 Forbidden - Submitter trying to access another user's idea:
```json
{
  "error": "access_denied",
  "message": "You don't have permission to view this idea"
}
```

---

## GET /api/v1/ideas/{id}/attachment

**Description**: Download idea attachment file

**Authorization**: Required
- **Submitters**: Can download only their own idea attachments
- **Admins**: Can download any attachment

**Path Parameters**:
| Parameter | Type | Description |
|-----------|------|-------------|
| `id` | UUID | Idea identifier |

**Success Response** (200 OK):
- **Content-Type**: File's original MIME type (e.g., `application/pdf`)
- **Content-Disposition**: `attachment; filename="architecture-diagram.pdf"`
- **Body**: Binary file content

**Error Responses**:

404 Not Found - Idea has no attachment:
```json
{
  "error": "attachment_not_found",
  "message": "This idea does not have an attachment"
}
```

403 Forbidden:
```json
{
  "error": "access_denied",
  "message": "You don't have permission to download this attachment"
}
```

---

## POST /api/v1/ideas/{id}/evaluate

**Description**: Evaluate idea (admin only) - change status and add comment

**Authorization**: Required - Role: admin only

**Path Parameters**:
| Parameter | Type | Description |
|-----------|------|-------------|
| `id` | UUID | Idea identifier |

**Request Body**:
```json
{
  "status": "accepted",
  "comment": "Excellent idea! We'll include this in Q2 roadmap. The technical team will reach out to discuss implementation details."
}
```

**Request Schema**:
| Field | Type | Required | Constraints |
|-------|------|----------|-------------|
| `status` | string | Yes | Enum: submitted, under_review, accepted, rejected |
| `comment` | string | Yes | 10-2000 chars |

**Success Response** (200 OK):
```json
{
  "id": "750e8400-e29b-41d4-a716-446655440002",
  "status": "accepted",
  "latest_evaluation": {
    "id": "850e8400-e29b-41d4-a716-446655440003",
    "evaluator": {
      "id": "450e8400-e29b-41d4-a716-446655440099",
      "full_name": "Admin User"
    },
    "comment": "Excellent idea! We'll include this in Q2 roadmap.",
    "previous_status": "under_review",
    "new_status": "accepted",
    "created_at": "2026-02-24T17:00:00Z"
  },
  "updated_at": "2026-02-24T17:00:00Z"
}
```

**Error Responses**:

403 Forbidden - Non-admin user:
```json
{
  "error": "admin_required",
  "message": "Only administrators can evaluate ideas"
}
```

404 Not Found:
```json
{
  "error": "idea_not_found",
  "message": "Idea with ID 750e8400... not found"
}
```

400 Bad Request - Validation error:
```json
{
  "error": "validation_error",
  "details": {
    "status": ["Invalid status value"],
    "comment": ["Comment must be at least 10 characters"]
  }
}
```

409 Conflict - Status unchanged:
```json
{
  "error": "status_unchanged",
  "message": "New status must be different from current status"
}
```

---

## GET /api/v1/ideas/{id}/evaluations

**Description**: Get evaluation history for an idea

**Authorization**: Required
- **Submitters**: Can view only their own idea evaluations
- **Admins**: Can view any idea's evaluations

**Path Parameters**:
| Parameter | Type | Description |
|-----------|------|-------------|
| `id` | UUID | Idea identifier |

**Success Response** (200 OK):
```json
{
  "idea_id": "750e8400-e29b-41d4-a716-446655440002",
  "evaluations": [
    {
      "id": "850e8400-e29b-41d4-a716-446655440003",
      "evaluator": {
        "id": "450e8400-e29b-41d4-a716-446655440099",
        "full_name": "Admin User"
      },
      "comment": "Excellent idea! We'll include this in Q2 roadmap.",
      "previous_status": "under_review",
      "new_status": "accepted",
      "created_at": "2026-02-24T17:00:00Z"
    },
    {
      "id": "840e8400-e29b-41d4-a716-446655440002",
      "evaluator": {
        "id": "450e8400-e29b-41d4-a716-446655440099",
        "full_name": "Admin User"
      },
      "comment": "This looks promising. We're reviewing technical feasibility.",
      "previous_status": "submitted",
      "new_status": "under_review",
      "created_at": "2026-02-24T16:00:00Z"
    }
  ]
}
```

**Note**: Evaluations ordered by most recent first

**Error Responses**:

404 Not Found:
```json
{
  "error": "idea_not_found",
  "message": "Idea with ID 750e8400... not found"
}
```

403 Forbidden:
```json
{
  "error": "access_denied",
  "message": "You don't have permission to view this idea's evaluations"
}
```

---

## GET /api/v1/categories

**Description**: List available categories for idea submission

**Authorization**: Required (any authenticated user)

**Query Parameters**:
| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `active_only` | boolean | No | true | Show only active categories |

**Success Response** (200 OK):
```json
{
  "categories": [
    {
      "id": "650e8400-e29b-41d4-a716-446655440001",
      "name": "Technology Innovation",
      "description": "New tools, platforms, or technical solutions",
      "display_order": 2
    },
    {
      "id": "650e8400-e29b-41d4-a716-446655440002",
      "name": "Process Improvement",
      "description": "Ideas to streamline workflows and procedures",
      "display_order": 1
    }
  ]
}
```

**Note**: Ordered by `display_order` ascending

---

## Response Time SLA

| Endpoint | Target | Description |
|----------|--------|-------------|
| `POST /ideas` | < 500ms | Excluding file upload time |
| `GET /ideas` | < 2s | For up to 100 results |
| `GET /ideas/{id}` | < 200ms | Single idea retrieval |
| `GET /ideas/{id}/attachment` | < 10s | For files up to 10MB |
| `POST /ideas/{id}/evaluate` | < 300ms | Status update |

---

## File Upload Requirements

**Supported File Types**:
- **Documents**: `.pdf`, `.doc`, `.docx`
- **Spreadsheets**: `.xls`, `.xlsx`
- **Images**: `.jpg`, `.jpeg`, `.png`, `.gif`

**Validation**:
1. File extension check
2. MIME type verification
3. File size limit (10MB = 10,485,760 bytes)
4. Filename sanitization (remove special characters, prevent path traversal)
5. Virus scanning (recommended for production)

**Storage**:
- Development: Local filesystem `uploads/ideas/{idea_id}/`
- Production: S3-compatible object storage with pre-signed URLs
