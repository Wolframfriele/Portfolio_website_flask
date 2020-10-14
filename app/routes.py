from flask import render_template, flash, url_for, redirect, request,send_from_directory
from flask_login import current_user, login_user, login_required, logout_user, login_manager
from app import app, db
from app.forms import LoginForm, ContactForm, EditWork, AddProject, EditProject, EditProjectSection, EditAbout, AddCvEntry
from app.models import StaticElements, Project, ProjectSection, CvEntry, CourseEntry, SocialMediaLink, User, Message
from app.email import send_confirmation_email, send_message_email
from werkzeug.utils import secure_filename
from config import Config
import os


@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static/img'), 'favicon.ico',
                               mimetype='image/vnd.microsoft.icon')


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
        send_message_email(message)
        send_confirmation_email(message)
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


# Admin Page

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


@app.route('/website-content', methods=['GET', 'POST'])
# @login_required
def website_content():
    static = StaticElements.query.first()
    projects = Project.query.all()[::-1]
    edit_work = EditWork()
    add_project = AddProject()

    if request.method == 'GET':
        edit_work.headline.data = static.headline_work
        edit_work.subline.data = static.subline_work

    elif edit_work.submit_static.data and edit_work.validate_on_submit():
        static.headline_work = edit_work.headline.data
        static.subline_work = edit_work.subline.data
        
        file = request.files['cover_image']
        if file and Config.allowed_file(file.filename):
            old_file = os.path.join(Config.UPLOAD_IMAGE, static.cover_image_work)
            file.save(os.path.join(Config.UPLOAD_IMAGE, secure_filename(file.filename)))
            static.cover_image_work = secure_filename(file.filename)
            os.remove(old_file)

        db.session.commit()
        flash('Changes are saved!')
        return redirect(url_for('website_content'))

    elif add_project.submit_project.data and add_project.validate_on_submit():
        new_project = Project(name=add_project.name.data,
                              url_name=secure_filename(add_project.name.data))
        db.session.add(new_project)
        db.session.commit()
        return redirect(request.referrer)

    return render_template('admin.html', title='Admin | Work', static=static, projects=projects, edit_work=edit_work,
                           add_project=add_project)


@app.route('/website-content/about')
@login_required
def website_content_about():
    static = StaticElements.query.first()
    cvs = CvEntry.query.order_by(CvEntry.order).all()[::-1]
    courses = CourseEntry.query.order_by(CourseEntry.order).all()[::-1]

    return render_template('about_admin.html', title='Admin | About', static=static, cvs=cvs, courses=courses)


@app.route('/website-content/contact')
@login_required
def website_content_contact():
    return render_template('contact_admin.html', title='Admin | Contact')


@app.route('/website-content/project/<url_name>', methods=['GET', 'POST'])
@login_required
def website_content_project(url_name):
    project = Project.query.filter_by(url_name=url_name).first_or_404()
    edit_project = EditProject()
    project_sections = ProjectSection.query.order_by(ProjectSection.order).all()
    edit_project_section = EditProjectSection()

    if request.method == 'GET':
        edit_project.name.data = project.name
        edit_project.short_description.data = project.short_description
        edit_project.date.data = project.date
        edit_project.long_description.data = project.long_description
        edit_project.video.data = project.video
        edit_project.url_name.data = project.url_name

    elif edit_project.submit_editproject.data and edit_project.validate_on_submit():
        project.name = edit_project.name.data
        project.short_description = edit_project.short_description.data
        project.date = edit_project.date.data
        project.long_description = edit_project.long_description.data
        project.video = edit_project.video.data
        project.url_name = edit_project.url_name.data

        file = request.files['main_image']
        if file and Config.allowed_file(file.filename):
            old_file = os.path.join(Config.UPLOAD_IMAGE, project.main_image)
            file.save(os.path.join(Config.UPLOAD_IMAGE, secure_filename(file.filename)))
            project.main_image = secure_filename(file.filename)
            os.remove(old_file)

        file = request.files['secondary_image']
        if file and Config.allowed_file(file.filename):
            old_file = os.path.join(Config.UPLOAD_IMAGE, project.secondary_image)
            file.save(os.path.join(Config.UPLOAD_IMAGE, secure_filename(file.filename)))
            project.secondary_image = secure_filename(file.filename)
            os.remove(old_file)

        db.session.commit()
        flash('Changes are saved!')
        return redirect(url_for('website_content_project', url_name=project.url_name))

    elif edit_project.delete_project.data and edit_project.validate_on_submit():
        db.session.delete(project)
        db.session.commit()
        flash('Project is deleted')
        return redirect(url_for('website_content'))

    return render_template('project_admin.html', title='Admin | Project', project=project, edit_project=edit_project,
                           project_sections=project_sections, edit_project_section=edit_project_section)

