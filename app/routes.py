# app/routes.py
from flask import current_app as app, request, abort, jsonify
from app import db
from app.models.models import Password

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
    return jsonify({"success": "Password Created"}, new_password.to_dict()), 201

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