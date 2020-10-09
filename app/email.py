from flask_mail import Message
from flask import render_template
from app import app, mail


def send_email(subject, sender, recipients, text_body, html_body):
    msg = Message(subject, sender=sender, recipients=recipients)
    msg.body = text_body
    msg.html = html_body
    mail.send(msg)


def send_confirmation_email(message):
    send_email('[CONFIRMATION] I got your message!',
               sender=app.config['ADMINS'][1],
               recipients=[message.email],
               text_body=render_template('email/confirmation_email.txt',
                                         message=message),
               html_body=render_template('email/confirmation_email.html',
                                         message=message))


def send_message_email(message):
    send_email('New message from: ' + message.name,
               sender=app.config['ADMINS'][1],
               recipients=[app.config['ADMINS'][0]],
               text_body=render_template('email/send_message_email.txt',
                                         message=message),
               html_body=render_template('email/send_message_email.html',
                                         message=message))
