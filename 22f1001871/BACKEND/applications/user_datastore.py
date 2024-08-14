from flask_security import Security, SQLAlchemySessionUserDatastore, hash_password
from applications.models import USER,ROLE
from applications.database import db

user_datastore = SQLAlchemySessionUserDatastore(db.session, USER, ROLE)