# IO Contract for User Registration & Login (RETAIL-5)

This document defines the API IO contracts (request/response schemas) for CRUD operations related to user registration and login.

---

## 1. Create User (Registration)

- **Endpoint:** `POST /api/v1/users/register`
- **Request Body:**
```json
{
  "email": "user@example.com",
  "password": "StrongPassword123!"
}
```
- **Response (201 Created):**
```json
{
  "id": 123,
  "email": "user@example.com",
  "created_at": "2026-01-05T12:00:00Z"
}
```
- **Error Responses:**
  - 400 Bad Request: Invalid input
  - 409 Conflict: Email already exists

---

## 2. Read User (Get Account Details)

- **Endpoint:** `GET /api/v1/users/me`
- **Headers:**
  - `Authorization: Bearer <token>`
- **Response (200 OK):**
```json
{
  "id": 123,
  "email": "user@example.com",
  "created_at": "2026-01-05T12:00:00Z",
  "order_history": [
    { "order_id": 1, "total": 100.0, "date": "2026-01-01T10:00:00Z" }
  ]
}
```
- **Error Responses:**
  - 401 Unauthorized: Invalid or missing token

---

## 3. Update User (Change Password)

- **Endpoint:** `PUT /api/v1/users/me/password`
- **Headers:**
  - `Authorization: Bearer <token>`
- **Request Body:**
```json
{
  "old_password": "OldPassword!",
  "new_password": "NewStrongPassword!"
}
```
- **Response (200 OK):**
```json
{
  "message": "Password updated successfully."
}
```
- **Error Responses:**
  - 400 Bad Request: Invalid input
  - 401 Unauthorized: Invalid or missing token
  - 403 Forbidden: Old password incorrect

---

## 4. Delete User (Account Deletion)

- **Endpoint:** `DELETE /api/v1/users/me`
- **Headers:**
  - `Authorization: Bearer <token>`
- **Response (204 No Content):**
  - No body
- **Error Responses:**
  - 401 Unauthorized: Invalid or missing token

---

## 5. Login

- **Endpoint:** `POST /api/v1/auth/login`
- **Request Body:**
```json
{
  "email": "user@example.com",
  "password": "StrongPassword123!"
}
```
- **Response (200 OK):**
```json
{
  "access_token": "jwt-token-string",
  "refresh_token": "refresh-token-string",
  "token_type": "bearer"
}
```
- **Error Responses:**
  - 401 Unauthorized: Invalid credentials

---

## 6. Logout

- **Endpoint:** `POST /api/v1/auth/logout`
- **Headers:**
  - `Authorization: Bearer <token>`
- **Response (200 OK):**
```json
{
  "message": "Logged out successfully."
}
```
- **Error Responses:**
  - 401 Unauthorized: Invalid or missing token

---

## Notes
- All endpoints return errors in the following format:
```json
{
  "detail": "Error message here."
}
```
- All dates/times are in ISO 8601 format (UTC).
- Passwords must meet security requirements (see registration validation).
