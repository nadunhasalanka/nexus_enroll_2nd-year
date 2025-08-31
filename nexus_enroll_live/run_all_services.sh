#!/bin/bash
echo "Starting all NexusEnroll services..."

# Use python3 or python depending on the system
PYTHON_CMD=python3

# Start each service in the background
$PYTHON_CMD database_service.py &
$PYTHON_CMD user_service.py &
$PYTHON_CMD course_service.py &
$PYTHON_CMD notification_service.py &
$PYTHON_CMD enrollment_service.py &

echo "All services started. Open http://127.0.0.1:5004 in your browser."