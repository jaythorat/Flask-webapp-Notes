# Importing Modules
from . import db 
from flask_login import UserMixin
from sqlalchemy.sql import func

# User notes info
class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.String(10000))
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    #Associating foreign key 'user.id' to link notes with their specified user
    user_id = db.Column(db.Integer, db.ForeignKey('user.id')) # In foreign key class name is written in small.


# User details
class User(db.Model,UserMixin):
    id= db.Column(db.Integer, primary_key =True)
    email = db.Column(db.String(150), unique=True)  #150 stands for max limit of that string
    password = db.Column(db.String(150))
    first_name = db.Column(db.String(150))

    def is_active(self):
        return True
    # Setting relationship With Note
    notes = db.relationship('Note') # In relationship class name is typed as it is.
