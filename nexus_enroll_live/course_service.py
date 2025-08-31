# course_service.py
from flask import Flask, request, jsonify
import requests
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
DB_SERVICE_URL = "http://127.0.0.1:5000"

@app.route('/courses', methods=['POST'])
def create_course_endpoint():
    data = request.json
    try:
        # In a real app, you'd have a Course class, but for simplicity we use a dict
        course_data = {
            "course_id": data['course_id'],
            "name": data['name'],
            "capacity": int(data['capacity'])
        }
        response = requests.post(f"{DB_SERVICE_URL}/courses", json=course_data)
        if response.status_code == 201:
            return jsonify({"message": "Course created successfully.", "course": course_data}), 201
        else:
            return jsonify({"error": "Failed to save course"}), 500
    except (ValueError, KeyError) as e:
        return jsonify({"error": str(e)}), 400

if __name__ == '__main__':
    # Runs on port 5002
    app.run(port=5002, debug=True)