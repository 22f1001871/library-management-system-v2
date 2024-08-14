from applications.database import db
from flask_security import UserMixin,RoleMixin


#model for roles and users
class ROLEUSER(db.Model):
    __tablename__='ROLEUSER'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column('USER_id', db.Integer, db.ForeignKey('USER.id'))
    role_id = db.Column('ROLE_id', db.Integer, db.ForeignKey('ROLE.id'))

#model for roles
class ROLE(db.Model,RoleMixin):
    __tablename__ = 'ROLE'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True)
    description = db.Column(db.String)

#model for users
class USER(db.Model,UserMixin):
    __tablename__ = 'USER'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String, unique=True)
    username = db.Column(db.String, unique=True, nullable=True)
    password = db.Column(db.String, nullable=False)
    last_login_at = db.Column(db.DateTime)
    current_login_at = db.Column(db.DateTime)
    last_login_ip = db.Column(db.String)
    current_login_ip = db.Column(db.String)
    login_count = db.Column(db.Integer,default=0)
    active = db.Column(db.Boolean)
    fs_uniquifier = db.Column(db.String, unique=True, nullable=False)
    confirmed_at = db.Column(db.DateTime)
    roles = db.relationship('ROLE', secondary='ROLEUSER',backref=db.backref('users', lazy='dynamic'))

#model for sections
class SECTIONS(db.Model):
    __tablename__="SECTIONS"
    id=db.Column(db.Integer,primary_key=True,autoincrement=True)
    name=db.Column(db.String,nullable=False,unique=True)
    date=db.Column(db.DateTime)
    description=db.Column(db.String)
    rawsection=db.Column(db.String)

#model for book
class BOOKS(db.Model):
    __tablename__="BOOKS"
    id=db.Column(db.Integer,primary_key=True,autoincrement=True)
    section_id=db.Column(db.Integer,db.ForeignKey('SECTIONS.id'))
    name=db.Column(db.String,nullable=False,unique=True)
    content=db.Column(db.String)
    author=db.Column(db.String)
    rating=db.Column(db.Integer,default=0)
    price=db.Column(db.Integer)
    user_id=db.Column(db.Integer,db.ForeignKey('USER.id'),default=0)
    issued_date=db.Column(db.DateTime)
    return_date=db.Column(db.DateTime)
    rawname=db.Column(db.String)
    rawauth=db.Column(db.String)

#model for requestes
class REQUESTS(db.Model):
    __tablename__="REQUESTS"
    id=db.Column(db.Integer,primary_key=True,autoincrement=True)
    h_id=db.Column(db.Integer)
    user_id=db.Column(db.Integer,db.ForeignKey('USER.id'))
    book_id=db.Column(db.Integer,db.ForeignKey('BOOKS.id'))
    day_requested=db.Column(db.DateTime)
    no_of_days=db.Column(db.Integer)

#model for books requested history
class HISTORY(db.Model):
    __tablename__="HISTORY"
    id=db.Column(db.Integer,primary_key=True,autoincrement=True)
    user_id=db.Column(db.Integer,db.ForeignKey('USER.id'))
    book_id=db.Column(db.Integer,db.ForeignKey('BOOKS.id'))
    access=db.Column(db.Boolean)
    description=db.Column(db.String)
    date_requested=db.Column(db.DateTime)
    date_accessed=db.Column(db.DateTime)
    date_returned=db.Column(db.DateTime)
    
class RATING(db.Model):
    __tablename__="RATING"
    rid=db.Column(db.Integer,primary_key=True,autoincrement=True)
    uid=db.Column(db.Integer,db.ForeignKey('USER.id'))
    bookid=db.Column(db.Integer,db.ForeignKey('BOOKS.id'))
    rating=db.Column(db.Integer)

#model to show  book
class MYBOOKS(db.Model):
    __tablename__="MYBOOKS"
    mbid=db.Column(db.Integer,primary_key=True,autoincrement=True)
    uid=db.Column(db.Integer,db.ForeignKey('USER.id'))
    bookid=db.Column(db.Integer,db.ForeignKey('BOOKS.id'))
    bname=db.Column(db.String)
    amountpaid=db.Column(db.Integer)