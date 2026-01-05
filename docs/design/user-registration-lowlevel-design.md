# User Registration Low-Level Design

## 1. Class Diagram (PlantUML)

```plantuml
@startuml
class RegistrationDTO {
  +email: str
  +password: str
}

class UserService {
  +register_user(email: str, password: str)
}

class UserRepository {
  +get_by_email(email: str)
  +create_user(email: str, password_hash: str)
}

RegistrationDTO --> UserService : used by
UserService --> UserRepository : uses
@enduml
```

---

## 2. Sequence Diagram (PlantUML)

```plantuml
@startuml
actor User
participant "RegistrationAPI\n(FastAPI endpoint)" as API
participant UserService
participant UserRepository

User -> API: POST /register (email, password)
API -> API: Validate input (Pydantic)
API -> UserService: register_user(email, password)
UserService -> UserRepository: get_by_email(email)
UserRepository --> UserService: user/None
UserService -> UserService: hash password (if user not exists)
UserService -> UserRepository: create_user(email, password_hash)
UserRepository --> UserService: user created
UserService --> API: success/error
API --> User: response
@enduml
```

---

## 3. Design Notes
- Input validation is handled by Pydantic models.
- Business logic (uniqueness, password policy, hashing) is in `UserService`.
- Database access is abstracted in `UserRepository`.
- API endpoint orchestrates the flow and returns appropriate responses.
