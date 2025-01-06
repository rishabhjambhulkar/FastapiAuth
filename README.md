### Installation Guide and Running FastAPI Application

#### 1. **Installation Guide**

To set up and run the FastAPI application, follow these steps:

##### Step 1: Install Dependencies

1. Clone the repository or download the project:
   ```bash
   git clone https://github.com/your-repository.git
   cd your-repository
   ```

2. Navigate to the project directory and create a virtual environment:
   ```bash
   python -m venv venv
   ```

3. Activate the virtual environment:
   - On Windows:
     ```bash
     .\venv\Scripts\activate
     ```
   - On macOS/Linux:
     ```bash
     source venv/bin/activate
     ```

4. Install the dependencies from the `requirements.txt` file:
   ```bash
   pip install -r requirements.txt
   ```

##### Step 2: Run FastAPI Application

1. Make sure your database (e.g., PostgreSQL, SQLite, or any other database) is set up and running.

2. Start the FastAPI server:
   ```bash
   uvicorn main:app --reload
   ```

3. Access the FastAPI application at:
   - `http://localhost:8000`

---


---

This setup will allow you to run and test the FastAPI application effectively.

### FastAPI API Documentation for User Management and Authentication

#### Overview
This document provides details for testing the `Users` and `Auth` endpoints in the FastAPI application. The API routes handle user creation, retrieval of user details, authentication, and token refreshing.

---

### API Routes

#### 1. **Create User**
- **Endpoint**: `POST /users`
- **Description**: Creates a new user account.
- **Request Body**: 
  - **Content Type**: `application/json`
  - **Schema**: `CreateUserRequest`
  
  Example Request:
  ```json
  {
    "name": "example_user",
    "email": "example@example.com",
    "password": "securepassword123"
  }
  ```

- **Response**: 
  - **Status Code**: `201 Created`
  - **Content**: 
    ```json
    {
      "message": "User account has been successfully created."
    }
    ```

---

#### 2. **Get User Details**
- **Endpoint**: `POST /users/details`
- **Description**: User details by authenticating the access token.
- **Headers**:
  - `access-token: <refresh_token>`
  
  Example Request:
  ```bash
  curl -X POST http://<base_url>/users/details -H "Authorization: Bearer <access_token>"
  ```

- **Response**:
  - **Status Code**: `200 OK`
  - **Content**:
    ```json
    {
      "id": 1,
      "name": "example_user",
      "email": "example@example.com"
    }
    ```

---

#### 3. **Authenticate User**
- **Endpoint**: `POST /auth/login`
- **Description**: Authenticates the user and provides access and refresh tokens.
- **Request Body**: 
  - **Content Type**: `application/json`
  - **Schema**: `LoginRequest`
  
  Example Request:
  ```json
  {
    "email": "example@example.com",
    "password": "securepassword123"
  }
  ```

- **Response**: 
  - **Status Code**: `200 OK`
  - **Content**: 
    ```json
    {
      "token": {
        "access_token": "<token_value>",
        "refresh_token": "<refresh_token_value>",
        "expires_in": <expiration_time>
      }
    }
    ```

- **Cookies**:
  - `access_token`: Secure token set in cookies with `httponly=True` and expiration time.
  - `refresh_token`: Secure refresh token set in cookies with `httponly=True`.

---

#### 4. **Refresh Access Token**
- **Endpoint**: `POST /auth/refresh`
- **Description**: Refreshes the access token using the refresh token.
- **Headers**:
  - `refresh-token: <refresh_token>`

- **Response**:
  - **Status Code**: `200 OK`
  - **Content**: 
    ```json
    {
      "token": {
        "access_token": "<new_access_token>",
        "expires_in": <new_expiration_time>
      }
    }
    ```

---

### Error Handling
- **401 Unauthorized**: 
  - Invalid email or password for login.
  - Example:
    ```json
    {
      "detail": "Invalid email or password",
      "status_code": 401
    }
    ```

---

### Dependencies and Security
- **Dependency**: 
  - `db: Session = Depends(getDb)` – Provides the database session.
  - `access_token: str = Header()` – Authentication using access token.
  - `refresh_token: str = Header()` – Used for refreshing tokens.

---

