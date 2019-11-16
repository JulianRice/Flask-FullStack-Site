from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Email, Length, EqualTo, ValidationError
from application.models import User

class LoginForm(FlaskForm):
    #The labels for the form, not the actual content
    email       = StringField("Email",      validators=[DataRequired(), Email()])
    password    = PasswordField("Password",   validators=[DataRequired(), Length(min=6,max=15)])
    rememberMe  = BooleanField("Remember Me")
    submit      = SubmitField("Login")

class RegisterForm(FlaskForm):
    email       = StringField("Email",              validators=[DataRequired(), Email()])
    #username    = StringField("Username",           validators=[DataRequired()])
    password    = PasswordField("Password",           validators=[DataRequired(), Length(min=6,max=15)])
    password2   = PasswordField("Confirm Password",   validators=[DataRequired(), Length(min=6,max=15), EqualTo('password')])
    firstName   = StringField("First Name",         validators=[DataRequired(), Length(min=2,max=55)])
    lastName    = StringField("Last Name",          validators=[DataRequired(), Length(min=2,max=55)])
    submit      = SubmitField("Register")

    def validate_email(self, email):
        user = User.objects(email=email.data).first()
        if user:
            raise ValidationError("Email is already in use. Please use another email")