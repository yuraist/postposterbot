from app import db


class User(db.Model):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True)
    password = db.Column(db.String(255))

    groups = db.relationship('Group', backref='admin', lazy='dynamic')

    def __repr__(self):
        return '<User {}>'.format(self.username)


class Group(db.Model):
    __tablename__ = 'group'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))
    access_token = db.Column(db.String(255))
    secure_key = db.Column(db.String(128))
    app_id = db.Column(db.String(64))

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return '<Group {}>'.format(self.name)
