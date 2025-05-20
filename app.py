import os
from flask import Flask, render_template, request, redirect, url_for, session, jsonify, flash
from models import db, User, JournalEntry, Streak
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, date, timedelta
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///journal.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'your_secret_key'  # Change this to a strong random key
app.config['UPLOAD_FOLDER'] = 'static/profile_pics'  # Folder to store uploaded pics
db.init_app(app)

with app.app_context():
    db.create_all()


@app.route('/')
def home():
    return render_template('homepage.html')

@app.route('/signup/', methods=['GET', 'POST'])
def signup():
    error = None  # Initialize an error variable
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        hashed_password = generate_password_hash(password)

        existing_user_username = User.query.filter_by(username=username).first()
        existing_user_email = User.query.filter_by(email=email).first()

        if existing_user_username:
            error = 'Username already taken. Please choose another.'
        elif existing_user_email:
            error = 'Email address already registered. Please log in or use a different email.'
        else:
            new_user = User(username=username, email=email,password=hashed_password)
            db.session.add(new_user)
            db.session.commit()
            return redirect(url_for('login'))
    return render_template('SignupNLogin.html', show_signup=True, error=error)

@app.route('/login/', methods=['GET', 'POST'])
def login():
    next_page = request.args.get('next')  # Get the 'next' parameter
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = User.query.filter_by(email=email).first()
        if user and check_password_hash(user.password, password):
            session['user_id'] = user.id
            update_streak(user)  # Update the streak here!
            if next_page:
                return redirect(next_page)  # Redirect to the 'next' page
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid credentials', 'error')
            return render_template('SignupNLogin.html', show_login=True)
    return render_template('SignupNLogin.html', show_login=True)

@app.route('/profile/')
def profile():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    user = User.query.get(session['user_id'])
    journal_entries = JournalEntry.query.filter_by(user_id=user.id).order_by(
        JournalEntry.date_posted.desc()).limit(5).all()  # Get recent entries
    current_streak = user.streak.current_streak if user.streak else 0
    return render_template('profile.html', user=user, journal_entries=journal_entries, current_streak=current_streak)

@app.route('/profile/upload_pic', methods=['POST'])
def upload_profile_pic():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    if 'profile_pic' in request.files:
        file = request.files['profile_pic']
        if file.filename != '':
            filename = secure_filename(file.filename)
            path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(path)

            user = User.query.get(session['user_id'])
            user.profile_pic = filename
            db.session.commit()
            return redirect(url_for('profile'))

    return redirect(url_for('profile'))
  
def update_streak(user):
    today = date.today()
    if not user.streak:  # Create a streak if it doesn't exist
        new_streak = Streak(user_id=user.id, current_streak=1, last_login_date=today)
        db.session.add(new_streak)
    else:
        if user.streak.last_login_date:
            time_since_last_login = today - user.streak.last_login_date
            if time_since_last_login.days == 1:  # Consecutive day
                user.streak.current_streak += 1
            elif time_since_last_login.days > 1:  # Streak broken
                user.streak.current_streak = 1
            else:  # time_since_last_login.days == 0:  # Same day login (do nothing)
                return
        else:  # First login
            user.streak.current_streak = 1
        user.streak.last_login_date = today
    db.session.commit()

@app.route('/dashboard/')
def dashboard():
    if 'user_id' in session:
        user = User.query.get(session['user_id'])
        journal_entries = JournalEntry.query.filter_by(user_id=user.id).order_by(
            JournalEntry.date_posted.desc()).all()
        current_streak = user.streak.current_streak if user.streak else 0
        return render_template('dashboard.html', journal_entries=journal_entries, current_streak=current_streak, user=user)
    else:
        return redirect(url_for('login'))

@app.route('/logout/')
def logout():
    session.pop('user_id', None)
    return redirect(url_for('home'))

@app.route('/journal/new/', methods=['GET', 'POST'])
def new_journal_entry():
    if 'user_id' not in session:
        flash('Login first!', 'error')
        return redirect(url_for('login'))

    user = User.query.get(session['user_id'])
    if request.method == 'POST':
        # Get data from the JSON request body
        data = request.get_json()
        title = data.get('title', 'Untitled Entry') # Default title if not provided
        content = data.get('content') # This will now contain the sketch placeholders
        entry_type = data.get('type')
        mood = data.get('mood')
        # font_family = data.get('fontFamily') # Not saving these to DB for now
        # font_size = data.get('fontSize')
        # line_height = data.get('lineHeight')

        new_entry = JournalEntry(
            title=title,
            content=content,
            type=entry_type,
            mood=mood,
            user_id=session['user_id']
            # You can add font-related fields to your model if you want to save them
        )
        db.session.add(new_entry)
        db.session.commit()
        return jsonify({'status': 'success', 'message': 'Journal saved successfully!'})
    return render_template('new_journal.html', user=user)



@app.route('/journal/<int:entry_id>')
def view_journal_entry(entry_id):
    if 'user_id' not in session:
        return redirect(url_for('login'))
    user = User.query.get(session['user_id'])
    entry = JournalEntry.query.get_or_404(entry_id)  # Get entry or 404 error
    if entry.user_id != session['user_id']:
        return "Unauthorized", 403  # User doesn't own this entry
    return render_template('view_journal.html', entry=entry, user=user)


@app.route('/journal/edit/<int:entry_id>', methods=['GET', 'POST'])
def edit_journal_entry(entry_id):
    if 'user_id' not in session:
        return redirect(url_for('login'))
    user = User.query.get(session['user_id'])
    entry = JournalEntry.query.get_or_404(entry_id)
    if entry.user_id != session['user_id']:
        return "Unauthorized", 403

    if request.method == 'POST':
        entry.title = request.form['title']
        entry.content = request.form['content']
        entry.type = request.form['type']
        entry.mood = request.form.get('mood')
        entry.sketch_data = request.form.get('sketch_data')

        db.session.commit()
        return redirect(url_for('view_journal_entry', entry_id=entry.id))

    return render_template('edit_journal.html', entry=entry, user=user)

@app.route('/journal/update/<int:entry_id>', methods=['POST'])
def update_journal_entry_json(entry_id):
    if 'user_id' not in session:
        return jsonify({'status': 'error', 'message': 'Unauthorized'}), 401

    entry = JournalEntry.query.get_or_404(entry_id)
    if entry.user_id != session['user_id']:
        return jsonify({'status': 'error', 'message': 'Forbidden'}), 403

    data = request.get_json()
    entry.title = data.get('title', entry.title)
    entry.content = data.get('content', entry.content)
    entry.type = data.get('type', entry.type)
    entry.mood = data.get('mood', entry.mood)

    db.session.commit()
    return jsonify({'status': 'success', 'message': 'Journal entry updated successfully!'})


@app.route('/journal/delete/<int:entry_id>')
def delete_journal_entry(entry_id):
    if 'user_id' not in session:
        return redirect(url_for('login'))
    user = User.query.get(session['user_id'])
    entry = JournalEntry.query.get_or_404(entry_id)
    if entry.user_id != session['user_id']:
        return "Unauthorized", 403

    db.session.delete(entry)
    db.session.commit()
    return redirect(url_for('dashboard'))  # Redirect back to the dashboard or journal list


@app.route('/planner/')
def planner():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    user = User.query.get(session['user_id'])
    planner_data = {}
    return render_template('planner.html', user=user, planner_data=planner_data)

@app.route('/musicplayer/')
def musicplayer():
    if 'user_id' not in session:
        return redirect(url_for('login'))  # Or handle unauthenticated access as you prefer
    user = User.query.get(session['user_id'])
    return render_template('musicplay.html', user=user)

@app.route('/check_login/')  # New route to check login status
def check_login():
    if 'user_id' in session:
        return jsonify({'is_logged_in': True})
    else:
        return jsonify({'is_logged_in': False})

if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Create tables within the app context
    app.run(debug=True)