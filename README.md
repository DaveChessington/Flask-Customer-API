## Customer Management System

This project is a Customer Management System that provides a REST API and a web interface to manage customer data.

The system allows users to:
- Create new customers
- View customer info
- Update existing records
- Delete customers
- Authenticate users through a login system

The architecture is divided into two parts:
- **API layer (Flask):** Handles business logic, validation, and database operations.
- **Client layer (Flask UI):** Provides web forms that consume the API using HTTP requests.

Currently, the system works with a **local database**, with support planned for **AWS RDS** integration.

### Features
- RESTful endpoints for CRUD operations
- Password encryption for security
- Login validation through API
- Form-based web interface
- Error handling and status code management

### Technologies Used
- Python
- Flask
- SQLite (local)
- Requests library
- HTML + Bootstrap

### Future Improvements
- AWS dynamo db integration and use of lambdas
- Session management and authentication
