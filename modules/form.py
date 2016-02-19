from flask.ext.wtf import Form
from wtforms import StringField, PasswordField, SubmitField, HiddenField
from wtforms.validators import DataRequired, Length, Email


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
        Length(min=1, max=100, message='Password should be 1-100.')
    ])
    submit = SubmitField('Submit')
