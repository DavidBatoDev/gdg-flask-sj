# app/routes.py

from flask import request, jsonify, abort, current_app as app
from . import db
from .models import Password

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