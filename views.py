__author__ = 'Will Crawford <will@metawhimsy.com>'
from main import app, login_manager
from flask import render_template, request, flash, redirect, url_for, session, g
from flask.ext.login import login_user, logout_user, login_required
from models import mods
from database import db_session
from forms import RegistrationForm, LoginForm


@login_manager.user_loader
def load_user(userid):
    return mods.get_by_name(userid)


@app.route('/')
@app.route('/index')
def index():
    return render_template('base.jinja2')


@app.route('/mods')
def mods_base():
    return "mods_base"


@app.route('/mods/login', methods=['GET', 'POST'])
def mods_login():
    if g.user is not None and g.user.is_authenticated():
        return redirect(url_for('index'))
    form = LoginForm(request.form)
    if request.method == 'POST' and form.validate():
        login_user(mods.get_by_name(form.username.data), remember=form.remember_me.data)
        flash("Logged in successfully.")
        return redirect(request.args.get("next") or url_for('index'))
    return render_template('mods_login.jinja2', form=form)


@app.route('/mods/logout')
def mods_logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/mods/register', methods=['GET', 'POST'])
def mods_register():
    form = RegistrationForm(request.form) # TODO: Find csrf.
    if request.method == 'POST' and form.validate():
        mod = mods(form.username.data, form.email.data,
                   form.password.data)
        db_session.add(mod)
        db_session.commit()
        flash('Thanks for registering')
        return redirect(url_for('mods_login'))
    return render_template('mods_register.jinja2', form=form)


@app.route('/email')
def email_base():
    return "email_base"


@app.route('/event')
def event_base():
    return "event_base"


@app.route('/about')
def about():
    return "about"


@app.route('/contact')
def contact():
    return "contact"


@app.route('/links')
def links():
    return "links"