# app/routes.py

from flask import request, jsonify, abort, current_app as app
from . import db
from .models import Password

# Create: Add a new password entry
@app.route('/passwords', methods=['POST'])
def create_password():
    data = request.get_json()
    if not data or not all(key in data for key in ('service', 'username', 'password')):
        abort(400, description="Missing required fields: service, username, password")
    
    new_password = Password(
        service=data['service'],
        username=data['username'],
        password=data['password'],
        notes=data.get('notes')
    )
    db.session.add(new_password)
    db.session.commit()
    return jsonify(new_password.to_dict()), 201

# Read: Get all password entries
@app.route('/passwords', methods=['GET'])
def get_passwords():
    passwords = Password.query.all()
    return jsonify([p.to_dict() for p in passwords]), 200

# Read: Get a specific password entry by id
@app.route('/passwords/<int:id>', methods=['GET'])
def get_password(id):
    password = Password.query.get_or_404(id)
    return jsonify(password.to_dict()), 200

# Update: Modify an existing password entry
@app.route('/passwords/<int:id>', methods=['PUT'])
def update_password(id):
    password = Password.query.get_or_404(id)
    data = request.get_json()
    if not data:
        abort(400, description="Missing JSON body")
    
    if 'service' in data:
        password.service = data['service']
    if 'username' in data:
        password.username = data['username']
    if 'password' in data:
        password.password = data['password']
    if 'notes' in data:
        password.notes = data['notes']
    
    db.session.commit()
    return jsonify(password.to_dict()), 200

# Delete: Remove a password entry
@app.route('/passwords/<int:id>', methods=['DELETE'])
def delete_password(id):
    password = Password.query.get_or_404(id)
    db.session.delete(password)
    db.session.commit()
    return jsonify({"message": "Password deleted"}), 200
