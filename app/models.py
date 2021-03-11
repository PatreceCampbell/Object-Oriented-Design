from . import db
from werkzeug.security import generate_password_hash

class UserProfile(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(80))
    last_name = db.Column(db.String(80))
    username = db.Column(db.String(80), unique=True)
    password = db.Column(db.String(255))
    email=db.Column(db.String(255))

    def __init__(self,first_name,last_name,username,password,email):
        self.first_name = first_name
        self.last_name = last_name
        self.username = username
        self.email = email
        self.password = generate_password_hash(password,method='pbkdf2:sha256')

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        try:
            return unicode(self.id)  # python 2 support
        except NameError:
            return str(self.id)  # python 3 support

    def __repr__(self):
        return '<User %r>' % (self.username)

class Subscriber(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(80))
    last_name = db.Column(db.String(80))
    email=db.Column(db.String(255))

    def __init__(self,first_name,last_name,email):
        self.first_name = first_name
        self.last_name = last_name
        self.email = email

    def __repr__(self):
        return f"Subscriber('{self.first_name}','{self.last_name}','{self.email}')" 

class Complaint(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(80))
    last_name = db.Column(db.String(80))
    email=db.Column(db.String(255))
    subject = db.Column(db.String(255))
    message = db.Column(db.String(255))

    def __init__(self,first_name,last_name,email,message,subject):
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.message=message
        self.subject=subject

    def __repr__(self):
        return f"Complaint('{self.first_name}','{self.last_name}','{self.email}','{self.subject}','{self.message}')" 
        