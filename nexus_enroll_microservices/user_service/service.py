# user_service/service.py
from abc import ABC, abstractmethod
from shared_db.singleton_db import db

# --- User Models (Product Interface and Concrete Products) ---
class User(ABC):
    """Abstract Product: Defines the interface for user objects."""
    def __init__(self, user_id, name):
        self.user_id = user_id
        self.name = name

    @abstractmethod
    def get_role(self):
        pass
        
    def update(self, course):
        """Method for Observer pattern, primarily for students."""
        print(f"  - NOTE: User {self.name} has no specific notification action.")

class Student(User):
    """Concrete Product: Represents a student user."""
    def get_role(self):
        return "Student"
        
    def update(self, course):
        """
        Concrete implementation for the Observer pattern.
        When notified, a student will receive a message.
        """
        from notification_service.service import NotificationService
        message = f"a spot has opened up in {course.name} (ID: {course.course_id})."
        NotificationService.send_notification(self, message)

class Faculty(User):
    """Concrete Product: Represents a faculty user."""
    def get_role(self):
        return "Faculty"

class Administrator(User):
    """Concrete Product: Represents an administrator user."""
    def get_role(self):
        return "Administrator"

# --- User Factory (Creator Interface and Concrete Creator) ---
class UserFactory(ABC):
    """Abstract Creator: Factory Method for creating users."""
    @abstractmethod
    def create_user(self, user_id, name):
        pass

class ConcreteUserFactory(UserFactory):
    """Concrete Creator: Implements the factory method."""
    def create_user(self, user_type, user_id, name):
        if user_type.lower() == 'student':
            return Student(user_id, name)
        elif user_type.lower() == 'faculty':
            return Faculty(user_id, name)
        elif user_type.lower() == 'administrator':
            return Administrator(user_id, name)
        raise ValueError(f"Unknown user type: {user_type}")

# --- Service Logic ---
class UserService:
    """Service to manage user creation and retrieval."""
    def __init__(self):
        self.user_factory = ConcreteUserFactory()

    def add_user(self, user_type, user_id, name):
        if user_id in db.users:
            print(f"Error: User with ID {user_id} already exists.")
            return None
        new_user = self.user_factory.create_user(user_type, user_id, name)
        db.users[user_id] = new_user
        print(f"User Added: {new_user.name} ({new_user.get_role()})")
        return new_user

    def get_user(self, user_id):
        return db.users.get(user_id)