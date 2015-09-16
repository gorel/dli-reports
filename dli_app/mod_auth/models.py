from dli_app import db, login_manager

@login_manager.user_loader
def user_loader(user_id):
    return User.query.get(user_id)

class User(db.Model):
    __tablename__ = 'auth_user'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String, index=True, unique=True)
    # TODO: Add other columns

    def __init__(self):
        # TODO: Initialize new user and add it to the database
        # (may need more parameters)
        pass

    # Any user that is logged in is automatically authenticated.
    def is_authenticated(self):
        return True

    # All users are active. We don't have "deactivated" accounts.
    def is_active(self):
        return True

    def is_anonymous(self):
        return not self.is_authenticated()

    def get_id(self):
        return self.id

    def __repr__(self):
        return '<User %s>' % self.email

    @classmethod
    def get_by_email(cls, email):
        return User.query.filter_by(email=email).first()
