from flask import render_template, flash, url_for, redirect, request,send_from_directory
from flask_login import current_user, login_user, login_required, logout_user, login_manager
from app import app, db
from app.forms import LoginForm, ContactForm, EditWork, AddProject, EditProject, EditProjectSection, AddProjectSection,\
    EditAbout, AddCvEntry, EditCv, AddCourseEntry, EditCourse, EditContact, AddSocial, EditSocial
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
    cvs = CvEntry.query.order_by(CvEntry.start).all()[::-1]
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
@login_required
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
            delete_old = False
            if static.cover_image_work:
                delete_old = True
                old_file = os.path.join(Config.UPLOAD_IMAGE, static.cover_image_work)
            file.save(os.path.join(Config.UPLOAD_IMAGE, secure_filename(file.filename)))
            static.cover_image_work = secure_filename(file.filename)
            if delete_old == True:
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


@app.route('/website-content/about', methods=['GET', 'POST'])
@login_required
def website_content_about():
    static = StaticElements.query.first()
    cvs = CvEntry.query.order_by(CvEntry.start).all()[::-1]
    courses = CourseEntry.query.order_by(CourseEntry.order).all()[::-1]
    edit_about = EditAbout()
    add_cv = AddCvEntry()
    add_course = AddCourseEntry()

    if request.method == 'GET':
        edit_about.headline_about.data = static.headline_about
        edit_about.subline_about.data = static.subline_about
        edit_about.paragraph_about.data = static.paragraph_about

    elif edit_about.submit_about.data and edit_about.validate_on_submit():
        static.headline_about = edit_about.headline_about.data
        static.subline_about = edit_about.subline_about.data
        static.paragraph_about = edit_about.paragraph_about.data
        db.session.commit()
        flash('Changes are saved!')
        return redirect(request.referrer)

    elif add_cv.submit_cv.data and add_cv.validate_on_submit():
        new_cv = CvEntry()
        add_cv.populate_obj(new_cv)
        db.session.add(new_cv)
        db.session.commit()
        return redirect(request.referrer)

    elif add_course.submit_course.data and add_course.validate_on_submit():
        new_course = CourseEntry()
        add_course.populate_obj(new_course)
        new_course.order = len(courses) + 1
        db.session.add(new_course)
        db.session.commit()
        return redirect(request.referrer)

    return render_template('about_admin.html', title='Admin | About', static=static, cvs=cvs, courses=courses,
                           edit_about=edit_about, add_cv=add_cv, add_course=add_course)


@app.route('/website-content/cv/<id>', methods=['GET', 'POST'])
@login_required
def website_content_cv(id):
    cv = CvEntry.query.filter_by(id=id).first_or_404()
    edit_cv = EditCv(obj=cv)

    if edit_cv.submit_edit_cv.data and edit_cv.validate_on_submit():
        edit_cv.populate_obj(cv)
        db.session.commit()
        flash('Entry updated.')
        return redirect(url_for('website_content_about'))

    elif edit_cv.delete_cv.data and edit_cv.validate_on_submit():
        db.session.delete(cv)
        db.session.commit()
        flash('Project is deleted')
        return redirect(url_for('website_content_about'))

    return render_template('cv_admin.html', title='Admin | About', cv=cv, edit_cv=edit_cv)


@app.route('/website-content/course/<id>', methods=['GET', 'POST'])
@login_required
def website_content_course(id):
    course = CourseEntry.query.filter_by(id=id).first_or_404()
    edit_course = EditCourse(obj=course)

    if edit_course.submit_course.data and edit_course.validate_on_submit():
        edit_course.populate_obj(course)
        db.session.commit()
        flash('Entry updated.')
        return redirect(url_for('website_content_about'))

    elif edit_course.delete_course.data and edit_course.validate_on_submit():
        db.session.delete(course)
        db.session.commit()
        flash('Project is deleted')
        return redirect(url_for('website_content_about'))

    return render_template('course_admin.html', title='Admin | About', course=course, edit_course=edit_course)


@app.route('/website-content/contact', methods=['GET', 'POST'])
@login_required
def website_content_contact():
    static = StaticElements.query.first()
    socials = SocialMediaLink.query.order_by(SocialMediaLink.order).all()
    messages = Message.query.order_by(Message.date).all()
    edit_contact = EditContact()
    add_social = AddSocial()

    if request.method == 'GET':
        edit_contact.headline_contact.data = static.headline_contact
        edit_contact.subline_contact.data = static.subline_contact
        edit_contact.hidden_subline_contact.data = static.hidden_subline_contact

    elif add_social.submit_social.data and add_social.validate_on_submit():
        new_social = SocialMediaLink()
        add_social.populate_obj(new_social)
        db.session.add(new_social)
        db.session.commit()
        flash('Social link added.')
        return redirect(url_for('website_content_contact'))

    return render_template('contact_admin.html', title='Admin | Contact', static=static, socials=socials,
                           edit_contact=edit_contact, add_social=add_social, messages=messages)


@app.route('/website-content/contact/<id>', methods=['GET', 'POST'])
@login_required
def website_content_social(id):
    social = SocialMediaLink.query.filter_by(id=id).first_or_404()
    edit_social = EditSocial(obj=social)

    if edit_social.submit_social.data and edit_social.validate_on_submit():
        edit_social.populate_obj(social)
        db.session.commit()
        flash('Social Link saved.')
        return redirect(url_for('website_content_contact'))

    elif edit_social.delete_social.data and edit_social.validate_on_submit():
        db.session.delete(social)
        db.session.commit()
        flash('Social link deleted.')
        return redirect(url_for('website_content_contact'))
    
    return render_template('social_admin.html', title='Admin | Contact', social=social, edit_social=edit_social)


@app.route('/website-content/project/<url_name>', methods=['GET', 'POST'])
@login_required
def website_content_project(url_name):
    project = Project.query.filter_by(url_name=url_name).first_or_404()
    edit_project = EditProject()
    project_sections = ProjectSection.query.order_by(ProjectSection.order).filter_by(project_id=project.id)
    edit_project_section = EditProjectSection()
    add_section = AddProjectSection()

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
        if edit_project.video.data == '':
            project.video = None
        else:
            project.video = edit_project.video.data
        project.url_name = edit_project.url_name.data

        file = request.files['main_image']
        if file and Config.allowed_file(file.filename):
            delete_old = False
            if project.main_image:
                delete_old = True
                old_file = os.path.join(Config.UPLOAD_IMAGE, project.main_image)
            file.save(os.path.join(Config.UPLOAD_IMAGE, secure_filename(file.filename)))
            project.main_image = secure_filename(file.filename)
            if delete_old == True:
                os.remove(old_file)

        file = request.files['secondary_image']
        if file and Config.allowed_file(file.filename):
            delete_old = False
            if project.secondary_image:
                delete_old = True
                old_file = os.path.join(Config.UPLOAD_IMAGE, project.secondary_image)
            file.save(os.path.join(Config.UPLOAD_IMAGE, secure_filename(file.filename)))
            project.secondary_image = secure_filename(file.filename)
            if delete_old == True:
                os.remove(old_file)

        db.session.commit()
        flash('Changes are saved!')
        return redirect(url_for('website_content_project', url_name=project.url_name))

    elif add_section.submit_section.data and add_section.validate_on_submit():
        new_section = ProjectSection(project_id=project.id)
        section_counter = 0
        for i in project_sections:
            section_counter += 1
        new_section.order = section_counter + 1
        new_section.title = add_section.title.data
        db.session.add(new_section)
        db.session.commit()
        flash('New section created.')
        return redirect(request.referrer)

    elif edit_project.delete_project.data and edit_project.validate_on_submit():
        for section in project_sections:
            db.session.delete(section)
        db.session.delete(project)
        db.session.commit()
        flash('Project is deleted')
        return redirect(url_for('website_content'))

    return render_template('project_admin.html', title='Admin | Project', project=project, edit_project=edit_project,
                           project_sections=project_sections, add_section=add_section,
                           edit_project_section=edit_project_section)


@app.route('/website-content/project/<url_name>/<id>', methods=['GET', 'POST'])
@login_required
def website_content_section(id, url_name):
    url_name = url_name
    section = ProjectSection.query.filter_by(id=id).first_or_404()
    edit_section = EditProjectSection(obj=section)

    if edit_section.submit_EditSection.data and edit_section.validate_on_submit():
        section.order = edit_section.order.data
        section.title = edit_section.title.data
        section.paragraph = edit_section.paragraph.data

        file = request.files['image_1']
        if file and Config.allowed_file(file.filename):
            delete_old = False
            if section.image_1:
                delete_old = True
                old_file = os.path.join(Config.UPLOAD_IMAGE, section.image_1)
            file.save(os.path.join(Config.UPLOAD_IMAGE, secure_filename(file.filename)))
            section.image_1 = secure_filename(file.filename)
            if delete_old == True:
                os.remove(old_file)

        file = request.files['image_2']
        if file and Config.allowed_file(file.filename):
            delete_old = False
            if section.image_2:
                delete_old = True
                old_file = os.path.join(Config.UPLOAD_IMAGE, section.image_2)
            file.save(os.path.join(Config.UPLOAD_IMAGE, secure_filename(file.filename)))
            section.image_2 = secure_filename(file.filename)
            if delete_old == True:
                os.remove(old_file)

        db.session.commit()
        flash('Section updated.')
        return redirect(url_for('website_content_project', url_name=url_name))

    elif edit_section.delete_section.data and edit_section.validate_on_submit():
        if section.image_1:
            old_file_1 = os.path.join(Config.UPLOAD_IMAGE, section.image_1)
            os.remove(old_file_1)
        if section.image_2:
            old_file_2 = os.path.join(Config.UPLOAD_IMAGE, section.image_2)
            os.remove(old_file_2)
        db.session.delete(section)
        db.session.commit()
        flash('Section is deleted')
        return redirect(url_for('website_content_project', url_name=url_name))

    return render_template('section_admin.html', title='Admin | About', section=section, edit_section=edit_section)