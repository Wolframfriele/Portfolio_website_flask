from app import db, login
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from datetime import datetime


# Setting up table for Semi-Static elements
class StaticElements(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    headline_work = db.Column(db.String(255))
    subline_work = db.Column(db.Text)
    cover_image_work = db.Column(db.String(64))
    headline_about = db.Column(db.String(255))
    subline_about = db.Column(db.Text)
    paragraph_about = db.Column(db.Text)
    headline_contact = db.Column(db.String(255))
    subline_contact = db.Column(db.Text)
    hidden_subline_contact = db.Column(db.Text)
    image_contact = db.Column(db.String(64))
    headline_experiments = db.Column(db.String(255))
    subline_experiments = db.Column(db.Text)


# Setting up the table for project entries
class Project(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))
    short_description = db.Column(db.Text)
    main_image = db.Column(db.String(255))
    secondary_image = db.Column(db.String(255))
    date = db.Column(db.Date)
    long_description = db.Column(db.Text)
    video = db.Column(db.Text)
    project_section = db.relationship('ProjectSection', backref='main_project_info', lazy='dynamic')
    url_name = db.Column(db.String(64))
    
    def __repr__(self):
        return '<Project {}' .format(self.name)


# Setting up the table to extend project descriptions
class ProjectSection(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    project_id = db.Column(db.Integer, db.ForeignKey('project.id'))
    order = db.Column(db.Integer)
    paragraph = db.Column(db.Text)
    title = db.Column(db.String(64))
    image_1 = db.Column(db.String(255))
    image_2 = db.Column(db.String(255))
    image_3 = db.Column(db.String(255))

    def __repr__(self):
        return '<ProjectSection {}' .format(self.id)


# Setting up table for CV entries
class CvEntry(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    order = db.Column(db.Integer)
    start = db.Column(db.Date)
    end = db.Column(db.Date)
    workplace = db.Column(db.String(255))
    paragraph = db.Column(db.Text)


# Setting up table for Course entries
class CourseEntry(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    order = db.Column(db.Integer)
    course_name = db.Column(db.String(255))
    paragraph = db.Column(db.Text)


# Setting up tables for Social Media Links
class SocialMediaLink(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    order = db.Column(db.Integer)
    link = db.Column(db.String(255))
    display = db.Column(db.String(255))


# Setting up tables for messages
class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    name = db.Column(db.String(120))
    email = db.Column(db.String(120))
    message = db.Column(db.Text)


# setting up a table for Users
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True)
    email = db.Column(db.String(120), unique=True)
    password_hash = db.Column(db.String(128))

    def __repr__(self):
        return '<User {}>' .format(self.username)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


@login.user_loader
def load_user(id):
    return User.query.get(int(id))