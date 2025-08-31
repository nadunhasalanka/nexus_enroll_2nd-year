# run_simulation.py
from user_service.service import UserService
from course_service.service import CourseService
from enrollment_service.service import EnrollmentFacade
from shared_db.singleton_db import db

def populate_initial_data():
    """Sets up the initial state of the university system."""
    print("--- POPULATING INITIAL UNIVERSITY DATA ---")
    user_service = UserService()
    course_service = CourseService()

    # Add Users
    user_service.add_user('student', 'S001', 'Alice')
    user_service.add_user('student', 'S002', 'Bob')
    user_service.add_user('student', 'S003', 'Charlie')
    user_service.add_user('faculty', 'F001', 'Dr. Einstein')
    user_service.add_user('administrator', 'A001', 'Admin Smith')

    # Add Courses
    course_service.add_course('CS101', 'Intro to Python', 2) # Small capacity for testing
    course_service.add_course('MA202', 'Calculus II', 20)
    print("--- INITIAL DATA POPULATED ---")

def main():
    """Main simulation function demonstrating all features."""
    
    # Clean slate before running
    db.clear_data()
    populate_initial_data()

    # The Facade is the single point of entry for enrollment operations
    enrollment_system = EnrollmentFacade()

    # --- Use Case 1: Successful Enrollments ---
    enrollment_system.enroll_student('S001', 'CS101') # Alice enrolls
    enrollment_system.enroll_student('S002', 'CS101') # Bob enrolls
    enrollment_system.enroll_student('S001', 'MA202') # Alice enrolls in another course

    # --- Use Case 2: Course is Full, Student gets Waitlisted (Facade handles complexity) ---
    enrollment_system.enroll_student('S003', 'CS101') # Charlie tries to enroll, gets waitlisted

    # --- Use Case 3: Faculty Views Course Roster ---
    enrollment_system.get_faculty_roster('F001', 'CS101')

    # --- Use Case 4: Student drops a course, triggering Observer pattern ---
    # Alice drops CS101. This should free up a spot.
    # The Course (Subject) should notify the first person on the waitlist (Charlie, the Observer).
    enrollment_system.drop_course('S001', 'CS101')

    # --- Use Case 5: Student Views Updated Schedule ---
    enrollment_system.get_student_schedule('S001') # Alice's updated schedule
    enrollment_system.get_student_schedule('S003') # Charlie is still not enrolled yet, just notified

    # --- Use Case 6: Administrator generates a report ---
    # Let's enroll Bob in MA202 to push its capacity over 0% for the report
    enrollment_system.enroll_student('S002', 'MA202')
    course_service = CourseService()
    course_service.generate_capacity_report(threshold=0.05) # Low threshold to ensure it appears

if __name__ == "__main__":
    main()