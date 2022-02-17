from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, validators


class RegisterForm(FlaskForm):
    login = StringField('Login', [validators.DataRequired(), validators.Length(min=3, max=50)])
    password1 = PasswordField('Password', [validators.DataRequired(), validators.Length(min=7, max=50), validators.EqualTo('password2',message='Passwords must match')])
    password2 = PasswordField('Password confirm', [validators.DataRequired(), validators.Length(min=7, max=50)])

class LoginForm(FlaskForm):
    login = StringField('Login', [validators.DataRequired()])
    password = PasswordField('Password', [validators.DataRequired()])

class ChangePasswordForm(FlaskForm):
    old_password = PasswordField('Old password', [validators.DataRequired()])
    new_password = PasswordField('New password', [validators.DataRequired(), validators.Length(min=7, max=50)])
    new_password_confirmation = PasswordField('New password confirmation', [validators.DataRequired(), validators.Length(min=7, max=50), validators.EqualTo('new_password',message='Passwords must match')])