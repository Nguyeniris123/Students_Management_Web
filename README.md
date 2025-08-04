# 🎯 Student Management System

## Description

The Student Management System is a web-based application designed to help schools manage student information, class lists, grades, and generate academic reports. The system is built with Flask (Python) for the backend and uses both REST APIs (called via JavaScript fetch) and server-side rendering with Flask templates (Jinja2) for the frontend.

## Key Features

### 1. Student Enrollment
- Staff can create student profiles including full name, gender, date of birth, address, and phone number.
- Students must be between 15 and 20 years old to enroll.

### 2. Class Management
- Create and manage class lists with student assignments.
- Support for 3 grade levels (10, 11, 12), minimum 1 class and maximum 40 students per class.

### 3. Grade Management
- Teachers can enter grades for students per subject and semester:
  - Minimum 1 and maximum 5 fifteen-minute tests.
  - Minimum 1 and maximum 3 one-period tests.
  - 1 final test per semester.
- Calculate average grades for each student and subject.
- Display subject grade sheets and class average grade tables.

### 4. Reporting
- Generate subject performance reports by class using charts and tables.
- Calculate student passing rates (students pass if average >= 5).

## Technology Stack

- Backend: Python, Flask
- Frontend: HTML, CSS, JavaScript, Bootstrap, Jinja2 (Flask templates)
- Database: MySQL
- Charts: Chart.js

## Link deploy: https://nguyeniris.pythonanywhere.com/
- Admin Account: admin - 1
- Student Account: student1 - 1
