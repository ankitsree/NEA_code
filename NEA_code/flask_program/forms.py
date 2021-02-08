from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length,EqualTo, Email,email_validator, ValidationError
from flask_program.models import User

class RegistrationForm(FlaskForm): #creates fields for registration form
    username = StringField('Username',
                validators=[DataRequired(), Length(min=3, max=20)])
    email = StringField('Email',
            validators=[DataRequired()])
    password = PasswordField('Password',validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password',
            validators=[DataRequired(),EqualTo('password')])
    sumbit = SubmitField('Sign up')

    def validate_username(self, username):#function to validate username and raises error if invalid data is entered
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('That username is taken. Please choose a different one.')

    def validate_email(self, email):#function to validate email and raises error if invalid email address is entered
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('That email is taken. Please choose a different one.')


class LoginForm(FlaskForm):
    username = StringField('Username',
                validators=[DataRequired(), Length(min=3, max=20)])
    password = PasswordField('Password',validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')