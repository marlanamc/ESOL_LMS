from flask import Flask, render_template, request, redirect, url_for, session, flash
from functools import wraps
import pandas as pd
from datetime import datetime
import json
import os

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

def teacher_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get('is_teacher'):
            return redirect(url_for('teacher_login'))
        return f(*args, **kwargs)
    return decorated_function

@app.route('/')
def index():
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
    return render_template('quiz_list.html', quizzes=formatted_quizzes)

@app.route('/quiz/<week>')
def take_quiz(week):
    if week in WEEKLY_QUIZZES:
        quiz_data = WEEKLY_QUIZZES[week]
        # Parse and format the due date
        due_date = datetime.strptime(quiz_data['due_date'], '%Y-%m-%d')
        formatted_due_date = due_date.strftime('%B %d, %Y')
        return render_template('index.html',
                             week=week,
                             due_date=formatted_due_date,
                             verbs=quiz_data['verbs'])
    return redirect(url_for('index'))

@app.route('/submit', methods=['POST'])
def submit():
    student_name = request.form['student_name'].strip()
    week = request.form.get('week')  # Get the week from the form

    # Make sure we're using the correct week's quiz data
    if week not in WEEKLY_QUIZZES:
        return redirect(url_for('index'))

    verbs = WEEKLY_QUIZZES[week]['verbs']  # Get the verbs for this specific week

    score = 0
    results = []

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

    final_score = (score / (len(verbs) * 5)) * 100

    # Save to CSV
    try:
        df = pd.read_csv('quiz_results.csv')
    except FileNotFoundError:
        df = pd.DataFrame(columns=['Date', 'Student', 'Score', 'Week'])

    new_row = {
        'Date': datetime.now().strftime("%Y-%m-%d %H:%M"),
        'Student': student_name,
        'Score': final_score,
        'Week': week
    }
    df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
    df.to_csv('quiz_results.csv', index=False)

    return render_template('results.html',
                         results=results,
                         score=final_score,
                         student_name=student_name,
                         week=week)

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

if __name__ == '__main__':
    app