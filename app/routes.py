from flask import render_template, flash, url_for
from app import app

@app.route('/')
@app.route('/index')
@app.route('/work')
def index():
    return render_template('work.html', title='Work')

@app.route('/about')
def about():
    return render_template('about.html', title='About')

@app.route('/contact')
def contact():
    return render_template('contact.html', title='Contact')

@app.route('/project')
def project():
    return render_template('project.html', title='Project')