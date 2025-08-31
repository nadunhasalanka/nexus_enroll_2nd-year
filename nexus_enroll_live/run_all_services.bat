@echo off
echo Starting all NexusEnroll services...

start "Database Service" cmd /k python database_service.py
start "User Service" cmd /k python user_service.py
start "Course Service" cmd /k python course_service.py
start "Notification Service" cmd /k python notification_service.py
start "Enrollment Service" cmd /k python enrollment_service.py

echo All services started. Open http://127.0.0.1:5004 in your browser.