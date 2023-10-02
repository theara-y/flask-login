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
    """ Redirect to /login. """
    return redirect('/login')


@app.route('/register', methods=['GET', 'POST'])
def register():
    """ Get registration form or handle registration and redirect to /users on success. """
    if session.get('username'):
        return redirect(f'/users/{session["username"]}')
    form = RegisterForm()
    if form.validate_on_submit():
        try:
            user = User.register(form)
            session['username'] = user.username
            return redirect(f'/users/{user.username}')
        except IntegrityError:
            form.username.errors = ['Username taken!']

    return render_template('register.html', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    """ Get login form or handle login and redirect to /users on success. """
    if session.get('username'):
        return redirect(f'/users/{session["username"]}')
    form = LoginForm()
    if form.validate_on_submit():
        try:
            user = User.login(form)
            session['username'] = user.username
            return redirect(f'/users/{user.username}')
        except AuthError as error:
            flash(error.message, 'danger')
            return redirect('/login')

    return render_template('login.html', form=form)


@app.route('/logout')
def logout():
    if session.get('username'):
        session.pop('username')
    return redirect('/login')


@app.route('/users/<username>')
def get_user(username):
    """ Allows only authenticated users. """
    if session.get('username') and session.get('username') == username:
        user = User.query.get(username)
        return render_template('user.html', user=user)
    flash('Request not authorized. Please login.', 'danger')
    return redirect('/')


@app.route('/users/<username>/delete', methods=['POST'])
def delete_user(username):
    """"""
    if session.get('username') and session.get('username') == username:
        user = User.query.get(username)
        db.session.delete(user)
        db.session.commit()
        return redirect('/')
    flash('Request not authorized. Please login.', 'danger')
    return redirect('/')


@app.route('/users/<username>/feedback/add')
def add_feedback_form(username):
    """"""
    if session.get('username') and session.get('username') == username:
        user = User.query.get(username)
        return render_template('user.html', user=user)
    flash('Request not authorized. Please login.', 'danger')
    return redirect('/')


@app.route('/users/<username>/feedback/add', methods=['POST'])
def handle_add_feedback(username):
    """"""
    if session.get('username') and session.get('username') == username:
        user = User.query.get(username)
        return render_template('user.html', user=user)
    flash('Request not authorized. Please login.', 'danger')
    return redirect('/')


@app.route('/feedback/<int:id>/update')
def update_feedback_form(id):
    """"""
    if session.get('username') and session.get('username') == username:
        user = User.query.get(username)
        return render_template('user.html', user=user)
    flash('Request not authorized. Please login.', 'danger')
    return redirect('/')


@app.route('/feedback/<int:id>/update', methods=['POST'])
def handle_update_feedback(id):
    """"""
    if session.get('username') and session.get('username') == username:
        user = User.query.get(username)
        return render_template('user.html', user=user)
    flash('Request not authorized. Please login.', 'danger')
    return redirect('/')


@app.route('/feedback/<int:id>/delete', methods=['POST'])
def delete_feedback(id):
    """"""
    if session.get('username') and session.get('username') == username:
        user = User.query.get(username)
        return render_template('user.html', user=user)
    flash('Request not authorized. Please login.', 'danger')
    return redirect('/')
