from dli_app import db, login_manager

@login_manager.user_loader
def user_loader(user_id):
    return User.query.get(user_id)

class User(db.Model):
    __tablename__ = 'auth_user'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))
    email = db.Column(db.String(64), index=True, unique=True)
    password = db.Column(db.String(128))
    is_admin = db.Column(db.Boolean)
    location = db.Column(db.Integer, db.ForeignKey("location.id"))

    def __init__(self):
        # TODO: Initialize new user and add it to the database
        # (may need more parameters)

        # Any user that is logged in is automatically authenticated.
        self._is_authenticated = True
        self._is_active = True

    @property
    def is_authenticated(self):
        return self._is_authenticated

    @property
    def is_active(self):
        return self._is_active

    @property
    def is_anonymous(self):
        return not self.is_authenticated()

    def get_id(self):
        return self.id

    def __repr__(self):
        return '<User %r>' % self.email

    @classmethod
    def get_by_email(cls, email):
        return User.query.filter_by(email=email).first()

class Location(db.Model):
    __tablename__ = "location"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=True, unique=True)

    def __repr__(self):
        return '<Location %r>' % self.name
