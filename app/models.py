from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, SubmitField, validators
from wtforms.validators import DataRequired
from wtforms.fields.html5 import EmailField
from datetime import date
from app import db


#Setting up table for Semi-Static elements
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

#Setting up the table to extend project descriptions
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

#Setting up table for CV entries
class CvEntry(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    order = db.Column(db.Integer)
    start = db.Column(db.Date)
    end = db.Column(db.Date)
    workplace = db.Column(db.String(255))
    paragraph = db.Column(db.Text)

#Setting up table for Course entries
class CourseEntry(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    order = db.Column(db.Integer)
    course_name = db.Column(db.String(255))
    paragraph = db.Column(db.Text)

#Setting up tables for Social Media Links
class SocialMediaLink(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    order = db.Column(db.Integer)
    link = db.Column(db.String(255))
    display = db.Column(db.String(255))

# class ContactForm(FlaskForm):
#     name = StringField('Name', validators=[DataRequired()])
#     email = EmailField('Email', validators=[DataRequired(), validators.Email()])
#     message = StringField('Message', validators=[DataRequired()])
#     submit = SubmitField('Submit')