from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, BooleanField, PasswordField
from wtforms.fields.html5 import TelField, DateField
from wtforms.validators import Length, Email, EqualTo, DataRequired, ValidationError


class LoginForm(FlaskForm):
    email_phone = StringField('Email or number phone', validators=[
        DataRequired(), Length(min=4, max=64)])
    password = PasswordField('Password', validators=[
        DataRequired(), Length(min=6, max=12)])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('LogIn')

    # def validate_email_phone(self, email_phone):



class RegisterForm(FlaskForm):
    username = StringField('Name', validators=[
        DataRequired(), Length(min=3, max=20)])
    email = StringField('Email', validators=[
        DataRequired(), Length(min=4, max=64), Email()])
    phone = StringField('Number phone')
    password1 = PasswordField('Password', validators=[
        DataRequired(), Length(min=6, max=12)])
    password2 = PasswordField('Repeat password', validators=[
        DataRequired(), Length(min=6, max=12), EqualTo('password1')])
    submit = SubmitField('Create user')