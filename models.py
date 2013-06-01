from sqlalchemy import (
    Column,
    Integer,
    Text,
    String,
    ForeignKey,
    DateTime,
    Boolean,
    Unicode,
    SmallInteger
    )
from sqlalchemy.orm import synonym
from database import Base, db_session
import cryptacular.bcrypt

__author__ = 'Will Crawford <will@metawhimsy.com>'

crypt = cryptacular.bcrypt.BCRYPTPasswordManager()

ROLE_USER = 0
ROLE_ADMIN = 1


def hash_password(password):
    ''' Uses cryptacular's encode function which automatically salts.'''
    return unicode(crypt.encode(password))


class mods(Base):
    """This table holds event moderators and their login information."""
    __tablename__ = 'mods'
    mod = Column(String(32), primary_key=True)
    email = Column(String(128), unique=True)
    desc = Column(Text())
    picture = Column(String(256))
    role = Column(SmallInteger, default=ROLE_USER)
    _password = Column('password', Unicode())

    def __init__(self, mod, email, password, role=ROLE_USER):
        self.mod = mod
        self.email = email
        self.password = password
        self.desc = None
        self.picture = None
        self.role = role

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return unicode(self.mod)

    def _get_password(self):
        return self._password

    def _set_password(self, password):
        self._password = hash_password(password)

    password = property(_get_password, _set_password)
    password = synonym('_password', descriptor=password)

    def set_desc(self, description):
        self.desc = description


    def set_picture(self, url):
        self.picture = url

    @classmethod
    def is_admin(cls, mod):
        return cls.get_by_name(mod).role

    @classmethod
    def check_password(cls, username, passwd):
        user = cls.get_by_name(username)
        if not user:
            return False
        return crypt.check(user.password, passwd)

    @classmethod
    def get_by_name(cls, username):
        return db_session.query(cls).filter(cls.mod == username).first()

    @classmethod
    def get_desc_by_name(cls, username):
        return mods.get_by_name(username).desc

    @classmethod
    def get_picture_by_name(cls, username):
        return mods.get_by_name(username).picture

    def __repr__(self):
        return '<Mod %r, %r, %r, %r>' % (self.mod, self.email, self.picture, self.desc)


class modRights(Base):
    """Defines which moderators can create/edit which events."""
    __tablename__ = 'modrights'
    mod = Column(ForeignKey("mods.mod"), primary_key=True)
    EventGroup = Column(ForeignKey("eventgroup.EventGroup"), primary_key=True)

    @classmethod
    def list_all_groups(cls, user):
        return ['group:%s' % g for g in modRights.query.filter(modRights.mod == user).all()]

    def __init__(self, mod, EventGroup):
        self.mod = mod
        self.EventGroup = EventGroup

    def __repr__(self):
        return '<modRights %r for %r>' % (self.mod, self.EventGroup)


class eventGroups(Base):
    """Defines group for a set of recurring events."""
    __tablename__ = 'eventgroup'
    EventGroup = Column(String(128), primary_key=True)
    EventName = Column(String(128), unique=True)
    desc = Column(Text)
    active = Column(Boolean)

    def __init__(self, EventGroup, EventName, desc):
        self.EventGroup = EventGroup
        self.EventName = EventName
        self.desc = desc

    def __repr__(self):
        return '<eventGroups %r, active = %r>' % (self.EventGroup, self.active)


class events(Base):
    """Defines instances of an event that is part of an eventGroup"""
    __tablename__ = 'events'
    EventGroup = Column(ForeignKey("eventgroup.EventGroup"))
    EventTime = Column(DateTime)
    EventID = Column(Integer, primary_key=True)

    def __init__(self, EventGroup, EventTime, EventID):
        self.EventGroup = EventGroup
        self.EventTime = EventTime
        self.EventID = EventID

    def __repr__(self):
        return '<events %r, %r>' % (self.EventGroup, self.EventTime)


class mailingList(Base):
    """This table holds information regarding who to email regarding which events and how often to do it"""
    __tablename__ = 'mailinglist'
    EventGroup = Column(ForeignKey("eventgroup.EventGroup"), primary_key=True)
    email = Column(String(128), primary_key=True)
    freq = Column(Integer)

    def __init__(self, EventGroup, email, freq):
        self.EventGroup = EventGroup
        self.email = email
        self.freq = freq

    def __repr__(self):
        return '<mailingList %r, %r, freq = %r>' % (self.email, self.EventGroup, self.freq)


class emailTokens(Base):
    """Members of the mailing list can edit their subscription information by having tokens sent to their email; this stores those tokens."""
    __tablename__ = 'emailtokens'
    email = Column(ForeignKey("mailinglist.email"), primary_key=True) # One token per email
    token = Column(String)
    created = Column(DateTime) # For expiry

    def __init__(self, email, token, created):
        self.email = email
        self.token = token
        self.created = created

    def __repr__(self):
        return '<emailTokens %r, %r, %r>' % (self.email, self.token, self.created)


class emailAlias(Base):
    """This table defines email forwarding aliases"""
    __tablename__ = 'emailalias'
    email = Column(String)
    AliasID = Column(Integer, primary_key=True) # Should eventually be a one-to-many instead of association

    def __init__(self, EventGroup, email, AliasID):
        self.email = email
        self.AliasID = AliasID

    def __repr__(self):
        return '<emailAlias %r points to %r>' % (self.AliasID, self.email)