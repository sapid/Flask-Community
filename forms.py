__author__ = 'Will Crawford <will@metawhimsy.com>'
from wtforms import Form, BooleanField, TextField, PasswordField, validators, ValidationError
from models import mods


class RegistrationForm(Form):
    def validate_username(form, field):
        if len(field.data) > 20:
            raise ValidationError(u'Username too long!')
        if mods.get_by_name(field.data) != None:
            raise ValidationError(u'Login is taken.')

    username = TextField(u'Username', [validators.Length(min=4, max=25), validate_username])
    email = TextField(u'Email Address', [validators.Length(min=6, max=35)])
    password = PasswordField(u'New Password', [
        validators.Required(),
        validators.EqualTo(u'confirm', message=u'Passwords must match')
    ])
    confirm = PasswordField(u'Repeat Password')
    accept_tos = BooleanField(u'I accept the TOS', [validators.Required()])


class LoginForm(Form):
    def validate_user(form, field):
        if mods.get_by_name(field.data) == None:
            raise ValidationError(u'User does not exist')

    def validate_combo(form, field):
        if not mods.check_password(form.username.data, form.password.data):
            raise ValidationError(u'Username and password do not match')

    username = TextField(u'Username', [validators.Length(min=4, max=25), validate_user])
    password = PasswordField(u'Password', [validators.Required(), validate_combo])
    remember_me = BooleanField(u'remember_me', default=False)