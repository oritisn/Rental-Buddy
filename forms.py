from wtforms import StringField, SubmitField, IntegerField, RadioField, \
    DateField, EmailField, PasswordField, SelectMultipleField, BooleanField, SelectField
from flask_wtf import FlaskForm
from wtforms.validators import InputRequired, Email


class LoginForm(FlaskForm):
    username = StringField("Username ", validators=[InputRequired()])
    password = PasswordField("Password ", validators=[InputRequired()])
    email = EmailField("Email", validators=[InputRequired(), Email()])

    remember = BooleanField("Remember me")
    login = SubmitField("Log In")


class LogoutForm(FlaskForm):
    submit = SubmitField("Log Out")


class UserForm(FlaskForm):
    username = StringField("Username", validators=[InputRequired()])
    password = PasswordField("Password", validators=[InputRequired()])
    confirm_password = PasswordField("Confirm Password", validators=[InputRequired()])
    category = RadioField("CATEGORY", choices=(("Teacher", "Teacher"), ("Student", "Student"))
                          , validators=[InputRequired()])
    email = EmailField(label="Email", validators=[InputRequired(), Email()])
    submit = SubmitField("Submit")


class SettingsForm(FlaskForm):
    password = PasswordField("PASSWORD")
    category = SelectField("CATEGORY", choices=(("Teacher", "teacher"), ("Student", "Student")))
    first_name = StringField("FIRST NAME")
    last_name = StringField("LAST NAME")
    email = EmailField("EMAIL")
    phone_number = StringField("PHONE NUMBER")
    address = StringField("ADDRESS")
    gender = RadioField("GENDER", choices=[("Male", "MALE"), ("Female", "FEMALE"), ("Other", "OTHER")])
    date_of_birth = DateField("DATE OF BIRTH")
    course_IELTS = BooleanField("IELTS")
    course_B1 = BooleanField("B1")
    course_Grammar = BooleanField("GRAMMAR")
    submit = SubmitField("Submit")
