from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, EmailField, TextAreaField
from wtforms.validators import InputRequired, Email, Regexp


class RegisterForm(FlaskForm):
    username = StringField(validators=[InputRequired()])
    password = PasswordField(validators=[InputRequired()])
    email = EmailField(validators=[InputRequired(), Email(
        message="Not a valid email address!")])
    first_name = StringField(validators=[InputRequired()])
    last_name = StringField(validators=[InputRequired()])


class LoginForm(FlaskForm):
    username = StringField(validators=[InputRequired()])
    password = PasswordField(validators=[InputRequired()])


class FeedbackForm(FlaskForm):
    title = StringField(validators=[InputRequired()])
    content = TextAreaField(validators=[InputRequired()])
