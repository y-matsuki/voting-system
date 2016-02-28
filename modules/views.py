import uuid

from app import app, db, mail, login_manager
from flask import request, redirect, url_for, render_template, flash, session, jsonify
from flask.ext.login import login_required, login_user, logout_user, current_user
from form import LoginForm, SignupForm, PasswordForm, TopicForm, EntryForm
from models import User, Reset, Topic, Entry, Point
from datetime import date
from sqlalchemy import func


@login_manager.unauthorized_handler
def unauthorized():
    return redirect(url_for('login'))


@app.before_request
def before_request():
    # app.logger.info(session)
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


@app.route('/')
@login_required
def home():
    topics = Topic.query.all()
    return render_template('home.html', topics=topics)


@app.route('/topic/new', methods=['GET', 'POST'])
@login_required
def add_topic():
    form = TopicForm(request.form)
    if form.validate_on_submit():
        topic = Topic.query.get(form.id.data)
        if topic:
            flash('Topic id is already exists.')
        else:
            topic = Topic(id=form.id.data, description=form.description.data,
                          title=form.title.data, owner_id=current_user.id,
                          is_public=form.is_public.data)
            db.session.add(topic)
            db.session.commit()
            return redirect(url_for('home'))
    return render_template('topic_new.html', form=form)


@app.route('/topic/<id>')
@login_required
def show_topic(id=None):
    topic = Topic.query.get(id)
    entries = db.session.query(Entry,
                               db.func.count(Point.user_id).label('points')
                               ).outerjoin(Point).group_by(Entry.id).order_by('points DESC')
    return render_template('topic.html', topic=topic, entries=entries)


@app.route('/topic/<id>/entry/new', methods=['GET', 'POST'])
@login_required
def add_entry(id=None):
    topic = Topic.query.get(id)
    form = EntryForm(request.form)
    print(form.title.data)
    print(form.description.data)
    print(form.category.data)
    print(form.show_user.data)
    if form.validate_on_submit():
        entry = Entry(topic_id=topic.id, title=form.title.data,
                      description=form.description.data, category=form.category.data,
                      user_id=current_user.id if form.show_user.data else None)
        db.session.add(entry)
        db.session.commit()
        return redirect(url_for('show_topic', id=topic.id))
    return render_template('entry_new.html', topic=topic, form=form)


@app.route('/topic/<topic_id>/entry/<entry_id>/vote')
@login_required
def vote_entry(topic_id=None, entry_id=None):
    today = date.today()
    point = Point.query.filter_by(entry_id=entry_id, user_id=current_user.id, date=today).first()
    if not point:
        point = Point(entry_id=entry_id, user_id=current_user.id, date=today)
        db.session.add(point)
        db.session.commit()
    return redirect(url_for('show_topic', id=topic_id))


@app.route('/topic/<topic_id>/entry/<entry_id>')
@login_required
def show_entry(topic_id=None, entry_id=None):
    entry = Entry.query.get(entry_id)
    return render_template('entry.html', entry=entry)


@app.route('/topic/<topic_id>/entry/<entry_id>')
@login_required
def add_comment(topic_id=None, entry_id=None):
    entry = Entry.query.get(entry_id)
    return render_template('entry.html', entry=entry)


@app.route('/user')
@login_required
def user():
    return render_template('user.html')
