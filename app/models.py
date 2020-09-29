from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, SubmitField, validators
from wtforms.validators import DataRequired
from wtforms.fields.html5 import EmailField

class ContactForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    email = EmailField('Email', validators=[DataRequired(), validators.Email()])
    message = StringField('Message', validators=[DataRequired()])
    submit = SubmitField('Submit')