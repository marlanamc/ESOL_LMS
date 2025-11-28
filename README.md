# ESOL Irregular Verb Quiz System

A lightweight Learning Management System (LMS) designed for ESOL students to practice irregular verb conjugations, featuring weekly quizzes and a teacher dashboard.

## Overview

This application provides a simple, focused environment for students to master irregular verbs. It guides students through a 14-week curriculum where they practice different verb forms (V1, V1-3rd, V1-ing, V2, V3). Teachers can monitor progress through a secure dashboard that aggregates class statistics and individual student performance.

## Features

*   **Student Quiz System**: Weekly quizzes focusing on 5 verbs per week.
*   **Instant Feedback**: Immediate validation of answers with corrections.
*   **Teacher Dashboard**: Password-protected view to monitor class progress.
*   **Class Statistics**: Aggregated data on passing rates and average scores.
*   **Progress Tracking**: Detailed breakdown of student performance by week.

## Tech Stack

*   **Python 3**: Core programming language.
*   **Flask**: Web framework for backend logic and routing.
*   **Jinja2**: Templating engine for dynamic HTML rendering.
*   **HTML5 & CSS3**: Frontend structure and styling.
*   **JSON**: Storage for quiz content and student data.
*   **CSV**: Storage for quiz results and performance data.

## Getting Started

Follow these steps to run the application locally:

1.  **Clone the repository**
    ```bash
    git clone https://github.com/marlanamc/ESOL_LMS.git
    cd ESOL_LMS
    ```

2.  **Create and activate a virtual environment**
    ```bash
    python3 -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    ```

3.  **Install dependencies**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Set environment variables**
    ```bash
    export FLASK_APP=app.py
    export FLASK_ENV=development
    export TEACHER_PASSWORD=your_secret_password
    ```

5.  **Run the application**
    ```bash
    flask run
    ```

6.  **Access the app**
    *   Open `http://127.0.0.1:5000` in your browser.

## Project Structure

*   `app.py`: Main Flask application containing routes and logic.
*   `templates/`: HTML templates for the application pages.
*   `static/`: CSS files and other static assets.
*   `quizzes.json`: Configuration file defining weekly quizzes and verbs.
*   `students.json`: Data store for registered students.
*   `quiz_results.csv`: Data store for student quiz submissions.

## Future Improvements

*   **Database Integration**: Migrate from CSV/JSON to SQLite or PostgreSQL for better data management.
*   **User Accounts**: Implement robust session management and user authentication.
*   **Enhanced Security**: Add password hashing and secure session handling.
*   **More Quiz Types**: Add multiple choice or fill-in-the-blank variations.
*   **Email Notifications**: Send reminders to students for upcoming due dates.
*   **Mobile App**: Create a dedicated mobile experience for on-the-go practice.
