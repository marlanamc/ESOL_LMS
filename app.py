from flask import Flask, render_template, request, redirect, url_for, session, flash, send_file
from functools import wraps
import pandas as pd
from datetime import datetime
import json
import os
import io
import hashlib
import secrets

app = Flask(__name__)
app.secret_key = os.urandom(24)
TEACHER_PASSWORD = os.getenv('TEACHER_PASSWORD')  # Get the password from an environment variable

def load_quizzes():
    file_path = os.path.join(os.path.dirname(__file__), 'quizzes.json')
    try:
        with open(file_path, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"Error: quizzes.json not found at {file_path}")
        return {}
    except json.JSONDecodeError:
        print("Error: Invalid JSON format in quizzes.json")
        return {}

WEEKLY_QUIZZES = load_quizzes()

def load_students():
    """Load student data from JSON file"""
    file_path = os.path.join(os.path.dirname(__file__), 'students.json')
    try:
        with open(file_path, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return {}
    except json.JSONDecodeError:
        return {}

def save_students(students):
    """Save student data to JSON file"""
    file_path = os.path.join(os.path.dirname(__file__), 'students.json')
    with open(file_path, 'w') as f:
        json.dump(students, f, indent=2)

def hash_password(password):
    """Hash password with salt"""
    salt = secrets.token_hex(16)
    return hashlib.pbkdf2_hmac('sha256', password.encode(), salt.encode(), 100000).hex() + ':' + salt

def verify_password(stored_password, provided_password):
    """Verify password against stored hash"""
    try:
        password_hash, salt = stored_password.split(':')
        return password_hash == hashlib.pbkdf2_hmac('sha256', provided_password.encode(), salt.encode(), 100000).hex()
    except ValueError:
        return False

def student_required(f):
    """Decorator to require student login"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get('student_id'):
            return redirect(url_for('student_login'))
        return f(*args, **kwargs)
    return decorated_function

def teacher_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get('is_teacher'):
            return redirect(url_for('teacher_login'))
        return f(*args, **kwargs)
    return decorated_function

@app.route('/')
def index():
    # Check if student is logged in
    if not session.get('student_id'):
        return redirect(url_for('student_login'))
    
    # Format the due dates
    print("Rendering quiz list")
    formatted_quizzes = {}
    for week, data in WEEKLY_QUIZZES.items():
        due_date = datetime.strptime(data['due_date'], '%Y-%m-%d')
        formatted_due_date = due_date.strftime('Due %A, %B %d, %Y')
        formatted_quizzes[week] = {
            'due_date': formatted_due_date,
            'verbs': data['verbs']
        }
    
    # Get student name for display
    students = load_students()
    student_name = students.get(session['student_id'], {}).get('name', 'Student')
    
    return render_template('quiz_list.html', quizzes=formatted_quizzes, student_name=student_name)

@app.route('/quiz/<week>')
@student_required
def take_quiz(week):
    if week in WEEKLY_QUIZZES:
        quiz_data = WEEKLY_QUIZZES[week]
        # Parse and format the due date
        due_date = datetime.strptime(quiz_data['due_date'], '%Y-%m-%d')
        formatted_due_date = due_date.strftime('%B %d, %Y')
        
        # Get student name
        students = load_students()
        student_name = students.get(session['student_id'], {}).get('name', 'Student')
        
        return render_template('index.html',
                             week=week,
                             due_date=formatted_due_date,
                             verbs=quiz_data['verbs'],
                             student_name=student_name)
    return redirect(url_for('index'))

@app.route('/submit', methods=['POST'])
@student_required
def submit():
    week = request.form.get('week')  # Get the week from the form

    # Make sure we're using the correct week's quiz data
    if week not in WEEKLY_QUIZZES:
        flash('Invalid quiz week selected.')
        return redirect(url_for('index'))

    # Get student name from session
    students = load_students()
    student_name = students.get(session['student_id'], {}).get('name', 'Student')

    verbs = WEEKLY_QUIZZES[week]['verbs']  # Get the verbs for this specific week

    score = 0
    results = []
    total_questions = len(verbs) * 5

    for verb in verbs:
        verb_results = {'verb': verb, 'answers': [], 'correct': []}
        for form in ['v1', 'v1_3rd', 'v1_ing', 'v2', 'v3']:
            student_answer = request.form.get(f'{verb}_{form}', '').strip().lower()
            correct_answer = verbs[verb][form].strip().lower()

            if student_answer == correct_answer:
                score += 1

            verb_results['answers'].append(student_answer)
            verb_results['correct'].append(correct_answer)

        results.append(verb_results)

    final_score = (score / total_questions) * 100 if total_questions > 0 else 0

    # Save to CSV
    try:
        df = pd.read_csv('quiz_results.csv')
    except FileNotFoundError:
        df = pd.DataFrame(columns=['Date', 'Student', 'Score', 'Week', 'Student_ID'])

    new_row = {
        'Date': datetime.now().strftime("%Y-%m-%d %H:%M"),
        'Student': student_name,
        'Score': final_score,
        'Week': week,
        'Student_ID': session['student_id']
    }
    df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
    df.to_csv('quiz_results.csv', index=False)

    return render_template('results.html',
                         results=results,
                         score=final_score,
                         student_name=student_name,
                         week=week,
                         total_questions=total_questions,
                         correct_answers=score)

@app.route('/student/register', methods=['GET', 'POST'])
def student_register():
    if request.method == 'POST':
        username = request.form['username'].strip().lower()
        password = request.form['password']
        name = request.form['name'].strip()
        
        if not username or not password or not name:
            flash('All fields are required')
            return render_template('student_register.html')
        
        if len(username) < 3:
            flash('Username must be at least 3 characters long')
            return render_template('student_register.html')
        
        if len(password) < 4:
            flash('Password must be at least 4 characters long')
            return render_template('student_register.html')
        
        students = load_students()
        
        if username in students:
            flash('Username already exists')
            return render_template('student_register.html')
        
        # Create new student
        students[username] = {
            'name': name,
            'password': hash_password(password),
            'created': datetime.now().strftime("%Y-%m-%d %H:%M")
        }
        
        save_students(students)
        flash('Registration successful! Please log in.')
        return redirect(url_for('student_login'))
    
    return render_template('student_register.html')

@app.route('/student/login', methods=['GET', 'POST'])
def student_login():
    if request.method == 'POST':
        username = request.form['username'].strip().lower()
        password = request.form['password']
        
        students = load_students()
        
        if username in students and verify_password(students[username]['password'], password):
            session['student_id'] = username
            flash('Login successful!')
            return redirect(url_for('index'))
        else:
            flash('Invalid username or password')
    
    return render_template('student_login.html')

@app.route('/student/logout')
def student_logout():
    session.pop('student_id', None)
    flash('You have been logged out')
    return redirect(url_for('student_login'))

@app.route('/teacher/login', methods=['GET', 'POST'])
def teacher_login():
    if request.method == 'POST':
        if request.form['password'] == TEACHER_PASSWORD:
            session['is_teacher'] = True
            return redirect(url_for('teacher_dashboard'))
        else:
            flash('Invalid password')
    return render_template('teacher_login.html')

@app.route('/teacher/logout')
def teacher_logout():
    session.pop('is_teacher', None)
    return redirect(url_for('index'))

@app.route('/teacher/dashboard')
@teacher_required
def teacher_dashboard():
    try:
        df = pd.read_csv('quiz_results.csv')
        selected_week = request.args.get('week', 'all')  # Get selected week from URL parameter

        # Get list of all weeks for dropdown
        all_weeks = sorted(df['Week'].unique())

        # Filter by week if one is selected
        if selected_week != 'all':
            filtered_df = df[df['Week'] == selected_week]
        else:
            filtered_df = df

        # Calculate statistics
        total_students = len(filtered_df['Student'].unique())
        average_score = filtered_df['Score'].mean()
        recent_results = filtered_df.tail(10).sort_values(by='Date', ascending=False)

        # Group by student and get their average scores
        student_averages = filtered_df.groupby('Student').agg({
            'Score': ['mean', 'count'],
            'Week': lambda x: ', '.join(sorted(set(x)))
        }).round(2)
        student_averages.columns = ['mean', 'count', 'weeks']
        student_averages = student_averages.sort_values(by='mean', ascending=False)

        # Calculate totals
        total_quizzes = len(filtered_df)
        total_passing = len(filtered_df[filtered_df['Score'] >= 70])
        passing_rate = (total_passing / total_quizzes * 100) if total_quizzes > 0 else 0

        return render_template('teacher_dashboard.html',
                             total_students=total_students,
                             average_score=round(average_score, 2),
                             recent_results=recent_results.to_dict('records'),
                             student_averages=student_averages.to_dict('index'),
                             all_weeks=all_weeks,
                             selected_week=selected_week,
                             total_quizzes=total_quizzes,
                             total_passing=total_passing,
                             passing_rate=round(passing_rate, 1))
    except FileNotFoundError:
        return render_template('teacher_dashboard.html',
                             error="No quiz results found yet.")

@app.route('/teacher/download_csv')
@teacher_required
def download_csv():
    try:
        df = pd.read_csv('quiz_results.csv')
        selected_week = request.args.get('week', 'all')
        
        # Filter by week if one is selected
        if selected_week != 'all':
            filtered_df = df[df['Week'] == selected_week]
            filename = f'quiz_results_{selected_week.replace(" ", "_")}.csv'
        else:
            filtered_df = df
            filename = 'quiz_results_all_weeks.csv'
        
        # Create CSV in memory
        output = io.StringIO()
        filtered_df.to_csv(output, index=False)
        output.seek(0)
        
        # Create BytesIO object for sending
        mem = io.BytesIO()
        mem.write(output.getvalue().encode('utf-8'))
        mem.seek(0)
        
        return send_file(
            mem,
            as_attachment=True,
            download_name=filename,
            mimetype='text/csv'
        )
    except FileNotFoundError:
        flash('No quiz results found to download.')
        return redirect(url_for('teacher_dashboard'))

@app.route('/teacher/reset_password', methods=['POST'])
@teacher_required
def reset_student_password():
    username = request.form['username'].strip().lower()
    new_password = request.form['new_password']
    
    if not username or not new_password:
        flash('Both username and password are required.')
        return redirect(url_for('teacher_dashboard'))
    
    if len(new_password) < 4:
        flash('Password must be at least 4 characters long.')
        return redirect(url_for('teacher_dashboard'))
    
    students = load_students()
    
    if username in students:
        students[username]['password'] = hash_password(new_password)
        save_students(students)
        flash(f'Password reset successfully for {username}')
    else:
        flash('Student not found.')
    
    return redirect(url_for('teacher_dashboard'))

if __name__ == '__main__':
    app