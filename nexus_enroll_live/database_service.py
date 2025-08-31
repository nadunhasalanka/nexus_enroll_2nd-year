from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app) 

# This dictionary acts as our in-memory database.
db = {
    "users": {},
    "courses": {},
    "enrollments": {}, 
    "waitlists": {}
}

@app.route('/data', methods=['GET'])
def get_all_data():
    """Endpoint to view the entire database state."""
    return jsonify(db)

@app.route('/clear', methods=['POST'])
def clear_data():
    """Endpoint to reset the database."""
    global db
    db = {"users": {}, "courses": {}, "enrollments": {}, "waitlists": {}}
    return jsonify({"message": "Database cleared."})

# --- User Data Endpoints ---
@app.route('/users', methods=['POST'])
def add_user():
    user_data = request.json
    db['users'][user_data['user_id']] = user_data
    return jsonify(user_data), 201

@app.route('/users/<user_id>', methods=['GET'])
def get_user(user_id):
    return jsonify(db['users'].get(user_id))

# --- Course Data Endpoints ---
@app.route('/courses', methods=['POST'])
def add_course():
    course_data = request.json
    db['courses'][course_data['course_id']] = course_data
    return jsonify(course_data), 201

@app.route('/courses/<course_id>', methods=['GET'])
def get_course(course_id):
    return jsonify(db['courses'].get(course_id))

# --- Enrollment and Waitlist Endpoints ---
@app.route('/enrollments', methods=['GET'])
def get_enrollments():
    return jsonify(db['enrollments'])
    
@app.route('/enrollments', methods=['POST'])
def update_enrollments():
    enrollment_data = request.json
    student_id = enrollment_data['student_id']
    db['enrollments'][student_id] = enrollment_data['courses']
    return jsonify(db['enrollments'][student_id])

@app.route('/waitlist', methods=['POST'])
def update_waitlist():
    waitlist_data = request.json
    course_id = waitlist_data['course_id']
    db['waitlists'][course_id] = waitlist_data['students']
    return jsonify(db['waitlists'][course_id])

if __name__ == '__main__':
    # Runs on port 5000
    app.run(port=5000, debug=True)