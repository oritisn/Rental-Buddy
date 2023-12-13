from wtforms import StringField, SubmitField, IntegerField, RadioField, \
    DateField, EmailField, PasswordField, SelectMultipleField, BooleanField, SelectField, FileField
from flask_wtf import FlaskForm
from wtforms.validators import InputRequired, Email, Length, DataRequired, ValidationError

from models import User


class LoginForm(FlaskForm):
    username = StringField("Username ", validators=[InputRequired()])
    password = PasswordField("Password ", validators=[InputRequired()])
    email = EmailField("Email", validators=[InputRequired(), Email()])
    remember = BooleanField("Remember me")
    submit = SubmitField("Log In")


class LogoutForm(FlaskForm):
    submit = SubmitField("Log Out")


class PortalForm(FlaskForm):
    landlord = SubmitField("Landlord")
    tenant = SubmitField("Tenant")
    upload = SubmitField("upload")


class RegisterForm(FlaskForm):
    username = StringField("Username", validators=[InputRequired(), Length(min=2, max=20)])  # UNIQUE
    password = PasswordField("Password", validators=[InputRequired(), Length(min=3, message="Password too short")])
    confirm_password = PasswordField("Confirm Password", validators=[InputRequired()])
    email = EmailField(label="Email", validators=[InputRequired(), Email()])  # UNIQUE
    tenant = BooleanField("Tenant")
    landlord = BooleanField("Landlord")
    submit = SubmitField("Register")


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


class LeaseUploadForm(FlaskForm):
    lease = FileField()
    submit = SubmitField("Upload")


class RequestResetForm(FlaskForm):
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    submit = SubmitField('Request Password Reset')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is None:
            raise ValidationError('There is no account with that email. You must register first.')


class ResetPasswordForm(FlaskForm):
    password = PasswordField("Password", validators=[InputRequired(), Length(min=3, message="Password too short")])
    confirm_password = PasswordField("Confirm Password", validators=[InputRequired()])

    submit = SubmitField('Reset Password')
