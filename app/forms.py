from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import DataRequired


class SignUpForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('password', validators=[DataRequired()])


class SignInForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('password', validators=[DataRequired()])


class AddGroupForm(FlaskForm):
    name = StringField('Group name', validators=[DataRequired()])
    app_id = StringField('App ID', validators=[DataRequired()])
    secure_key = StringField('Secure key', validators=[DataRequired()])
    access_token = StringField('Access token', validators=[DataRequired()])

class PostForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    url = StringField('URL', validators=[DataRequired()])
