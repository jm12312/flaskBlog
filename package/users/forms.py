from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from flask_wtf.file import FileAllowed, FileField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from package.models import User
from flask_login import current_user

class RegistrationForm(FlaskForm):
    username = StringField("Username", 
                           validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired()])
    confirm_password = PasswordField("Confirm_Password", validators=[DataRequired(), EqualTo("password")])
    submit = SubmitField("Sign Up")

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user: 
            raise ValidationError("Username is taken.")
        
    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user: 
            raise ValidationError("Email is taken.")

class LoginForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired()])
    remember = BooleanField("Remeber Me")
    submit = SubmitField("Log In")

class UpdateForm(FlaskForm):
    username = StringField("Username", 
                           validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField("Email", validators=[DataRequired(), Email()])
    submit = SubmitField("Update Profile")
    image = FileField("Upload Your Profile Picture", validators=[FileAllowed(["jpg", "png", "jpeg"])])
    def validate_username(self, username):
        if username.data != current_user.username:
            user = User.query.filter_by(username=username.data).first()
            if user: 
                raise ValidationError("Username is taken.")
        
    def validate_email(self, email):
        if email.data != current_user.email:
            user = User.query.filter_by(email=email.data).first()
            if user: 
                raise ValidationError("Email is taken.")



class RequestResetForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired(), Email()])
    submit = SubmitField("Request password reset")
    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is None: 
            raise ValidationError("No account with Email address.")

class ResetPasswordForm(FlaskForm):
    password = PasswordField("Password", validators=[DataRequired()])
    confirm_password = PasswordField("Confirm_Password", validators=[DataRequired(), EqualTo("password")])
    submit = SubmitField("Reset Password")
