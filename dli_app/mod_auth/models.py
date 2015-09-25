"""Models for the auth module

Author: Logan Gore
This file is responsible for defining models that belong in the auth module.
"""

from flask_sqlalchemy import (
    orm,
)

from werkzeug.security import (
    generate_password_hash,
)

from dli_app import db, login_manager


@login_manager.user_loader
def user_loader(user_id):
    """Unique user loader for the login manager"""
    return User.query.get(user_id)


class RegisterCandidate(db.Model):
    """Model for users who are allowed to register on the site"""
    __tablename__ = 'register_candidate'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(64), index=True, unique=True)
    registration_key = db.Column(db.String(64))

    def __init__(self, email, registration_key):
        """Initialize a RegisterCandidate model"""
        self.email = email
        self.registration_key = registration_key

    def __repr__(self):
        """Return a descriptive representation of a RegisterCandidate"""
        return '<Register Candidate %r>' % self.email


class User(db.Model):
    """Model for users of the site"""
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))
    email = db.Column(db.String(64), index=True, unique=True)
    password = db.Column(db.String(128))
    is_admin = db.Column(db.Boolean)
    location = db.Column(db.Integer, db.ForeignKey("location.id"))

    def __init__(self, name, email, password, location):
        """Initialize a User model"""
        self.name = name
        self.email = email
        self.password = generate_password_hash(password)
        self.location = location
        self.is_admin = False

        self._is_authenticated = None
        self._is_active = None

        # Call the method to load local variables NOT stored in the db
        self.init_on_load()

    @orm.reconstructor
    def init_on_load(self):
        """Load code that isn't stored in the db model"""
        self._is_authenticated = True
        self._is_active = True

    @property
    def is_authenticated(self):
        """Return whether or not the user is authenticated (logged in)"""
        return self._is_authenticated

    @property
    def is_active(self):
        """Return whether or not the user's account is active on the site"""
        return self._is_active

    @property
    def is_anonymous(self):
        """Return whether or not the user is acting in an anonymous context"""
        return not self.is_authenticated()

    def get_id(self):
        """Return a unique identifier for the user"""
        return self.id

    def __repr__(self):
        """Return a descriptive representation of a User"""
        return '<User %r>' % self.email

    @classmethod
    def get_by_email(cls, email):
        """Retrieve a user by their email address"""
        return User.query.filter_by(email=email).first()


class Location(db.Model):
    """Model for DLI's physical locations"""
    __tablename__ = "location"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=True, unique=True)

    def __init__(self, name):
        """Initialize a Location model"""
        self.name = name

    def __repr__(self):
        """Return a descriptive representation of a Location"""
        return '<Location %r>' % self.name


class Department(db.Model):
    """Model for DLI's departments"""
    __tablename__ = "department"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=True, unique=True)

    def __init__(self, name):
        """Initialize a Department model"""
        self.name = name

    def __repr__(self):
        """Return a descriptive representation of a Department"""
        return '<Department %r>' % self.name
