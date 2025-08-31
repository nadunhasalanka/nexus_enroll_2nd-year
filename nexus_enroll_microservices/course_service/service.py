# course_service/service.py
from shared_db.singleton_db import db

# --- The 'Subject' for the Observer Pattern ---
class Course:
    def __init__(self, course_id, name, capacity, prerequisites=None):
        self.course_id = course_id
        self.name = name
        self.capacity = capacity
        self.prerequisites = prerequisites or []
        self._observers = [] # List of student observers on the waitlist

    # --- Observer Pattern Methods ---
    def attach(self, observer):
        """Add a student to the waitlist (observers)."""
        if observer not in self._observers:
            self._observers.append(observer)
            print(f"  - Observer Added: {observer.name} is now observing {self.name}.")

    def detach(self, observer):
        """Remove a student from the waitlist."""
        self._observers.remove(observer)
        print(f"  - Observer Removed: {observer.name} is no longer observing {self.name}.")

    def notify(self):
        """Notify all observers (waitlisted students) of a change."""
        print(f"\n--- Notifying Observers for Course '{self.name}' ---")
        if not self._observers:
            print("  - No observers to notify.")
            return
        # Notify the first student on the waitlist
        observer_to_notify = self._observers[0]
        print(f"  - Notifying {observer_to_notify.name}...")
        observer_to_notify.update(self)

# --- Service Logic ---
class CourseService:
    def add_course(self, course_id, name, capacity):
        if course_id in db.courses:
            return None
        new_course = Course(course_id, name, capacity)
        db.courses[course_id] = new_course
        print(f"Course Added: {name} (Capacity: {capacity})")
        return new_course

    def get_course(self, course_id):
        return db.courses.get(course_id)

    def get_enrolled_count(self, course_id):
        return sum(1 for enroll_list in db.enrollments.values() if course_id in enroll_list)

    def generate_capacity_report(self, threshold=0.9):
        print(f"\n--- Generating Report: Courses over {threshold*100}% capacity ---")
        for course_id, course in db.courses.items():
            enrolled_count = self.get_enrolled_count(course_id)
            if course.capacity > 0 and (enrolled_count / course.capacity) >= threshold:
                print(f"  - {course.name}: {enrolled_count}/{course.capacity} students")