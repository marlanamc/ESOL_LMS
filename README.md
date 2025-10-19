# ESOL Irregular Verb Quiz System

A Flask-based Learning Management System (LMS) designed for ESOL (English for Speakers of Other Languages) students to practice irregular verb conjugations. This system provides weekly quizzes with immediate feedback and a teacher dashboard for tracking student progress.

## Features

### Student Features
- **Weekly Quiz System**: 14 weeks of progressive irregular verb quizzes
- **Interactive Quiz Interface**: Clean, user-friendly forms for verb conjugation practice
- **Immediate Feedback**: Detailed results showing correct/incorrect answers with explanations
- **Score Tracking**: Visual score indicators (high/medium/low performance)
- **Responsive Design**: Works on desktop and mobile devices

### Teacher Features
- **Secure Dashboard**: Password-protected teacher access
- **Student Progress Tracking**: View individual student performance and averages
- **Class Statistics**: Overall class performance metrics and passing rates
- **Week-by-Week Analysis**: Filter results by specific weeks
- **CSV Export**: Automatic data storage for record keeping

## Quiz Structure

Each week focuses on 5 irregular verbs with students practicing:
- **V1**: Base form (infinitive)
- **V1-3rd**: Third person singular present
- **V1-ing**: Present participle (-ing form)
- **V2**: Past simple
- **V3**: Past participle

## Technology Stack

- **Backend**: Python Flask
- **Frontend**: HTML5, CSS3, Jinja2 templates
- **Data Storage**: JSON (quiz content), CSV (student results)
- **Styling**: Custom CSS with Google Fonts (Poppins)
- **Deployment**: PythonAnywhere compatible

## Installation & Setup

### Prerequisites
- Python 3.7 or higher
- pip (Python package installer)

### Local Development Setup

1. **Clone the repository**
   ```bash
   git clone <your-repo-url>
   cd ESOL_LMS
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   ```bash
   export TEACHER_PASSWORD="your_secure_password_here"
   ```

5. **Run the application**
   ```bash
   python app.py
   ```

6. **Access the application**
   - Student interface: `http://localhost:5000`
   - Teacher login: `http://localhost:5000/teacher/login`

### PythonAnywhere Deployment

1. **Upload files** to your PythonAnywhere account
2. **Set environment variable** in the Web tab:
   - Variable: `TEACHER_PASSWORD`
   - Value: Your secure password
3. **Configure WSGI file** to point to `app.py`
4. **Reload** your web application

## File Structure

```
ESOL_LMS/
├── app.py                 # Main Flask application
├── quizzes.json          # Quiz content and due dates
├── requirements.txt      # Python dependencies
├── static/
│   └── style.css        # Application styling
├── templates/
│   ├── index.html       # Quiz form template
│   ├── quiz_list.html   # Quiz selection page
│   ├── results.html     # Quiz results page
│   ├── teacher_dashboard.html  # Teacher analytics
│   └── teacher_login.html     # Teacher authentication
└── README.md            # This file
```

## Configuration

### Quiz Content
Edit `quizzes.json` to modify:
- Due dates for each week
- Verb lists and correct answers
- Number of weeks

### Styling
Modify `static/style.css` to customize:
- Color scheme
- Typography
- Layout and spacing
- Responsive design

### Security
- Change the `TEACHER_PASSWORD` environment variable
- Consider implementing session timeouts
- Add HTTPS in production

## Usage Guide

### For Students
1. Visit the quiz homepage
2. Select a week's quiz
3. Enter your name
4. Complete all verb forms
5. Submit and review results
6. Practice with other weeks

### For Teachers
1. Access `/teacher/login`
2. Enter the teacher password
3. View class statistics and individual progress
4. Filter by specific weeks
5. Monitor student engagement and performance

## Data Management

### Student Results
- Stored in `quiz_results.csv`
- Columns: Date, Student, Score, Week
- Automatically created on first submission
- Accessible via teacher dashboard

### Quiz Content
- Stored in `quizzes.json`
- Easy to modify and extend
- Supports any number of weeks and verbs

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## Future Enhancements

- [ ] User authentication system
- [ ] Email notifications for due dates
- [ ] Advanced analytics and reporting
- [ ] Mobile app version
- [ ] Multiple language support
- [ ] Automated quiz generation
- [ ] Integration with learning management systems

## License

This project is open source and available under the [WTFPL License](http://www.wtfpl.net/).

## Support

For questions or issues:
- Create an issue in the GitHub repository
- Contact the development team
- Check the documentation for common solutions

## Acknowledgments

- Designed for ESOL education
- Built with Flask framework
- Styled with modern CSS practices
- Deployed on PythonAnywhere platform
