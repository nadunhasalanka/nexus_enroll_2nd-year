# user_service.py
from flask import Flask, request, jsonify
import requests
from flask_cors import CORS # Import CORS

# The Factory Pattern implementation remains the same
from abc import ABC, abstractmethod

class User(ABC):
    def __init__(self, user_id, name):
        self.user_id = user_id
        self.name = name
    @abstractmethod
    def get_role(self): pass
    def to_dict(self):
        return {"user_id": self.user_id, "name": self.name, "role": self.get_role()}

class Student(User):
    def get_role(self): return "Student"

class Faculty(User):
    def get_role(self): return "Faculty"

class Administrator(User):
    def get_role(self): return "Administrator"

class ConcreteUserFactory:
    def create_user(self, user_type, user_id, name):
        if user_type.lower() == 'student': return Student(user_id, name)
        if user_type.lower() == 'faculty': return Faculty(user_id, name)
        if user_type.lower() == 'administrator': return Administrator(user_id, name)
        raise ValueError(f"Unknown user type: {user_type}")

app = Flask(__name__)
CORS(app)
user_factory = ConcreteUserFactory()
DB_SERVICE_URL = "http://127.0.0.1:5000"

@app.route('/users', methods=['POST'])
def create_user_endpoint():
    data = request.json
    try:
        # 1. Use the factory to create a user object
        new_user = user_factory.create_user(data['type'], data['user_id'], data['name'])
        
        # 2. Persist it by calling the database service
        response = requests.post(f"{DB_SERVICE_URL}/users", json=new_user.to_dict())
        
        if response.status_code == 201:
            return jsonify({"message": f"{new_user.get_role()} created successfully.", "user": new_user.to_dict()}), 201
        else:
            return jsonify({"error": "Failed to save user in db service"}), 500
    except (ValueError, KeyError) as e:
        return jsonify({"error": str(e)}), 400

if __name__ == '__main__':
    # Runs on port 5001
    app.run(port=5001, debug=True)