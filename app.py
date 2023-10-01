from flask import Flask, render_template, redirect
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db
from forms import RegisterForm, LoginForm

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


@app.route('/register')
def get_register():
    """ Get registration form. """
    form = RegisterForm()
    return render_template('register.html', form=form)


@app.route('/register', methods=['POST'])
def post_register():
    """ Process registration and redirect to /secret on success. """
    return redirect('/')


@app.route('/login')
def get_login():
    """ Get login form. """
    form = LoginForm()
    return render_template('login.html', form=form)


@app.route('/login', methods=['POST'])
def post_login():
    """ Process login and redirect to /secret on success. """
    return redirect('/')


@app.route('/secret')
def get_secret():
    """ Allows only authenticated users. """
    return render_template('secret.html')
