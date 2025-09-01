Of course. Here is a comprehensive `README.md` file tailored specifically for Windows users. It explains the project's architecture, the design patterns used, and provides clear, step-by-step instructions for running the entire system.

You can save this content directly into a file named `README.md` in your `nexus_enroll_live` project folder.

---

# NexusEnroll: A Microservice-Based University Enrollment System

Welcome to NexusEnroll, a proof-of-concept application demonstrating a modern, microservice-based approach to a university course enrollment system. This project was created as a teaching tool to illustrate key software architecture principles and design patterns using Python and Flask.

The system is fully interactive, running as a set of independent services that communicate with each other via APIs, with a simple web interface for user interaction.

## Architectural Overview

This project is built using a **Microservice Architecture**. Instead of a single, monolithic application, the system is broken down into small, independent services. Each service has a single responsibility, runs in its own process, and communicates with others over the network (HTTP).

This architecture promotes scalability, maintainability, and resilience.

### The Services

1.  **Database Service** (`port 5000`): The single source of truth. This service's only job is to store and retrieve data. It acts as our in-memory database, ensuring data consistency.
2.  **User Service** (`port 5001`): Responsible for creating different types of users (Students, Faculty, etc.).
3.  **Course Service** (`port 5002`): Responsible for creating courses and managing course-related data.
4.  **Notification Service** (`port 5003`): A decoupled service responsible for sending notifications (simulated as console output). This prevents the core logic from being blocked by notification failures.
5.  **Enrollment Service (Facade)** (`port 5004`): The main entry point for the user interface and the orchestrator of all major operations. It handles the complex logic for enrolling, unenrolling, and waitlisting students by coordinating with the other services.



## Design Patterns Implemented

This project explicitly demonstrates several key software design patterns:

*   **Facade Pattern:** The `enrollment_service` acts as a Facade. The user interface only needs to talk to this one service to perform complex actions like enrolling a student. The facade hides the underlying complexity of coordinating calls to the User, Course, and Database services.

*   **Factory Method Pattern:** The `user_service` uses a Factory to create user objects. This decouples the client (the API endpoint) from the concrete implementation of `Student`, `Faculty`, or `Administrator` classes, making it easy to add new user types in the future.

*   **Observer Pattern (Modern Interpretation):** When a student unenrolls from a full course, a spot opens up. The `enrollment_service` (the "Subject") triggers an event. The `notification_service` is called to alert the first student on the waitlist (the "Observer"). This decouples the unenrollment logic from the notification logic.

## Getting Started on Windows

Follow these instructions to get the entire system up and running on your Windows machine.

### Prerequisites

*   **Python 3.6+**: Make sure Python is installed on your system and added to your PATH. You can download it from the [official Python website](https://www.python.org/downloads/).
*   **pip**: The Python package installer (it comes included with modern Python versions).

### Step 1: Set Up the Project

1.  Download or clone the project files into a folder on your computer (e.g., `C:\Users\YourUser\Desktop\nexus_enroll_live`).
2.  Open the Windows Command Prompt (`cmd`) or PowerShell.
3.  Navigate into your project directory.
    ```cmd
    cd C:\Users\YourUser\Desktop\nexus_enroll_live
    ```

### Step 2: Create and Activate a Virtual Environment

It is a best practice to create a virtual environment to isolate project dependencies.

1.  **Create the environment:**
    ```cmd
    python -m venv venv
    ```
2.  **Activate the environment:**
    ```cmd
    venv\Scripts\activate
    ```
    ###### OR

    ```cmd
    venv\bin\activate
    ```

    You will know it's active because your command prompt will now be prefixed with `(venv)`.

### Step 3: Install Dependencies

Install all the required Python libraries using the `requirements.txt` file.
```cmd
pip install -r requirements.txt
```

### Step 4: Run All Microservices

A convenient batch script is included to launch all five services at once.
```cmd
run_all_services.bat
```
This command will open **five new Command Prompt windows**, one for each microservice. You will see output in each window indicating that a Flask server is running.

### Step 5: Access the Application

Once all services are running, open your web browser and navigate to:
> **http://127.0.0.1:5004**

## How to Use the Application

The web interface is split into three columns: **Actions**, **Current System Data**, and **Service Response Log**.

Here is a recommended workflow to test all features:

1.  **View Initial State:** Click the **"View/Refresh System Data"** button. The middle column will show the empty database.
2.  **Create Users:**
    *   Use the "Add User" form to create an "Enrolled Student" (e.g., ID `S001`).
    *   Create a "Waitlist Student" (e.g., ID `S002`).
3.  **Create a Course:**
    *   Use the "Add Course" form to create a course with a small capacity (e.g., ID `CS101`, Name `Test Course`, **Capacity `1`**).
4.  **Enroll and Fill the Course:**
    *   Use the "Enroll Student" form to enroll `S001` in `CS101`. The log will show success.
    *   Click "View/Refresh System Data" to see that `S001` is now enrolled and the course is full.
5.  **Get on the Waitlist:**
    *   Use the "Enroll Student" form to enroll `S002` in `CS101`.
    *   The log will confirm that `S002` was added to the waitlist. Refresh the data to see the `waitlists` object updated.
6.  **Unenroll and Trigger Notification:**
    *   **Look at the terminal window for the `notification_service` (port 5003).**
    *   Use the **"Unenroll Student from Course"** form to remove `S001` from `CS101`.
    *   The UI log will confirm the action and state that the waitlisted student was notified.
    *   The notification service's terminal window will print the simulated notification message sent to `S002`.

## Stopping the Services

To shut down the application, you must stop all five running services. The easiest way is to go to each of the five Command Prompt windows that opened and press **`Ctrl + C`** in each one.

## Troubleshooting

### "Address already in use" Error

This is the most common error. It means you tried to start the services when the old ones were still running in the background.

**Solution:**
1.  Open Command Prompt **as an Administrator**.
2.  Run this command to find the Process IDs (PIDs) using the required ports:
    ```cmd
    netstat -ano -p tcp | findstr "LISTEN" | findstr ":500"
    ```
3.  Look at the last column to find the PIDs.
4.  For each PID you found, forcefully stop the process:
    ```cmd
    taskkill /PID <ProcessID> /F
    ```    (Replace `<ProcessID>` with the actual number, e.g., `taskkill /PID 12345 /F`).
5.  Once all old processes are stopped, try running `run_all_services.bat` again.