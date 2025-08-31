# shared_db/singleton_db.py

class InMemoryDatabase:
    """
    Singleton class for an in-memory database.
    This ensures all microservices access the same data instance.
    """
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            print("Creating a new database instance.")
            cls._instance = super(InMemoryDatabase, cls).__new__(cls)
            # Initialize data stores
            cls._instance.courses = {}
            cls._instance.users = {}
            cls._instance.enrollments = {} 
            cls._instance.waitlists = {} 
        return cls._instance

    def clear_data(self):
        """Utility method to reset data for clean test runs."""
        print("\n--- CLEARING ALL DATABASE DATA ---")
        self.courses.clear()
        self.users.clear()
        self.enrollments.clear()
        self.waitlists.clear()

# Instantiate the singleton
db = InMemoryDatabase()