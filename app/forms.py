from flask_wtf import FlaskForm
from wtforms import StringField,TextAreaField, PasswordField, BooleanField, SubmitField, validators
from wtforms.validators import DataRequired, Email


class LoginForm(FlaskForm):
    username = StringField('Username',  validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')

class ContactForm(FlaskForm):
    name = StringField('Name', render_kw={"placeholder": 'Your name'}, validators=[DataRequired()])
    email = StringField('Email', render_kw={"placeholder": 'Your email'}, validators=[DataRequired(), Email()])
    message = TextAreaField('Message', render_kw={"placeholder": 'Your message','cols': 30, 'rows': 10}, validators=[DataRequired()])
    submit = SubmitField('Send Message')