from app import app, db
from app.models import Project, ProjectSection

#Makes testing in the shell easier by automaticly importing database models

@app.shell_context_processor
def make_shell_context():
   return {'db': db, 'Project': Project, 'ProjectSection': ProjectSection}