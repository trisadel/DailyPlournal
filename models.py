from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, date

db = SQLAlchemy()


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    profile_pic = db.Column(db.String(255), nullable=True)
    date_joined = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationships
    journals = db.relationship('JournalEntry', backref='author', lazy=True)
    streak = db.relationship('Streak', backref='user', uselist=False)
    templates = db.relationship('Template', backref='user', lazy=True)
    notes = db.relationship('Note', backref='user', lazy=True)
    habits = db.relationship('Habit', backref='user', lazy=True)
    habit_statuses = db.relationship('HabitStatus', backref='user', lazy=True)
    custom_sections = db.relationship('CustomSection', backref='user', lazy=True)

class JournalEntry(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text, nullable=False, default='note')
    type = db.Column(db.String(50), nullable=False)
    date_posted = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    # New fields
    mood = db.Column(db.String(50), nullable=True)  # Add mood


class Streak(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    current_streak = db.Column(db.Integer, default=0)
    last_login_date = db.Column(db.Date, nullable=True)

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)


class Template(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    date = db.Column(db.Date, nullable=False)
    content = db.Column(db.Text, nullable=False)
    __table_args__ = (db.UniqueConstraint('user_id', 'date', name='_user_date_note_uc'),)


class Habit(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    __table_args__ = (db.UniqueConstraint('user_id', 'name', name='_user_name_habit_uc'),)


class HabitStatus(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    habit_id = db.Column(db.Integer, db.ForeignKey('habit.id'), nullable=False)
    date = db.Column(db.Date, nullable=False)
    completed = db.Column(db.Boolean, default=False)
    habit = db.relationship('Habit', backref=db.backref('statuses', lazy=True))
    __table_args__ = (db.UniqueConstraint('habit_id', 'date', name='_habit_date_status_uc'),)


class CustomSectionType(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    # 'text' or 'time'
    type = db.Column(db.String(50), nullable=False)
    __table_args__ = (db.UniqueConstraint('user_id', 'name', name='_user_name_custom_section_type_uc'),)


class CustomSection(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    date = db.Column(db.Date, nullable=False)
    name = db.Column(db.String(100), nullable=False) # Name of the section (e.g., "Daily Goals")
    type = db.Column(db.String(50), nullable=False) # 'text' or 'time'
    content = db.Column(db.Text, nullable=True) # Stores text content or JSON string for time slots
    __table_args__ = (db.UniqueConstraint('user_id', 'date', 'name', name='_user_date_name_custom_section_uc'),)