from flask import render_template, flash, url_for, redirect
from flask_login import current_user, login_user, login_required, logout_user, login_manager
from app import app, db
from app.forms import LoginForm, ContactForm
from app.models import StaticElements, Project, ProjectSection, CvEntry, CourseEntry, SocialMediaLink, User, Message

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

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    static = StaticElements.query.first()
    socials = SocialMediaLink.query.order_by(SocialMediaLink.order).all()
    form = ContactForm()
    if form.validate_on_submit():
        message = Message(name=form.name.data, email=form.email.data, message=form.message.data)
        db.session.add(message)
        db.session.commit()
        flash("You're message has been sent! You will also receive confirmation by email.")
        return redirect(url_for('contact'))
    return render_template('contact.html', title='Contact', static=static, form=form, socials=socials)

@app.route('/project/<url_name>')
def project(url_name):
    project = Project.query.filter_by(url_name=url_name).first_or_404()
    sections = ProjectSection.query.order_by(ProjectSection.order).filter_by(project_id=project.id)
    socials = SocialMediaLink.query.order_by(SocialMediaLink.order).all()
    return render_template('project.html', title=project.name, project=project, sections=sections, socials=socials)

@app.errorhandler(404)
def not_found_error(error):
    socials = SocialMediaLink.query.order_by(SocialMediaLink.order).all()
    return render_template('404.html', socials=socials), 404

@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    socials = SocialMediaLink.query.order_by(SocialMediaLink.order).all()
    return render_template('500.html', socials=socials), 500

@app.route('/behind-the-scenes', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('website_content'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        return redirect(url_for('website_content'))
    socials = SocialMediaLink.query.order_by(SocialMediaLink.order).all()
    return render_template('log-in.html', title='Log In', form=form, socials=socials)

@app.route('/logout')
def logout():
    logout_user()
    flash("You have been logged out!")
    return redirect(url_for('index'))

@app.route('/website-content')
@login_required
def website_content():
    return render_template('admin.html')

