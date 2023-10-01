from flask import Flask, render_template, redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from sqlalchemy.exc import IntegrityError
from models import db, connect_db, User
from forms import RegisterForm, LoginForm
from errors import AuthError

app = Flask(__name__)

app.app_context().push()
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///flask_login'
app.config['SQLALCHEMY_ECHO'] = False
app.config['SECRET_KEY'] = 'secret'
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

connect_db(app)

toolbar = DebugToolbarExtension(app)


@app.route('/')
def get_root():
    """ Redirect to /register. """
    return redirect('/register')


@app.route('/register', methods=['GET', 'POST'])
def register():
    """ Get registration form or handle registration and redirect to /secret on success. """
    form = RegisterForm()
    if form.validate_on_submit():
        try:
            user = User.register(form)
            session['username'] = user.username
            return redirect('/secret')
        except IntegrityError:
            form.username.errors = ['Username taken!']

    return render_template('register.html', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    """ Get login form or handle login and redirect to /secret on success. """
    form = LoginForm()
    if form.validate_on_submit():
        try:
            user = User.login(form)
            session['username'] = user.username
            return redirect('/secret')
        except AuthError as error:
            flash(error.message, 'danger')
            return redirect('/login')

    return render_template('login.html', form=form)


@app.route('/secret')
def get_secret():
    """ Allows only authenticated users. """
    if session.get('username'):
        return "Hello secret."
    return redirect('/')
