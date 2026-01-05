# Unit Test Cases for Registration API Endpoint (RETAIL-10)

| Test Case Name                      | Description                                                        | Input Example                                      | Expected Output / Assertion                        |
|-------------------------------------|--------------------------------------------------------------------|----------------------------------------------------|----------------------------------------------------|
| test_api_accepts_valid_data         | API accepts valid registration data                                | {"email": "user1@example.com", "password": "StrongPass1!"} | 201 Created, user created, correct response body   |
| test_api_rejects_duplicate_email    | API rejects registration with duplicate email                      | {"email": "existing@example.com", "password": "StrongPass1!"} | 409 Conflict, error message about duplicate email  |
| test_api_rejects_invalid_email      | API rejects invalid email format                                   | {"email": "bademail", "password": "StrongPass1!"}           | 400 Bad Request, error message about email format  |
| test_api_rejects_weak_password      | API rejects weak password not meeting policy                       | {"email": "user2@example.com", "password": "123"}           | 400 Bad Request, error message about password      |
| test_api_missing_email_field        | API rejects missing email field                                    | {"password": "StrongPass1!"}                                 | 400 Bad Request, error about missing email         |
| test_api_missing_password_field     | API rejects missing password field                                 | {"email": "user3@example.com"}                                 | 400 Bad Request, error about missing password      |
| test_api_empty_payload              | API rejects empty request payload                                  | {}                                                 | 400 Bad Request, error about missing fields        |
| test_api_trims_whitespace           | API trims whitespace in email and password fields                  | {"email": " user4@example.com ", "password": " StrongPass1! "} | 201 Created, user created, trimmed values stored   |
| test_api_handles_long_email         | API rejects excessively long email                                 | {"email": "a...@example.com", "password": "StrongPass1!"}    | 400 Bad Request, error about email length          |
| test_api_handles_long_password      | API rejects excessively long password                              | {"email": "user5@example.com", "password": "a...a"}         | 400 Bad Request, error about password length       |
| test_api_returns_json_content_type  | API always returns JSON content type                               | {"email": "user6@example.com", "password": "StrongPass1!"}  | Response header Content-Type: application/json     |
| test_api_handles_concurrent_signup  | API handles concurrent registration attempts for same email        | Multiple requests with same email                  | Only one succeeds, others get 409 Conflict         |
| test_api_returns_error_structure    | API returns error in standard format                               | Invalid input                                      | {"detail": "..."} in response body               |
| test_api_db_failure_handling        | API returns 500 on database failure                                | Valid input, DB down                               | 500 Internal Server Error, error message           |
| test_api_rate_limit                 | API enforces rate limiting on registration endpoint                | Rapid repeated requests                            | 429 Too Many Requests, error message               |

---

- All tests should mock external dependencies (DB, email, etc.) as needed.
- Security and edge cases are included for comprehensive coverage.
