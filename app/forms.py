from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField, TextAreaField, SelectField
from wtforms.validators import InputRequired

class SignUpForm(FlaskForm):
    first_name = StringField('First Name', validators=[InputRequired()])
    last_name = StringField('Last Name', validators=[InputRequired()])
    username = StringField('Username', validators=[InputRequired()])
    password = PasswordField('Password', validators=[InputRequired()])
    acctype = SelectField('Account Type', choices=[('leader', 'Project Leader'), ('member', 'Club Member')], validators=[InputRequired()])
    special_interest_group=SelectField('Special interest group',
    choices=[('mobile', 'Mobile App Development'), ('robot', 'Robotics'),('security', 'Cyber Security'),
    ('games', 'Game Development'),('web', 'Web Development')],validators=[InputRequired()])

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[InputRequired()])
    password = PasswordField('Password', validators=[InputRequired()])

class MessageForm(FlaskForm):
    title = StringField('Title', validators=[InputRequired()])
    message = TextAreaField('Message', validators=[InputRequired()])
    
class ProjectForm(FlaskForm):
    name = StringField('Project Name', validators=[InputRequired()])
    description = StringField('Description', validators=[InputRequired()])
    sig = StringField('SIG', validators=[InputRequired()])

class TaskForm(FlaskForm):
    assignee = StringField('Assignee Name', validators=[InputRequired()])
    description = StringField('Description', validators=[InputRequired()])