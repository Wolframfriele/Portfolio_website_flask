from flask import render_template, flash, url_for
from app import app
from app.models import StaticElements, Project, ProjectSection, CvEntry, CourseEntry, SocialMediaLink

@app.route('/')
@app.route('/index')
@app.route('/work')
def index():
    static = StaticElements.query.first()
    projects = Project.query.all()[::-1] #Requests the projects fom the database and orders them recent to older
    socials = SocialMediaLink.query.order_by(SocialMediaLink.order).all()
    return render_template('work.html', title='Work', projects=projects, static=static, socials=socials)

@app.route('/about')
def about():
    static = StaticElements.query.first()
    cvs = CvEntry.query.order_by(CvEntry.order).all()[::-1]
    courses = CourseEntry.query.order_by(CourseEntry.order).all()[::-1]
    socials = SocialMediaLink.query.order_by(SocialMediaLink.order).all()
    return render_template('about.html', title='About', static=static, cvs=cvs, courses=courses, socials=socials)

@app.route('/contact')
def contact():
    static = StaticElements.query.first()
    socials = SocialMediaLink.query.order_by(SocialMediaLink.order).all()
    return render_template('contact.html', title='Contact', static=static, socials=socials)

@app.route('/project/<url_name>')
def project(url_name):
    project = Project.query.filter_by(url_name=url_name).first_or_404()
    sections = ProjectSection.query.order_by(ProjectSection.order).filter_by(project_id=project.id)
    socials = SocialMediaLink.query.order_by(SocialMediaLink.order).all()
    return render_template('project.html', title=project.name, project=project, sections=sections, socials=socials)