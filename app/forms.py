from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, PasswordField, FileField, BooleanField, SubmitField, \
    DateField, IntegerField
from wtforms.validators import DataRequired, Email


class ContactForm(FlaskForm):
    name = StringField('Name', render_kw={"placeholder": 'Your name'}, validators=[DataRequired()])
    email = StringField('Email', render_kw={"placeholder": 'Your email'}, validators=[DataRequired(), Email()])
    message = TextAreaField('Message', render_kw={"placeholder": 'Your message','cols': 30, 'rows': 10},
                            validators=[DataRequired()])
    submit = SubmitField('Send Message')


# Admin Forms
class LoginForm(FlaskForm):
    username = StringField('Username',  validators=[DataRequired()], render_kw={'class': 'text-field'})
    password = PasswordField('Password', validators=[DataRequired()], render_kw={'class': 'text-field'})
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In', render_kw={'class': 'submit'})


class EditWork(FlaskForm):
    headline = StringField('Headline Work', render_kw={'class': 'text-field'})
    subline = StringField('Subline Work', render_kw={'class': 'text-field'})
    cover_image = FileField('Cover Image')
    submit_static = SubmitField('Save Changes', render_kw={'class': 'submit'})


class AddProject(FlaskForm):
    name = StringField('Project Name', render_kw={"placeholder": 'New Project Name', 'class': 'short'})
    submit_project = SubmitField('Add Project', render_kw={'class': 'add'})


class EditProject(FlaskForm):
    name = StringField('Project Name', render_kw={'class': 'text-field'})
    short_description = TextAreaField('Short Project Description', render_kw={'class': 'text-field'})
    main_image = FileField('Main Project Image')
    secondary_image = FileField('Secondary Project Image')
    date = DateField('Date', format='%Y-%m-%d', render_kw={'class': 'text-field'})
    long_description = TextAreaField('Long Project Description', render_kw={'class': 'text-field'})
    video = StringField('Video Embed Link', render_kw={'class': 'text-field'})
    url_name = StringField('URL name', render_kw={'class': 'text-field'})
    submit_editproject = SubmitField('Save Project', render_kw={'class': 'submit'})
    delete_project = SubmitField('Yes, Delete Project', render_kw={'class': 'delete'})


class AddProjectSection(FlaskForm):
    title = StringField('Section Title', render_kw={"placeholder": 'Add Section Title', 'class': 'short'})
    submit_section = SubmitField('Add Section', render_kw={'class': 'submit'})


class EditProjectSection(FlaskForm):
    order = IntegerField('Section Order', render_kw={"placeholder": 'Display Order', 'class': 'short'})
    paragraph = TextAreaField('Section paragraph', render_kw={'class': 'text-field'})
    title = StringField('Section Title', render_kw={'class': 'text-field'})
    image_1 = FileField('Section Image 1')
    image_2 = FileField('Section Image 2')
    image_3 = FileField('Section Image 3')
    submit_EditSection = SubmitField('Save Projection Section', render_kw={'class': 'submit'})
    delete_section = SubmitField('Delete Section', render_kw={'class': 'delete'})


class EditAbout(FlaskForm):
    headline_about = StringField('Headline About', render_kw={'class': 'text-field'})
    subline_about = StringField('Subline About', render_kw={'class': 'text-field'})
    paragraph_about = TextAreaField('Paragraph About', render_kw={'class': 'text-field', 'cols': 30, 'rows': 12})
    submit_about = SubmitField('Save Changes', render_kw={'class': 'submit'})


class AddCvEntry(FlaskForm):
    start = DateField('Date', format='%Y-%m-%d', render_kw={"placeholder": 'yyyy-mm-dd', 'class': 'short'})
    end = DateField('Date', format='%Y-%m-%d', render_kw={"placeholder": 'yyyy-mm-dd, leave empty for current',
                                                          'class': 'short'}, filters=[lambda x: x or None])
    workplace = StringField('CV Workplace', render_kw={"placeholder": 'New workplace', 'class': 'short'})
    paragraph = TextAreaField('Paragraph', render_kw={"placeholder": 'Describe what is learned ',
                                                      'class': 'text-field'})
    submit_cv = SubmitField('Add CV', render_kw={'class': 'add'})


class EditCv(FlaskForm):
    start = DateField('Date', format='%Y-%m-%d', render_kw={'class': 'short'})
    end = DateField('Date', format='%Y-%m-%d', render_kw={"placeholder": 'yyyy-mm-dd, leave empty for current',
                                                          'class': 'short'}, filters=[lambda x: x or None])
    workplace = StringField('Workplace', render_kw={'class': 'text-field'})
    paragraph = TextAreaField('Job Description', render_kw={'class': 'text-field'})
    submit_edit_cv = SubmitField('Save CV Changes', render_kw={'class': 'submit'})
    delete_cv = SubmitField('Delete Entry', render_kw={'class': 'delete'})


class AddCourseEntry(FlaskForm):
    course_name = StringField('Course Name', render_kw={"placeholder": 'New Course Entry', 'class': 'short'})
    paragraph = StringField('Course Description', render_kw={"placeholder": 'New Course Description',
                                                             'class': 'text-field'})
    submit_course = SubmitField('Add Course', render_kw={'class': 'add'})


class EditCourse(FlaskForm):
    order = IntegerField('Course Order', render_kw={"placeholder": 'Display Order', 'class': 'short'})
    course_name = StringField('Course Name', render_kw={'class': 'text-field'})
    paragraph = TextAreaField('Course Description', render_kw={'class': 'text-field'})
    submit_course = SubmitField('Save Changes', render_kw={'class': 'submit'})
    delete_course = SubmitField('Delete Entry', render_kw={'class': 'delete'})


class EditContact(FlaskForm):
    headline_contact = StringField('Headline Contact', render_kw={'class': 'text-field'})
    subline_contact = StringField('Subline Contact', render_kw={'class': 'text-field'})
    hidden_subline_contact = StringField('Hidden Subline Contact', render_kw={'class': 'text-field'})
    image_contact = FileField('Contact Image')
    submit_contact = SubmitField('Save Changes', render_kw={'class': 'submit'})


class AddSocial(FlaskForm):
    link = StringField('Link', render_kw={"placeholder": 'Social Link', 'class': 'short'})
    display = StringField('Display', render_kw={"placeholder": 'Display Name', 'class': 'short'})
    order = IntegerField('Social Order', render_kw={"placeholder": 'Display Order', 'class': 'short'})
    submit_social = SubmitField('Add Social Link', render_kw={'class': 'submit'})


class EditSocial(FlaskForm):
    link = StringField('Link', render_kw={"placeholder": 'Social Link', 'class': 'short'})
    display = StringField('Display', render_kw={"placeholder": 'Display Name', 'class': 'short'})
    order = IntegerField('Social Order', render_kw={"placeholder": 'Display Order', 'class': 'short'})
    submit_social = SubmitField('Save Social Link', render_kw={'class': 'submit'})
    delete_social = SubmitField('Delete Entry', render_kw={'class': 'delete'})


class EditExperiments(FlaskForm):
    headline_experiments = StringField('Headline Experiments', render_kw={'class': 'text-field'})
    subline_experiments = StringField('Subline Experiments', render_kw={'class': 'text-field'})
    submit_experiments = SubmitField('Save Changes', render_kw={'class': 'submit'})
