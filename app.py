from flask import Flask, render_template, request, redirect, url_for, send_from_directory, session, flash
import os
from models import db, JobSeeker, init_db
from config import config

app = Flask(__name__)
app.config.from_object(config)

# Initialize the database
init_db(app)

# Hardcoded credentials for login
USERNAME = 'amit'
PASSWORD = '12345'

@app.route('/', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        phone = request.form['phone']
        resume = request.files['resume']

        # Save the resume file
        resume_filename = f"{name}_{resume.filename}"
        resume_path = os.path.join(app.config['UPLOAD_FOLDER'], resume_filename)
        resume.save(resume_path)

        # Save the job seeker's data in the database
        new_seeker = JobSeeker(name=name, email=email, phone=phone, resume=resume_filename)
        db.session.add(new_seeker)
        db.session.commit()

        return redirect(url_for('success', seeker_id=new_seeker.id))

    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username == USERNAME and password == PASSWORD:
            session['logged_in'] = True
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid credentials. Please try again.')
    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    
    seekers = JobSeeker.query.all()
    return render_template('dashboard.html', seekers=seekers)

@app.route('/success/<int:seeker_id>')
def success(seeker_id):
    seeker = JobSeeker.query.get_or_404(seeker_id)
    return render_template('success.html', seeker=seeker)

@app.route('/resume/<filename>')
def resume(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    app.run(debug=True)
