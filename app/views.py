from app import app, db
from flask import render_template, redirect, g, request, url_for
from flask_security import login_user, current_user, logout_user
from flask_security.utils import hash_password, verify_password
from app.models import User, Group, Post
from app.forms import SignUpForm, SignInForm, AddGroupForm, PostForm
from app.publisher import Publisher


@app.before_request
def before_request():
    g.user = current_user


@app.route('/')
@app.route('/index')
def index():
    form = AddGroupForm()
    post_form = PostForm()

    return render_template('index.html', user=current_user, form=form, post_form=post_form)


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

        return redirect(url_for('index'))
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

            return redirect(url_for('index'))
    return render_template('signin.html', form=form, error=error)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/add_group', methods=['POST'])
def add_group():
    form = AddGroupForm()
    if form.validate_on_submit():
        name = form.name.data
        app_id = form.app_id.data
        secure_key = form.secure_key.data
        access_token = form.access_token.data

        group = Group(name=name, app_id=app_id, secure_key=secure_key, access_token=access_token)
        group.user_id = g.user.id
        db.session.add(group)
        db.session.commit()
    return redirect(url_for('index'))


@app.route('/post', methods=['POST'])
def post():
    form = PostForm()
    if form.validate_on_submit():
        title = form.title.data
        url = form.url.data

        post = Post(title, url)
        group = Group.query.filter_by(user_id=current_user.id).first()
        publisher = Publisher(group)
        publisher.publish(post)

    return redirect(url_for('index'))
