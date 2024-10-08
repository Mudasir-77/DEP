# -*- coding: utf-8 -*-
"""Developing RESTFULL API.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1Hn6dti58JbWffmFVZP6exOun8b12BdSd
"""

# Install necessary libraries
!pip install Flask Flask-SQLAlchemy Flask-HTTPAuth pandas

from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_httpauth import HTTPBasicAuth
import pandas as pd
from werkzeug.serving import run_simple
from threading import Thread

app = Flask(__name__)

# Configurations
app.config['SECRET_KEY'] = 'yoursecretkey'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize extensions
db = SQLAlchemy(app)
auth = HTTPBasicAuth()

# User model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)  # Store hashed passwords in real-world applications

    def __repr__(self):
        return f'<User {self.username}>'

# Authentication setup
@auth.verify_password
def verify_password(username, password):
    user = User.query.filter_by(username=username).first()
    if user and user.password == password:  # In practice, use hashed passwords
        return user
    return None

# Routes for CRUD operations
@app.route('/users', methods=['POST'])
def create_user():
    data = request.get_json()
    new_user = User(username=data['username'], email=data['email'], password=data['password'])
    db.session.add(new_user)
    db.session.commit()
    return jsonify({'message': 'User created successfully'}), 201

@app.route('/users', methods=['GET'])
def get_users():
    users = User.query.all()
    return jsonify([{'id': user.id, 'username': user.username, 'email': user.email} for user in users])

@app.route('/users/<int:id>', methods=['GET'])
def get_user(id):
    user = User.query.get_or_404(id)
    return jsonify({'id': user.id, 'username': user.username, 'email': user.email})

@app.route('/users/<int:id>', methods=['PUT'])
def update_user(id):
    data = request.get_json()
    user = User.query.get_or_404(id)
    user.username = data['username']
    user.email = data['email']
    user.password = data['password']
    db.session.commit()
    return jsonify({'message': 'User updated successfully'})

@app.route('/users/<int:id>', methods=['DELETE'])
def delete_user(id):
    user = User.query.get_or_404(id)
    db.session.delete(user)
    db.session.commit()
    return jsonify({'message': 'User deleted successfully'})

# Route to export data to CSV
@app.route('/export-users', methods=['GET'])
def export_users():
    users = User.query.all()
    user_data = [{'id': user.id, 'username': user.username, 'email': user.email} for user in users]

    # Convert the list of dictionaries to a DataFrame
    df = pd.DataFrame(user_data)

    # Save the DataFrame to a CSV file
    file_path = '/content/users_data.csv'
    df.to_csv(file_path, index=False)

    return jsonify({'message': f'User data exported to {file_path}'}), 200

# Protected route example
@app.route('/protected')
@auth.login_required
def protected():
    return jsonify({'message': f'Hello, {auth.current_user().username}!'})

# Function to run Flask app in Colab
def run_app():
    run_simple('localhost', 5001, app)  # Changed port to 5001

# Start the Flask app in a separate thread
Thread(target=run_app).start()