# enrollment_service.py
from flask import Flask, jsonify, request, render_template
import requests
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# URLs of the other microservices
DB_URL = "http://127.0.0.1:5000"
NOTIFY_URL = "http://127.0.0.1:5003"

# --- UI Endpoint ---
@app.route('/')
def index():
    """Serves the main HTML page."""
    return render_template('index.html')

# --- Facade API Endpoints ---
@app.route('/enroll', methods=['POST'])
def enroll_student():
    """Facade method to handle the complex enrollment process."""
    data = request.json
    student_id = data['student_id']
    course_id = data['course_id']
    
    # 1. Get all required data from the database service first
    try:
        db_data_res = requests.get(f"{DB_URL}/data")
        db_data_res.raise_for_status()
        db_data = db_data_res.json()
        
        student = db_data.get('users', {}).get(student_id)
        course = db_data.get('courses', {}).get(course_id)
        all_enrollments = db_data.get('enrollments', {})
        all_waitlists = db_data.get('waitlists', {})

    except requests.exceptions.RequestException as e:
        return jsonify({"error": f"Could not connect to database service: {e}"}), 503

    # 2. Validate that the student and course exist
    if not student or not course:
        return jsonify({"error": f"Student ID '{student_id}' or Course ID '{course_id}' not found. Please add them first."}), 404

    # 3. Core Logic: Check for enrollment, capacity, and waitlisting
    student_enrollments = all_enrollments.get(student_id, [])
    if course_id in student_enrollments:
        return jsonify({"message": f"{student['name']} is already enrolled in {course['name']}."}), 200
        
    enrolled_count = sum(1 for elist in all_enrollments.values() if course_id in elist)
    
    # --- THIS IS THE CORRECTED LOGIC BLOCK ---
    if enrolled_count >= course['capacity']:
        # Course is full, handle waitlisting.
        course_waitlist = all_waitlists.get(course_id, [])
        
        if student_id in course_waitlist:
            return jsonify({"message": f"{student['name']} is already on the waitlist for {course['name']}."}), 200
        else:
            # Add the student to the waitlist and update the DB
            course_waitlist.append(student_id)
            try:
                # Make the API call to update the waitlist in the database
                requests.post(f"{DB_URL}/waitlist", json={"course_id": course_id, "students": course_waitlist})
                return jsonify({"message": f"Course is full. Successfully added {student['name']} to the waitlist for {course['name']}."}), 200
            except requests.exceptions.RequestException as e:
                return jsonify({"error": f"Failed to update waitlist: {e}"}), 503
    
    # 4. Success: If not full, perform enrollment and update the DB
    student_enrollments.append(course_id)
    try:
        requests.post(f"{DB_URL}/enrollments", json={"student_id": student_id, "courses": student_enrollments})
        return jsonify({"message": f"Successfully enrolled {student['name']} in {course['name']}."}), 200
    except requests.exceptions.RequestException as e:
        return jsonify({"error": f"Failed to update enrollments: {e}"}), 503
    
@app.route('/drop', methods=['POST'])
def drop_course():
    """Facade method to handle dropping a course and notifying waitlisters."""
    data = request.json
    student_id, course_id = data['student_id'], data['course_id']

    # 1. Get all current data from the database
    try:
        db_data_res = requests.get(f"{DB_URL}/data")
        db_data_res.raise_for_status()
        db_data = db_data_res.json()
        
        all_enrollments = db_data.get('enrollments', {})
        student_enrollments = all_enrollments.get(student_id, [])
    except requests.exceptions.RequestException as e:
        return jsonify({"error": f"Could not connect to database service: {e}"}), 503

    # 2. Validate that the student is actually enrolled
    if course_id not in student_enrollments:
        return jsonify({"error": f"Student '{student_id}' is not enrolled in this course."}), 400

    # 3. Perform the drop action
    student_enrollments.remove(course_id)
    requests.post(f"{DB_URL}/enrollments", json={"student_id": student_id, "courses": student_enrollments})

    # 4. OBSERVER PATTERN TRIGGER: Check waitlist and notify
    all_waitlists = db_data.get('waitlists', {})
    if course_id in all_waitlists and all_waitlists[course_id]:
        student_to_notify_id = all_waitlists[course_id][0]
        student_to_notify = db_data.get('users', {}).get(student_to_notify_id)
        course = db_data.get('courses', {}).get(course_id)
        
        if student_to_notify and course:
            notification_payload = {
                "user_id": student_to_notify['user_id'],
                "user_name": student_to_notify['name'],
                "message": f"A spot has opened up in {course['name']}! Please try to enroll."
            }
            requests.post(f"{NOTIFY_URL}/notify", json=notification_payload)
            
            return jsonify({"status": "Success", "message": f"Student unenrolled. {student_to_notify['name']} has been notified from the waitlist."})

    # --- THIS MESSAGE HAS BEEN CORRECTED ---
    return jsonify({"status": "Success", "message": "Student unenrolled successfully. The course waitlist was empty."})

@app.route('/system_data', methods=['GET'])
def get_system_data():
    """
    Acts as a proxy to fetch all data from the database service.
    This gives the UI a single endpoint to get a snapshot of the system state.
    """
    try:
        response = requests.get(f"{DB_URL}/data")
        response.raise_for_status()  # Will raise an exception for 4xx/5xx errors
        return jsonify(response.json())
    except requests.exceptions.RequestException as e:
        print(f"Error connecting to database service: {e}")
        return jsonify({"error": "Could not fetch data from the database service."}), 503


if __name__ == '__main__':
    # Runs on port 5004
    app.run(port=5004, debug=True)