# Epic: User Registration & Login

**Description:**
Enable customers to create an account, log in securely, and access their account and order history.

**Acceptance Criteria:**
- Customers can register with email and password.
- Customers can log in with valid credentials.
- Invalid login attempts are handled securely.
- Users can access their account and order history after login.

---

## Story: User Registration
**Description:**
Allow new users to create an account using their email and password.

**Acceptance Criteria:**
- Registration form is available with email and password fields.
- Email must be unique and valid.
- Password must meet security requirements.
- Successful registration logs the user in.
- Errors are shown for invalid or duplicate emails.

**Unit Test Cases:**
- test_registration_form_renders: Registration form is displayed.
- test_registration_success: User can register with valid email and password.
- test_registration_duplicate_email: Duplicate email registration is rejected.
- test_registration_invalid_email: Invalid email format is rejected.
- test_registration_weak_password: Weak passwords are rejected.

### Subtask: Registration Form UI
**Description:**
Implement the frontend registration form with validation.

**Acceptance Criteria:**
- Form fields for email and password are present.
- Client-side validation for email and password.
- Submit button is disabled until form is valid.

**Unit Test Cases:**
- test_form_fields_present: Email and password fields are rendered.
- test_client_side_validation: Invalid input shows error messages.
- test_submit_button_disabled: Submit is disabled for invalid form.

### Subtask: Registration API Endpoint
**Description:**
Create backend API to handle user registration.

**Acceptance Criteria:**
- Accepts email and password.
- Validates input and checks for duplicates.
- Returns success or error response.

**Unit Test Cases:**
- test_api_accepts_valid_data: API accepts valid registration data.
- test_api_rejects_duplicate_email: API rejects duplicate emails.
- test_api_rejects_invalid_data: API rejects invalid input.

### Subtask: Store User in Database
**Description:**
Persist new user data securely in the database.

**Acceptance Criteria:**
- User data is stored with hashed password.
- No plaintext passwords are stored.
- User record is created only on successful registration.

**Unit Test Cases:**
- test_user_saved_with_hashed_password: Password is hashed in DB.
- test_no_plaintext_password: No plaintext password in DB.
- test_user_record_created: User record exists after registration.

---

## Story: User Login
**Description:**
Allow registered users to log in with their email and password.

**Acceptance Criteria:**
- Login form is available with email and password fields.
- Users can log in with valid credentials.
- Invalid credentials show error messages.
- Successful login grants access to account and order history.

**Unit Test Cases:**
- test_login_form_renders: Login form is displayed.
- test_login_success: User can log in with valid credentials.
- test_login_invalid_credentials: Invalid login is rejected.
- test_login_error_message: Error message shown for invalid login.

### Subtask: Login Form UI
**Description:**
Implement the frontend login form with validation.

**Acceptance Criteria:**
- Form fields for email and password are present.
- Client-side validation for required fields.
- Error messages for invalid input.

**Unit Test Cases:**
- test_form_fields_present: Email and password fields are rendered.
- test_client_side_validation: Invalid input shows error messages.
- test_error_message_display: Error message appears on invalid login.

### Subtask: Login API Endpoint
**Description:**
Create backend API to handle user login and authentication.

**Acceptance Criteria:**
- Accepts email and password.
- Validates credentials against stored data.
- Returns authentication token on success.
- Returns error on failure.

**Unit Test Cases:**
- test_api_accepts_valid_credentials: API accepts valid login.
- test_api_rejects_invalid_credentials: API rejects invalid login.
- test_api_returns_token: Token is returned on successful login.

### Subtask: Session Management
**Description:**
Manage user session after successful login.

**Acceptance Criteria:**
- Session or JWT token is issued on login.
- User remains logged in across pages.
- Session expires after logout or timeout.

**Unit Test Cases:**
- test_token_issued_on_login: Token/session is created on login.
- test_session_persistence: User remains logged in.
- test_session_expiry: Session expires correctly.

---

## Story: View Account & Order History
**Description:**
Allow logged-in users to view their account details and order history.

**Acceptance Criteria:**
- Users can access account page after login.
- Order history is displayed for the logged-in user.
- Access is restricted to authenticated users only.

**Unit Test Cases:**
- test_account_page_accessible: Account page loads for logged-in user.
- test_order_history_display: Order history is shown.
- test_access_restricted: Unauthenticated users cannot access account page.

### Subtask: Account Page UI
**Description:**
Implement frontend for account details and order history.

**Acceptance Criteria:**
- Account details and order history are displayed.
- Proper loading and error states are handled.

**Unit Test Cases:**
- test_account_details_render: Account details are rendered.
- test_order_history_render: Order history is rendered.
- test_error_state_handling: Error state is handled gracefully.

### Subtask: Account API Endpoint
**Description:**
Create backend API to fetch account details and order history.

**Acceptance Criteria:**
- Returns user account details and order history for authenticated user.
- Returns error for unauthenticated requests.

**Unit Test Cases:**
- test_api_returns_account_details: API returns correct account data.
- test_api_returns_order_history: API returns correct order history.
- test_api_rejects_unauthenticated: API rejects unauthenticated requests.
