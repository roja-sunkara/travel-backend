# models.py

from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin

# Create the SQLAlchemy instance
db = SQLAlchemy()

# Define the User model
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)  # Unique user ID
    username = db.Column(db.String(80), unique=True, nullable=False)  # Username
    email = db.Column(db.String(120), unique=True, nullable=False)  # Email address
    password = db.Column(db.String(120), nullable=False)  # Hashed password

    def __repr__(self):
        return f'<User {self.username}>'
