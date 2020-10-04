from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, SubmitField, validators
from wtforms.validators import DataRequired
from wtforms.fields.html5 import EmailField
from datetime import date
from app import db

# class ContactForm(FlaskForm):
#     name = StringField('Name', validators=[DataRequired()])
#     email = EmailField('Email', validators=[DataRequired(), validators.Email()])
#     message = StringField('Message', validators=[DataRequired()])
#     submit = SubmitField('Submit')

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
    
    def __repr__(self):
        return '<Project {}' .format(self.name)

#Setting up the table to extend project descriptions
class ProjectSection(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    project_id = db.Column(db.Integer, db.ForeignKey('project.id'))
    order = db.Column(db.Integer)
    html = db.Column(db.Text)

    def __repr__(self):
        return '<ProjectSection {}' .format(self.id)
