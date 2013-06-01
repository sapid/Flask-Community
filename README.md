#Flask-Community

This project is designed to provide a web page for communities to advertise their events. Groups of event organizers can announce when their next event will be, and users can sign up to be reminded of these events by email.

## TODO

* Is CSRF working? I need to verify that Flask-WTF is actually taking care of that.
* Is itsdangerous using pickle or json for sessions?
* Style flashed messages properly
* Write a Hero template

##Current requirements
Flask==0.9
Flask-Login==0.1.3
Flask-Mail==0.8.2
Flask-SQLAlchemy==0.16
Flask-WTF==0.8.3
Jinja2==2.7
MarkupSafe==0.18
SQLAlchemy==0.8.1
WTForms==1.0.4
Werkzeug==0.8.3
blinker==1.2
cryptacular==1.4.1
itsdangerous==0.21
pbkdf2==1.3