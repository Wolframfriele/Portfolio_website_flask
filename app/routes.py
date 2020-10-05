from flask import render_template, flash, url_for
from app import app
from app.models import Project, ProjectSection

@app.route('/')
@app.route('/index')
@app.route('/work')
def index():
    projects = Project.query.all()[::-1] #Requests the projects fom the database and orders them recent to older
    return render_template('work.html', title='Work', projects=projects)

@app.route('/about')
def about():
    return render_template('about.html', title='About')

@app.route('/contact')
def contact():
    return render_template('contact.html', title='Contact')

@app.route('/project/<url_name>')
def project(url_name):
    project = Project.query.filter_by(url_name=url_name).first_or_404()
    return render_template('project.html', title=project.name, project=project)