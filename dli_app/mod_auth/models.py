"""Models for the auth module

Author: Logan Gore
This file is responsible for defining models that belong in the auth module.
"""

import datetime
import os
import random
import string

from flask_login import UserMixin
from flask_mail import Message

from werkzeug.security import check_password_hash
from werkzeug.security import generate_password_hash

from dli_app import db
from dli_app import login_manager
from dli_app import mail

from dli_app.mod_admin.models import ErrorReport

from dli_app.mod_reports.models import Chart
from dli_app.mod_reports.models import Field
from dli_app.mod_reports.models import Report


report_users = db.Table(
    'report_users',
    db.Column('report_id', db.Integer, db.ForeignKey('report.id')),
    db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
)


chart_users = db.Table(
    'chart_users',
    db.Column('chart_id', db.Integer, db.ForeignKey('chart.id')),
    db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
)


@login_manager.user_loader
def user_loader(user_id):
    """Unique user loader for the login manager"""
    return User.query.get(user_id)


class RegisterCandidate(db.Model):
    """Model for users who are allowed to register on the site"""
    __tablename__ = 'register_candidate'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(64), index=True, unique=True)
    send_time = db.Column(db.String(32))
    registration_key = db.Column(db.String(64))

    def __init__(self, email, registration_key=None):
        """Initialize a RegisterCandidate model"""
        if registration_key is None:
            registration_key = ''.join(
                random.choice(string.ascii_letters + string.digits)
                for _ in range(60)
            )

        self.email = email
        self.registration_key = registration_key
        self.send_time = datetime.datetime.now().strftime('%m/%d/%Y %I:%M %p')

    def __repr__(self):
        """Return a descriptive representation of a RegisterCandidate"""
        return '<Register Candidate %r>' % self.email

    def send_link(self):
        """Send a registration link to this user"""
        key = self.registration_key
        title = 'Activate your account'
        content = 'Please go to the link: {url}'
        url = '{site}/auth/register/{key}'.format(
            site=os.environ['DLI_REPORTS_SITE_URL'],
            key=key,
        )
        recipient = self.email
        msg = Message(title, recipients=[recipient])
        msg.body = content.format(url=url)
        mail.send(msg)


class PasswordReset(db.Model):
    """Model for password reset key"""
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    key = db.Column(db.String(64))
    expiration = db.Column(db.DateTime)

    def __init__(self, user, key=None):
        """Initialize a  model"""
        if key is None:
            key = ''.join(random.choice(
                string.ascii_letters
                + string.digits) for _ in range(60))
        self.user = user
        self.key = key
        # Add one additional day so the user can potentially reset their password at midnight
        self.expiration = datetime.datetime.now() + datetime.timedelta(days=8)

    def __repr__(self):
        """Return a descriptive representation of password reset"""
        return '<Reset password for user %r>' % self.user

    @classmethod
    def get_by_key(cls, key):
        """Retrieve a user by the associated password reset key"""
        pw_reset = PasswordReset.query.filter_by(key=key).first()
        if pw_reset is not None:
            return pw_reset.user
        else:
            return None


class User(db.Model, UserMixin):
    """Model for users of the site"""
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))
    email = db.Column(db.String(64), index=True, unique=True)
    password = db.Column(db.String(128))
    is_admin = db.Column(db.Boolean)
    location_id = db.Column(db.Integer, db.ForeignKey("location.id"))
    dept_id = db.Column(db.Integer, db.ForeignKey("department.id"))
    pw_reset = db.relationship(
        PasswordReset,
        backref="user",
    )
    reports = db.relationship(
        Report,
        backref="user",
    )
    charts = db.relationship(
        Chart,
        backref="user",
    )
    error_reports = db.relationship(
        ErrorReport,
        backref="user",
    )
    favorite_reports = db.relationship(
        Report,
        secondary=report_users,
        backref='favorite_users',
    )
    favorite_charts = db.relationship(
        Chart,
        secondary=chart_users,
        backref='favorite_users',
    )

    def __init__(self, name, email, password, location, department):
        """Initialize a User model"""
        self.name = name
        self.email = email
        self.password = generate_password_hash(password)
        self.location = location
        self.department = department
        self.is_admin = False

    def set_password(self, new_password):
        """Change the user's password to the new password"""
        self.password = generate_password_hash(new_password)

    def check_password(self, password):
        """Check the user's password against the given value"""
        return check_password_hash(self.password, password)

    def favorite(self, report):
        """Add a report to the user's list of favorite reports"""
        if report not in self.favorite_reports:
            self.favorite_reports.append(report)

    def unfavorite(self, report):
        """Remove a report from the user's list of favorite reports"""
        if report in self.favorite_reports:
            self.favorite_reports.remove(report)

    def favorite_chart(self, chart):
        """Add a chart to the user's list of favorite charts"""
        if chart not in self.favorite_charts:
            self.favorite_charts.append(chart)

    def unfavorite_chart(self, chart):
        """Remove a chart from the user's list of favorite charts"""
        if chart in self.favorite_charts:
            self.favorite_charts.remove(chart)

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
    users = db.relationship(
        User,
        backref="location",
    )

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
    users = db.relationship(
        User,
        backref="department",
        lazy="dynamic",
    )
    fields = db.relationship(
        Field,
        backref="department",
    )

    def __init__(self, name):
        """Initialize a Department model"""
        self.name = name

    def __repr__(self):
        """Return a descriptive representation of a Department"""
        return '<Department %r>' % self.name
