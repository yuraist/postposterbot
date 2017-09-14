from app import app, db
from flask_security import SQLAlchemyUserDatastore, UserMixin, RoleMixin, Security


roles_users = db.Table('roles_users', db.Column('user_id', db.Integer(), db.ForeignKey('user.id')),
                       db.Column('role_id', db.Integer(), db.ForeignKey('role.id')))


class Role(db.Model, RoleMixin):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(80), unique=True)
    description = db.Column(db.String(255))


class User(db.Model, UserMixin):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True)
    password = db.Column(db.String(255))
    is_active = db.Column(db.Boolean())

    groups = db.relationship('Group', backref='admin', lazy='dynamic')

    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.is_active = True

    def __repr__(self):
        return '<User {}>'.format(self.username)


class Group(db.Model):
    __tablename__ = 'group'

    id = db.Column(db.Integer, primary_key=True)
    gid = db.Column(db.String(64))

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __init__(self, gid):
        self.gid = gid


    def __repr__(self):
        return '<Group {}>'.format(self.name)


class Post(db.Model):
    __tablename__ = 'post'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255))
    url = db.Column(db.String(), unique=True)
    is_published = db.Column(db.Boolean, default=False)

    def __init__(self, title, url):
        self.title = title
        self.url = url


user_datastore = SQLAlchemyUserDatastore(db, User, Role)
security = Security(app, user_datastore)
