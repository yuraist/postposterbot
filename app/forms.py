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
    gid = StringField('Group ID', validators=[DataRequired()])


class PostForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    url = StringField('URL', validators=[DataRequired()])
