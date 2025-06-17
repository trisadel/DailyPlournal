import os
from flask import Flask, render_template, request, redirect, url_for, session, jsonify, flash
from models import db, User, JournalEntry, Streak,  Note, Habit, HabitStatus, CustomSection, CustomSectionType, Template
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, date, timedelta
from werkzeug.utils import secure_filename
import json

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
    current_streak = 0
    user = None
    if 'user_id' in session:
        user = User.query.get(session['user_id'])
        # More robust check: ensure user exists AND user.streak exists before accessing current_streak
        if user and user.streak:
            current_streak = user.streak.current_streak
        else:
            current_streak = 0
    return render_template('homepage.html', user=user, current_streak=current_streak)

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
        return redirect(url_for('login'))

    user = User.query.get(session['user_id'])
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        entry_type = request.form['type']
        mood = request.form.get('mood')
        
        # Get date from form and convert to datetime object
        date_posted_str = request.form['date_posted']
        date_posted = datetime.strptime(date_posted_str, '%Y-%m-%d') # Convert string to datetime object

        new_entry = JournalEntry(
            title=title,
            content=content,
            type=entry_type,
            mood=mood,
            date_posted=date_posted, # Use the date from the form
            user_id=session['user_id']
        )
        db.session.add(new_entry)
        db.session.commit()

       # Update streak based on the journal entry's date_posted
        entry_date_for_streak = date_posted.date() # Use the date from the form for streak calculation
        streak = Streak.query.filter_by(user_id=session['user_id']).first()

        if not streak:
            # If no streak exists, start a new one with the entry's date
            streak = Streak(user_id=session['user_id'], current_streak=1, last_login_date=entry_date_for_streak)
            db.session.add(streak)
        else:
            # Compare with the entry's date for streak logic
            if streak.last_login_date == entry_date_for_streak - timedelta(days=1):
                # If the entry date is the day after the last streak date, increment
                streak.current_streak += 1
            elif streak.last_login_date != entry_date_for_streak:
                # If the entry date is not consecutive and not the same day, reset streak
                streak.current_streak = 1
                streak.last_login_date = entry_date_for_streak
        db.session.commit()

        flash('Journal entry created successfully!', 'success')
        return redirect(url_for('dashboard'))
    
    # Pass today's date to the template for default value
    today_date = date.today().strftime('%Y-%m-%d')
    current_streak = user.streak.current_streak if user.streak else 0
    return render_template('new_journal.html', user=user, today_date=today_date, current_streak=current_streak)

@app.route('/journal/view/<int:entry_id>')
def view_journal_entry(entry_id):
    if 'user_id' not in session:
        return redirect(url_for('login'))
    user = User.query.get(session['user_id'])
    entry = JournalEntry.query.get_or_404(entry_id)

    if entry.user_id != session['user_id']:
        return "Unauthorized", 403
    current_streak = user.streak.current_streak if user.streak else 0
    return render_template('view_journal.html', user=user, entry=entry, current_streak=current_streak)


@app.route('/journal/edit/<int:entry_id>', methods=['GET', 'POST'])
def edit_journal_entry(entry_id):
    if 'user_id' not in session:
        return redirect(url_for('login'))

    user = User.query.get(session['user_id'])
    entry = JournalEntry.query.get_or_404(entry_id)

    if entry.user_id != session['user_id']:
        flash('You are not authorized to edit this entry.', 'danger')
        return redirect(url_for('dashboard'))

    if request.method == 'POST':
        entry.title = request.form['title']
        entry.content = request.form['content']
        entry.type = request.form['type']
        entry.mood = request.form.get('mood')
        
        # Get date from form and update entry's date_posted
        date_posted_str = request.form['date_posted']
        entry.date_posted = datetime.strptime(date_posted_str, '%Y-%m-%d') # Update date_posted
        
        entry.updated_at = datetime.utcnow() # Always update updated_at on edit

        db.session.commit()
        flash('Journal entry updated successfully!', 'success')
        # Change this line to redirect instead of jsonify
        return redirect(url_for('view_journal_entry', entry_id=entry.id)) # Corrected line
    current_streak = user.streak.current_streak if user.streak else 0
    return render_template('edit_journal.html', user=user, entry=entry, current_streak=current_streak)

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
    # IMPORTANT: Check if user exists. If not, clear session and redirect.
    if user is None:
        session.pop('user_id', None)
        session.pop('username', None)
        flash('Your session is invalid. Please log in again.', 'warning')
        return redirect(url_for('login'))

    # Fetch initial data for the planner
    initial_notes = {}
    notes_db = Note.query.filter_by(user_id=user.id).all()
    for note in notes_db:
        initial_notes[note.date.strftime('%Y-%m-%d')] = note.content

    initial_habit_list = []
    habits_db = Habit.query.filter_by(user_id=user.id).order_by(Habit.name).all()
    for habit in habits_db:
        initial_habit_list.append(habit.name)

    initial_habit_status = {}
    habit_statuses_db = HabitStatus.query.filter_by(user_id=user.id).all()
    for status in habit_statuses_db:
        habit_name = status.habit.name # Assuming a relationship to Habit model via habit_id
        status_date = status.date.strftime('%Y-%m-%d')
        # The frontend expects habitStatus[date][habitName], so structure it this way
        if status_date not in initial_habit_status:
            initial_habit_status[status_date] = {}
        initial_habit_status[status_date][habit_name] = status.completed


    initial_custom_sections = {}
    custom_sections_db = CustomSection.query.filter_by(user_id=user.id).all()
    for section in custom_sections_db:
        section_date = section.date.strftime('%Y-%m-%d')
        if section_date not in initial_custom_sections:
            initial_custom_sections[section_date] = {}
        
        section_data = {
            'type': section.type,
            'name': section.name # Explicitly add name to the section_data
        }
        if section.type == 'text':
            section_data['value'] = section.content
        elif section.type == 'time':
            try:
                section_data['slots'] = json.loads(section.content) if section.content else []
            except json.JSONDecodeError:
                section_data['slots'] = [] # Handle potential bad JSON
        elif section.type == 'money': # Handle money type explicitly
            section_data['value'] = section.content

        initial_custom_sections[section_date][section.name] = section_data

    current_streak = user.streak.current_streak if user.streak else 0
    return render_template(
        'planner.html',
        user=user,
        initial_notes=initial_notes,
        initial_habit_list=initial_habit_list,
        initial_habit_status=initial_habit_status,
        initial_custom_sections=initial_custom_sections,
        current_streak=current_streak
    )

# API Endpoints for Planner data interaction

@app.route('/api/save_note/', methods=['POST'])
def save_note():
    if 'user_id' not in session:
        return jsonify({'status': 'error', 'message': 'Not logged in'}), 401
    
    data = request.get_json()
    date_str = data.get('date')
    content = data.get('content')
    
    if not date_str:
        return jsonify({'status': 'error', 'message': 'Date is required'}), 400
    
    note_date = datetime.strptime(date_str, '%Y-%m-%d').date()
    
    note = Note.query.filter_by(user_id=session['user_id'], date=note_date).first()
    if note:
        note.content = content
    else:
        note = Note(user_id=session['user_id'], date=note_date, content=content)
        db.session.add(note)
    
    db.session.commit()
    return jsonify({'status': 'success', 'message': 'Note saved!'})

@app.route('/api/delete_note/', methods=['POST'])
def delete_note():
    if 'user_id' not in session:
        return jsonify({'status': 'error', 'message': 'Not logged in'}), 401

    data = request.get_json()
    date_str = data.get('date')

    if not date_str:
        return jsonify({'status': 'error', 'message': 'Date is required'}), 400

    note_date = datetime.strptime(date_str, '%Y-%m-%d').date()

    note = Note.query.filter_by(user_id=session['user_id'], date=note_date).first()
    if note:
        db.session.delete(note)
        db.session.commit()
        return jsonify({'status': 'success', 'message': 'Note deleted!'})
    else:
        return jsonify({'status': 'error', 'message': 'Note not found'}), 404


@app.route('/api/save_habit_status/', methods=['POST'])
def save_habit_status():
    if 'user_id' not in session:
        return jsonify({'status': 'error', 'message': 'Not logged in'}), 401
    
    data = request.get_json()
    date_str = data.get('date')
    habit_name = data.get('habitName')
    completed = data.get('completed')
    
    # Corrected condition for missing data: check if habit_name and completed are not None
    if not date_str or habit_name is None or completed is None:
        return jsonify({'status': 'error', 'message': 'Date, habit name, and completion status are required'}), 400

    habit_date = datetime.strptime(date_str, '%Y-%m-%d').date()

    habit = Habit.query.filter_by(user_id=session['user_id'], name=habit_name).first()
    if not habit:
        return jsonify({'status': 'error', 'message': 'Habit not found'}), 404

    habit_status = HabitStatus.query.filter_by(habit_id=habit.id, date=habit_date).first()
    if habit_status:
        habit_status.completed = completed
    else:
        habit_status = HabitStatus(user_id=session['user_id'], habit_id=habit.id, date=habit_date, completed=completed)
        db.session.add(habit_status)
    
    db.session.commit()
    return jsonify({'status': 'success', 'message': 'Habit status updated!'})

@app.route('/api/add_habit/', methods=['POST'])
def add_habit():
    if 'user_id' not in session:
        return jsonify({'status': 'error', 'message': 'Not logged in'}), 401

    data = request.get_json()
    habit_name = data.get('habitName')

    if not habit_name:
        return jsonify({'status': 'error', 'message': 'Habit name is required'}), 400
    
    existing_habit = Habit.query.filter_by(user_id=session['user_id'], name=habit_name).first()
    if existing_habit:
        return jsonify({'status': 'error', 'message': 'Habit already exists'}), 409

    new_habit = Habit(user_id=session['user_id'], name=habit_name)
    db.session.add(new_habit)
    db.session.commit()
    return jsonify({'status': 'success', 'message': 'Habit added!', 'habitId': new_habit.id})

@app.route('/api/delete_habit/', methods=['POST'])
def delete_habit():
    if 'user_id' not in session:
        return jsonify({'status': 'error', 'message': 'Not logged in'}), 401

    data = request.get_json()
    habit_name = data.get('habitName')

    if not habit_name:
        return jsonify({'status': 'error', 'message': 'Habit name is required'}), 400
    
    habit = Habit.query.filter_by(user_id=session['user_id'], name=habit_name).first()
    if not habit:
        return jsonify({'status': 'error', 'message': 'Habit not found'}), 404
    
    # Delete associated habit statuses first
    HabitStatus.query.filter_by(habit_id=habit.id).delete()
    db.session.delete(habit)
    db.session.commit()
    return jsonify({'status': 'success', 'message': 'Habit deleted!'})


@app.route('/api/add_custom_section_type/', methods=['POST'])
def add_custom_section_type():
    if 'user_id' not in session:
        return jsonify({'status': 'error', 'message': 'Not logged in'}), 401

    data = request.get_json()
    name = data.get('name')
    section_type = data.get('type') # 'text' or 'time'

    if not name or not section_type:
        return jsonify({'status': 'error', 'message': 'Name and type are required'}), 400
    
    existing_type = CustomSectionType.query.filter_by(user_id=session['user_id'], name=name).first()
    if existing_type:
        return jsonify({'status': 'error', 'message': 'Custom section type with this name already exists'}), 409

    new_type = CustomSectionType(user_id=session['user_id'], name=name, type=section_type)
    db.session.add(new_type)
    db.session.commit()
    return jsonify({'status': 'success', 'message': 'Custom section type added!'})


@app.route('/api/save_custom_section/', methods=['POST'])
def save_custom_section():
    if 'user_id' not in session:
        return jsonify({'status': 'error', 'message': 'Not logged in'}), 401

    data = request.get_json()
    date_str = data.get('date')
    section_name = data.get('sectionName')
    section_type = data.get('type')
    content = data.get('content') # For text type, or JSON string for time type

    if not date_str or not section_name or not section_type:
        return jsonify({'status': 'error', 'message': 'Missing data'}), 400

    section_date = datetime.strptime(date_str, '%Y-%m-%d').date()

    section = CustomSection.query.filter_by(
        user_id=session['user_id'],
        date=section_date,
        name=section_name
    ).first()

    if section:
        section.content = content
        section.type = section_type # Update type in case it was changed, though usually fixed by name
    else:
        section = CustomSection(
            user_id=session['user_id'],
            date=section_date,
            name=section_name,
            type=section_type,
            content=content
        )
        db.session.add(section)
    
    db.session.commit()
    return jsonify({'status': 'success', 'message': 'Custom section saved!'})

@app.route('/api/delete_custom_section/', methods=['POST'])
def delete_custom_section():
    if 'user_id' not in session:
        return jsonify({'status': 'error', 'message': 'Not logged in'}), 401

    data = request.get_json()
    date_str = data.get('date')
    section_name = data.get('sectionName')

    if not date_str or not section_name:
        return jsonify({'status': 'error', 'message': 'Date and section name are required'}), 400

    section_date = datetime.strptime(date_str, '%Y-%m-%d').date()

    section = CustomSection.query.filter_by(
        user_id=session['user_id'],
        date=section_date,
        name=section_name
    ).first()

    if section:
        db.session.delete(section)
        db.session.commit()
        return jsonify({'status': 'success', 'message': 'Custom section deleted!'})
    else:
        return jsonify({'status': 'error', 'message': 'Custom section not found'}), 404


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