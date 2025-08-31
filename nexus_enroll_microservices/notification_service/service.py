# notification_service/service.py

class NotificationService:
    @staticmethod
    def send_notification(user, message):
        """Simulates sending an email or other notification."""
        print(f"--- Notification Sent to {user.name} ({user.get_role()}) ---")
        print(f"  - Message: Hi {user.name}, {message}")