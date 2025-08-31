# enrollment_service/service.py
from shared_db.singleton_db import db
from course_service.service import CourseService
from user_service.service import UserService

class EnrollmentFacade:
    """
    Facade Design Pattern: Simplifies the complex enrollment subsystem.
    A client interacts with this facade rather than the individual services.
    """
    def __init__(self):
        self.course_service = CourseService()
        self.user_service = UserService()
        print("\nEnrollmentFacade initialized.")

    def enroll_student(self, student_id, course_id):
        """A single, simple method to handle the entire enrollment process."""
        print(f"\n--- Attempting to enroll Student {student_id} in Course {course_id} ---")
        student = self.user_service.get_user(student_id)
        course = self.course_service.get_course(course_id)

        if not student or not course:
            print("Error: Invalid student or course ID.")
            return False

        # 1. Check if already enrolled
        if student_id in db.enrollments and course_id in db.enrollments[student_id]:
            print(f"Result: {student.name} is already enrolled in {course.name}.")
            return False

        # 2. Check for capacity
        enrolled_count = self.course_service.get_enrolled_count(course_id)
        if enrolled_count >= course.capacity:
            # Capacity is full, add to waitlist
            if course_id not in db.waitlists:
                db.waitlists[course_id] = []
            if student_id not in db.waitlists[course_id]:
                db.waitlists[course_id].append(student_id)
                course.attach(student) # Attach student as an observer
                print(f"Result: {course.name} is full. {student.name} has been added to the waitlist.")
            else:
                print(f"Result: {student.name} is already on the waitlist for {course.name}.")
            return False

        # 3. All checks passed, perform enrollment (Transactional step)
        if student_id not in db.enrollments:
            db.enrollments[student_id] = []
        db.enrollments[student_id].append(course_id)
        print(f"SUCCESS: {student.name} has been enrolled in {course.name}.")
        return True

    def drop_course(self, student_id, course_id):
        """Handles dropping a course and triggers the notification system."""
        print(f"\n--- Attempting to drop Course {course_id} for Student {student_id} ---")
        student = self.user_service.get_user(student_id)
        course = self.course_service.get_course(course_id)

        if student_id in db.enrollments and course_id in db.enrollments[student_id]:
            db.enrollments[student_id].remove(course_id)
            print(f"SUCCESS: {student.name} has dropped {course.name}.")
            
            # --- Trigger for Observer Pattern ---
            # If there's a waitlist for this course, notify them.
            if course_id in db.waitlists and db.waitlists[course_id]:
                course.notify()
        else:
            print(f"Error: {student.name} is not enrolled in {course.name}.")

    def get_student_schedule(self, student_id):
        student = self.user_service.get_user(student_id)
        print(f"\n--- Schedule for {student.name} ---")
        if student_id in db.enrollments and db.enrollments[student_id]:
            for course_id in db.enrollments[student_id]:
                course = self.course_service.get_course(course_id)
                print(f"  - {course.name} (ID: {course.course_id})")
        else:
            print("  - No courses enrolled.")
            
    def get_faculty_roster(self, faculty_id, course_id):
        faculty = self.user_service.get_user(faculty_id)
        course = self.course_service.get_course(course_id)
        print(f"\n--- Roster for {course.name} (Instructor: {faculty.name}) ---")
        enrolled_students = [
            self.user_service.get_user(s_id)
            for s_id, c_list in db.enrollments.items()
            if course_id in c_list
        ]
        if enrolled_students:
            for student in enrolled_students:
                print(f"  - Student: {student.name} (ID: {student.user_id})")
        else:
            print("  - No students enrolled.")