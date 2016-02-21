from flask.ext.wtf import Form
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField, SelectField
from wtforms.validators import DataRequired, Length, Email, EqualTo


class LoginForm(Form):
    email = StringField('Email', validators=[
        DataRequired(message='Email is required.'),
        Email(message='Email format is invalid.'),
        Length(min=1, max=200, message='Email should be 1-200.')
    ])
    password = PasswordField('Password', validators=[
        DataRequired(message='Password is required.'),
        Length(min=1, max=100, message='Password should be 1-100.')
    ])
    submit = SubmitField('Login')


class SignupForm(Form):
    username = StringField('Username', validators=[
        DataRequired(message='Username is required.'),
        Length(min=1, max=200, message='Username should be 1-200.')
    ])
    email = StringField('Email', validators=[
        DataRequired(message='Email is required.'),
        Length(min=1, max=200, message='Email should be 1-200.')
    ])
    submit = SubmitField('Signup')


class PasswordForm(Form):
    password = PasswordField('Password', validators=[
        DataRequired(message='Password is required.'),
        Length(min=1, max=100, message='Password should be 1-100.')
    ])
    confirm = PasswordField('Confirm Password', validators=[
        DataRequired(message='Confirm Password is required.'),
        EqualTo('password', 'Please enter same password.'),
        Length(min=1, max=100, message='Password should be 1-100.')
    ])
    submit = SubmitField('Submit')


class TopicForm(Form):
    id = StringField('Unique ID', validators=[
        DataRequired('Unique ID is required.'),
        Length(min=3, max=25, message='Unique should be 3-25.')
    ])
    title = StringField('Title', validators=[
        DataRequired('Title is required.'),
        Length(min=1, max=100, message='Title should be 1-100.')
    ])
    description = TextAreaField('Description')
    is_public = BooleanField('Public')
    submit = SubmitField('Submit')


class EntryForm(Form):
    title = StringField('Title', validators=[
        DataRequired('Title is required.'),
        Length(min=1, max=50, message='Unique should be 1-50.')
    ])
    description = TextAreaField('Description', validators=[
        DataRequired('Title is required.'),
        Length(min=1, max=5000, message='Description should be 1-5000.')
    ])
    category = SelectField('Type', choices=[
        ('requirement', 'Requirement'), ('idea', 'Idea'),
        ('bug', 'Bug')
    ])
    show_user = BooleanField('Show User')
    submit = SubmitField('Submit')
