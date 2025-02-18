from flask import Flask, request, jsonify, abort
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

# Initialize the Flask app
app = Flask(__name__)

# Configure the database URI (using SQLite for this demo)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///passwords.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize SQLAlchemy with the app
db = SQLAlchemy(app)

# Define the Password model
class Password(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    service = db.Column(db.String(80), nullable=False)
    username = db.Column(db.String(80), nullable=False)
    password = db.Column(db.String(120), nullable=False)  # In real-world, encrypt this!
    notes = db.Column(db.String(200), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            "id": self.id,
            "service": self.service,
            "username": self.username,
            "password": self.password,
            "notes": self.notes,
            "created_at": self.created_at.isoformat()
        }

# -----------------------------------
# CRUD API Endpoints for the Passwords
# -----------------------------------

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

# -----------------------------------
# Run the Application
# -----------------------------------
if __name__ == '__main__':
    # Create database tables if they don't exist yet
    db.create_all()
    app.run(debug=True)
