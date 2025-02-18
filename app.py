from flask import Flask, request, jsonify, abort
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

# ---------------------------
# Initialize the Flask App
# ---------------------------
app = Flask(__name__)

CORS(app)  # Enable CORS for all routes

# ---------------------------
# Configure the Database
# ---------------------------
# We're using SQLite for this demo. The database file will be named "passwords.db".
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///passwords.db'
# Disable extra overhead features.
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize SQLAlchemy with our Flask app
db = SQLAlchemy(app)

# ---------------------------
# Define the Database Model
# ---------------------------
# The "Password" model now only includes title, username, and password.
class Password(db.Model):
    id = db.Column(db.Integer, primary_key=True)  # Unique ID for each entry
    title = db.Column(db.String(80), nullable=False)  # Title of the entry (e.g., "GitHub")
    username = db.Column(db.String(80), nullable=False)  # Username for the service
    password = db.Column(db.String(120), nullable=False)  # The password

    def to_dict(self):
        """
        Convert the Password record to a dictionary.
        This helps when sending JSON responses.
        """
        return {
            "id": self.id,
            "title": self.title,
            "username": self.username,
            "password": self.password
        }

# ---------------------------
# API Endpoints (CRUD Operations)
# ---------------------------

# Create: Add a new password entry
@app.route('/passwords', methods=['POST'])
def create_password():
    data = request.get_json()  # Get JSON data from the request body
    # Check that required fields are present: 'title', 'username', and 'password'
    if not data or not all(key in data for key in ('title', 'username', 'password')):
        abort(400, description="Missing required fields: title, username, password")
    
    # Create a new Password instance using the provided data
    new_password = Password(
        title=data['title'],
        username=data['username'],
        password=data['password']
    )
    
    db.session.add(new_password)  # Add the new record to the session
    db.session.commit()  # Save the record to the database

    # Return the new record as JSON with a 201 Created status code
    return jsonify(new_password.to_dict()), 201

# Read: Get all password entries
@app.route('/passwords', methods=['GET'])
def get_passwords():
    passwords = Password.query.all()  # Retrieve all records from the database
    # Return the list of records as JSON
    return jsonify([p.to_dict() for p in passwords]), 200

# Read: Get a specific password entry by its ID
@app.route('/passwords/<int:id>', methods=['GET'])
def get_password(id):
    password = Password.query.get_or_404(id)  # Retrieve the record by ID or return 404 if not found
    return jsonify(password.to_dict()), 200

# Update: Modify an existing password entry
@app.route('/passwords/<int:id>', methods=['PUT'])
def update_password(id):
    password = Password.query.get_or_404(id)  # Get the record or return 404 if not found
    data = request.get_json()  # Get JSON data from the request body
    if not data:
        abort(400, description="Missing JSON body")
    
    # Update each field if it's present in the incoming data
    if 'title' in data:
        password.title = data['title']
    if 'username' in data:
        password.username = data['username']
    if 'password' in data:
        password.password = data['password']
    
    db.session.commit()  # Save changes to the database
    return jsonify(password.to_dict()), 200

# Delete: Remove a password entry
@app.route('/passwords/<int:id>', methods=['DELETE'])
def delete_password(id):
    password = Password.query.get_or_404(id)  # Get the record or return 404 if not found
    db.session.delete(password)  # Delete the record from the session
    db.session.commit()  # Commit the deletion to the database
    return jsonify({"message": "Password deleted"}), 200

# ---------------------------
# Run the Application
# ---------------------------
if __name__ == '__main__':
    # Create the database tables if they don't exist yet.
    with app.app_context():
        db.create_all()
    # Start the Flask development server.
    app.run(debug=True)
