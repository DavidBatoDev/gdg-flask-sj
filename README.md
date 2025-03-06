# Password Manager API

## Introduction
This project is a simple Password Manager API built with Flask. It is designed to teach the fundamentals of backend development as part of the **Google On Campus PUP Web Development Department** curriculum. The API allows users to create, read, update, and delete (CRUD) password entries using an SQLite database.

## Features
- **Create Password Entries**: Store login credentials with a title, username, and password.
- **Retrieve Password Entries**: Fetch all stored credentials or a specific one using an ID.
- **Update Password Entries**: Modify existing credentials.
- **Delete Password Entries**: Remove credentials from the database.
- **CORS Enabled**: Allows interaction with frontend applications.

## Technologies Used
- Python
- Flask
- Flask-SQLAlchemy (for database management)
- Flask-CORS (for cross-origin requests)
- SQLite (as the database)

## Installation and Setup

### Prerequisites
Ensure you have Python installed on your system. You can download it from [python.org](https://www.python.org/downloads/).

### Steps to Run the Project
1. **Clone the repository**  
    ```
    git clone <repository_url>
    cd <repository_folder>
    ```
2. **Create a virtual environment (optional but recommended)**  
    ```
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```
3. **Install dependencies**  
    ```
    pip install flask flask-sqlalchemy flask-cors
    ```
4. **Run the application**  
    ```
    python app.py
    ```
5. The API will be available at `http://127.0.0.1:5000/`

## API Endpoints

### Create a Password Entry
- **Endpoint:** `POST /passwords`
- **Request Body:**
    ```json
    {
      "title": "GitHub",
      "username": "user123",
      "password": "securepassword"
    }
    ```
- **Response:**
    ```json
    {
      "id": 1,
      "title": "GitHub",
      "username": "user123",
      "password": "securepassword"
    }
    ```

### Retrieve All Password Entries
- **Endpoint:** `GET /passwords`
- **Response:**
    ```json
    [
      {
        "id": 1,
        "title": "GitHub",
        "username": "user123",
        "password": "securepassword"
      }
    ]
    ```

### Retrieve a Specific Password Entry
- **Endpoint:** `GET /passwords/<id>`
- **Example:** `GET /passwords/1`
- **Response:**
    ```json
    {
      "id": 1,
      "title": "GitHub",
      "username": "user123",
      "password": "securepassword"
    }
    ```

### Update a Password Entry
- **Endpoint:** `PUT /passwords/<id>`
- **Example:** `PUT /passwords/1`
- **Request Body:**
    ```json
    {
      "password": "newsecurepassword"
    }
    ```
- **Response:**
    ```json
    {
      "id": 1,
      "title": "GitHub",
      "username": "user123",
      "password": "newsecurepassword"
    }
    ```

### Delete a Password Entry
- **Endpoint:** `DELETE /passwords/<id>`
- **Example:** `DELETE /passwords/1`
- **Response:**
    ```json
    {
      "message": "Password deleted"
    }
    ```

## Notes
- The application starts by creating the database if it doesn’t already exist.
- It runs on **Flask’s development server**, which is not suitable for production use.
- You can modify the database configuration in `app.config['SQLALCHEMY_DATABASE_URI']` if needed.

## License
This project is intended for educational purposes only and is part of the **Google On Campus PUP Web Development Department** curriculum.
