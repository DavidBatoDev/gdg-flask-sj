# app/models/models.py

from datetime import datetime
from app import db

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