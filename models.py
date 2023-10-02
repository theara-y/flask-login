from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import IntegrityError
from flask_bcrypt import Bcrypt
from forms import RegisterForm, LoginForm, FeedbackForm
from errors import AuthError

db = SQLAlchemy()
bcrypt = Bcrypt()


def connect_db(app):
    db.init_app(app)
    db.create_all()


class User(db.Model):
    __tablename__ = 'users'
    username = db.Column(db.String(20), primary_key=True)
    password = db.Column(db.Text, nullable=False)
    email = db.Column(db.String(50), nullable=False)
    first_name = db.Column(db.String(3), nullable=False)
    last_name = db.Column(db.String(3), nullable=False)
    feedbacks = db.relationship('Feedback', cascade='all,delete,delete-orphan')

    def __repr__(self):
        return f'<User username={self.username}>'

    @classmethod
    def register(cls, form: RegisterForm):
        """ Throws IntegrityError if users exists. """
        hashed_password = bcrypt.generate_password_hash(form.password.data)
        hashed_password_utf8 = hashed_password.decode('utf8')
        user = cls(
            username=form.username.data,
            password=hashed_password_utf8,
            email=form.email.data,
            first_name=form.first_name.data,
            last_name=form.last_name.data)
        db.session.add(user)
        db.session.commit()
        return user

    @classmethod
    def login(cls, form: LoginForm):
        """ Throws AuthError on bad login. """
        user = User.query.get(form.username.data)
        if user:
            if bcrypt.check_password_hash(user.password, form.password.data):
                return user
        raise AuthError(
            'The username and/or password you have entered is incorrect.')


class Feedback(db.Model):
    __tablename__ = 'feedbacks'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    username = db.Column(db.String(20), db.ForeignKey('users.username'))
    user = db.relationship('User')

    def __repr__(self):
        return f'<Feedback username={self.username} title={self.title}>'

    @classmethod
    def submit(cls, username, form: FeedbackForm):
        """ Submits feedback. """
        feedback = cls(
            title=form.title.data,
            content=form.content.data,
            username=username
        )
        db.session.add(feedback)
        db.session.commit()

    @classmethod
    def update(cls, feedback, form: FeedbackForm):
        """ Updates feedback. """
        feedback.title = form.title.data
        feedback.content = form.content.data
        db.session.commit()

    @classmethod
    def delete(cls, id):
        """ Deletes feedback. """
        feedback = Feedback.query.get(id)
        db.session.delete(feedback)
        db.session.commit()
