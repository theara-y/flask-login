from flask import Flask, render_template, redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from sqlalchemy.exc import IntegrityError
from models import db, connect_db, User, Feedback
from forms import RegisterForm, LoginForm, FeedbackForm
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
            flash(f'Welcome {user.first_name} {user.last_name}!', 'success')
            return redirect(f'/users/{user.username}')
        except AuthError as error:
            flash(error.message, 'danger')
            return redirect('/login')

    return render_template('login.html', form=form)


@app.route('/logout')
def logout():
    """ Logout user. """
    if session.get('username'):
        session.pop('username')
        flash('You have been logged out!', 'success')
    return redirect('/login')


@app.route('/users/<username>')
def get_user(username):
    """ Allow only authenticated users to see their page. """
    session_username = session.get('username')
    if session_username and session_username == username:
        user = User.query.get(username)
        return render_template('user.html', user=user, feedbacks=user.feedbacks)
    flash('Request not authorized. Please login.', 'danger')
    return redirect('/')


@app.route('/users/<username>/delete', methods=['POST'])
def delete_user(username):
    """"""
    if session.get('username') and session.get('username') == username:
        user = User.query.get(username)
        db.session.delete(user)
        db.session.commit()
        session.pop('username')
        flash('You have been logged out!', 'success')
    else:
        flash('Request not authorized. Please login.', 'danger')
    return redirect('/')


@app.route('/users/<username>/feedback/add', methods=['GET', 'POST'])
def add_feedback(username):
    """"""
    session_username = session.get('username')
    if session_username and session_username == username:
        form = FeedbackForm()
        if form.validate_on_submit():
            Feedback.submit(username, form)
            flash('Feedback submitted!', 'success')
            return redirect('/')
        return render_template('feedback.html', form=form, form_action=f'/users/{username}/feedback/add')
    flash('Request not authorized. Please login.', 'danger')
    return redirect('/')


@app.route('/feedback/<int:id>/update', methods=['GET', 'POST'])
def handle_update_feedback(id):
    """"""
    feedback = Feedback.query.get(id)
    if feedback:
        session_username = session.get('username')
        if session_username and session_username == feedback.username:
            form = FeedbackForm(obj=feedback)
            if form.validate_on_submit():
                Feedback.update(feedback, form)
                flash('Feedback updated!', 'success')
                return redirect('/')
            return render_template('feedback.html', form=form, id=id, form_action=f'/feedback/{id}/update')
        flash('Request not authorized. Please login.', 'danger')
    return redirect('/')


@app.route('/feedback/<int:id>/delete', methods=['POST'])
def delete_feedback(id):
    """"""
    feedback = Feedback.query.get(id)
    if feedback:
        session_username = session.get('username')
        if session_username and session_username == feedback.username:
            Feedback.delete(id)
            flash('Feedback deleted.', 'success')
            return redirect('/')
        flash('Request not authorized. Please login.', 'danger')
    return redirect('/')
