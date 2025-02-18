from flask import Flask, request, jsonify, abort
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

# ---------------------------
# Initialize the Flask App
# ---------------------------
app = Flask(__name__)

# ---------------------------
# Configure the Database
# ---------------------------
# We're using SQLite for this demo. The database file will be named "passwords.db".
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///passwords.db'
# Disable a feature that we don't need to avoid extra overhead.
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize SQLAlchemy with our Flask app
db = SQLAlchemy(app)

# ---------------------------
# Define the Database Model
# ---------------------------
# This "Password" class represents our table in the database.
class Password(db.Model):
    id = db.Column(db.Integer, primary_key=True)  # A unique ID for each password entry
    service = db.Column(db.String(80), nullable=False)  # The name of the service (e.g., "GitHub")
    username = db.Column(db.String(80), nullable=False)  # The username for the service
    password = db.Column(db.String(120), nullable=False)  # The password (note: encrypt in real apps!)
    notes = db.Column(db.String(200), nullable=True)  # Additional notes (this field is optional)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)  # Timestamp when the entry was created

    def to_dict(self):
        """
        Convert the Password record to a dictionary.
        This makes it easy to convert our record into JSON when sending a response.
        """
        return {
            "id": self.id,
            "service": self.service,
            "username": self.username,
            "password": self.password,
            "notes": self.notes,
            "created_at": self.created_at.isoformat()
        }

# ---------------------------
# API Endpoints (CRUD Operations)
# ---------------------------

# Create: Add a new password entry
@app.route('/passwords', methods=['POST'])
def create_password():
    data = request.get_json()  # Get JSON data from the request body
    # Check that required fields are present: 'service', 'username', and 'password'
    if not data or not all(key in data for key in ('service', 'username', 'password')):
        abort(400, description="Missing required fields: service, username, password")
    
    # Create a new Password instance with the data provided
    new_password = Password(
        service=data['service'],
        username=data['username'],
        password=data['password'],
        notes=data.get('notes')  # Use .get() for optional fields (returns None if not provided)
    )
    
    db.session.add(new_password)  # Add the new record to our database session
    db.session.commit()  # Save the record to the database

    # Return the new record in JSON format with a 201 Created status code
    return jsonify(new_password.to_dict()), 201

# Read: Get all password entries
@app.route('/passwords', methods=['GET'])
def get_passwords():
    passwords = Password.query.all()  # Retrieve all password records from the database
    # Convert each record to a dictionary and return them as a list in JSON format
    return jsonify([p.to_dict() for p in passwords]), 200

# Read: Get a specific password entry by its ID
@app.route('/passwords/<int:id>', methods=['GET'])
def get_password(id):
    password = Password.query.get_or_404(id)  # Retrieve the record by ID or return a 404 error if not found
    return jsonify(password.to_dict()), 200

# Update: Modify an existing password entry
@app.route('/passwords/<int:id>', methods=['PUT'])
def update_password(id):
    password = Password.query.get_or_404(id)  # Get the existing record or 404 if not found
    data = request.get_json()  # Get JSON data from the request body
    if not data:
        abort(400, description="Missing JSON body")
    
    # Update each field if it's present in the incoming data
    if 'service' in data:
        password.service = data['service']
    if 'username' in data:
        password.username = data['username']
    if 'password' in data:
        password.password = data['password']
    if 'notes' in data:
        password.notes = data['notes']
    
    db.session.commit()  # Save changes to the database
    return jsonify(password.to_dict()), 200

# Delete: Remove a password entry
@app.route('/passwords/<int:id>', methods=['DELETE'])
def delete_password(id):
    password = Password.query.get_or_404(id)  # Get the record to delete or 404 if not found
    db.session.delete(password)  # Mark the record for deletion
    db.session.commit()  # Commit the deletion to the database
    return jsonify({"message": "Password deleted"}), 200

# ---------------------------
# Run the Application
# ---------------------------
if __name__ == '__main__':
    # Create the database tables if they don't exist yet.
    # We use "app.app_context()" to make sure we have the right context.
    with app.app_context():
        db.create_all()
    # Start the Flask development server. The debug=True flag provides helpful error messages.
    app.run(debug=True)
