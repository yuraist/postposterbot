from app import app, db
from flask import render_template, redirect
from flask_security import login_user, current_user, logout_user
from flask_security.utils import hash_password, verify_password
from app.models import User
from app.forms import SignUpForm, SignInForm


@app.route('/')
@app.route('/index')
def index():
    print(current_user)
    return render_template('index.html', user=current_user)


@app.route('/signup', methods=['GET', 'POST'])
def sign_up():
    error = None
    form = SignUpForm()

    if form.validate_on_submit():
        username = form.username.data
        password = hash_password(form.password.data)

        user = User(username=username, password=password)
        db.session.add(user)
        db.session.commit()
        user = User.query.filter_by(username=username).first()
        user.is_active = True
        login_user(user, remember=True)

        return redirect('index')
    else:
        print(form.errors)

    return render_template('signup.html', form=form, error=error)

@app.route('/signin', methods=['GET', 'POST'])
def login():
    error = None
    form = SignInForm()

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        user = User.query.filter_by(username=username).first()
        if verify_password(password, user.password):
            print(user.username)
            login_user(user, remember=True)

            return redirect('index')
    return render_template('signin.html', form=form, error=error)


@app.route('/logout')
def logout():
    logout_user()
    return redirect('index')


@app.route('/user/<username>')
def user(username):

    user = User.query.filter_by(username=username).first()
    print(user)
    return render_template('index.html', user=user)
