import uuid

from app import app, db, mail, login_manager
from flask import request, redirect, url_for, render_template, flash, session
from flask.ext.login import login_required, login_user, logout_user, current_user
from form import LoginForm, SignupForm, PasswordForm
from models import User, Reset


@app.route('/')
@login_required
def home():
    return render_template('home.html')


@login_manager.unauthorized_handler
def unauthorized():
    return redirect(url_for('login'))


@app.before_request
def before_request():
    app.logger.info(session)
    pass


@app.after_request
def after_request(response):
    return response


@login_manager.user_loader
def load_user(user_id=None):
    return User.query.get(user_id)


@login_manager.unauthorized_handler
def unauthorized():
    app.logger.info('unauthorized!')
    return redirect(url_for('login'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    login_form = LoginForm(request.form)
    if request.method == 'POST':
        if login_form.validate_on_submit():
            user, authenticated = User.authenticate(query=db.session.query,
                                                    email=login_form.email.data,
                                                    password=login_form.password.data)
            if authenticated:
                app.logger.info("success login!")
                login_user(user)
                return redirect(url_for('home'))
        else:
            flash('Invalid email or password')
    return render_template('login.html', login_form=login_form, signup_form=SignupForm())


@app.route('/signup', methods=['POST'])
def signup():
    signup_form = SignupForm(request.form)
    if signup_form.validate_on_submit():
        if User.query.filter_by(username=signup_form.username.data).first():
            flash('Username is already exists.')
        elif User.query.filter_by(email=signup_form.email.data).first():
            flash('Email is already exists.')
        else:
            user = User(username=signup_form.username.data, email=signup_form.email.data,
                        is_admin=False, active=False)
            db.session.add(user)
            db.session.commit()
            login_user(user)
            key = uuid.uuid4().get_hex()
            db.session.add(Reset(key=key, user_id=user.id))
            db.session.commit()
            mail.sign_up(username=user.username, email=user.email, key=key)
            return redirect(url_for('thanks'))
    return render_template('login.html', login_form=LoginForm(), signup_form=signup_form)


@app.route('/signup/<key>', methods=['GET'])
def password_reset(key=None):
    reset = Reset.query.get(key)
    if reset:
        user = User.query.get(reset.user_id)
        if user:
            session['key'] = key
            if user.active:
                # TODO password reset
                return redirect(url_for('password'))
            else:
                # TODO password setting
                return redirect(url_for('password'))
    return redirect(url_for('login'))


@app.route('/thanks')
def thanks():
    # TODO
    return 'thank you!'


@app.route('/password', methods=['GET', 'POST'])
def password():
    form = PasswordForm(request.form)
    if 'key' in session:
        if form.validate_on_submit():
            if form.password.data != form.confirm.data:
                flash('Please enter same password.')
            else:
                reset = Reset.query.get(session['key'])
                user = User.query.get(reset.user_id)
                user.password = form.password.data
                user.active = True
                db.session.add(user)
                db.session.delete(reset)
                db.session.commit()
                login_user(user)
                session.pop('key')
                return redirect(url_for('home'))
        return render_template('password.html', form=form)
    return redirect(url_for('login'))


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))
