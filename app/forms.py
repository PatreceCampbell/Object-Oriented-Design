from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField,TextAreaField
from wtforms.validators import DataRequired, Email,InputRequired

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[InputRequired()])
    password = PasswordField('Password', validators=[InputRequired()])

class SubscriberForm(FlaskForm):
    firstname = StringField('First Name', validators=[DataRequired()])
    lastname = StringField('Last Name', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])

    def set_first(self,firstname):
        self.firstname=firstname

    def get_first(self):
        return self.firstname

    def set_last(self,lastname):
        self.lastname=lastname
        
    def get_last(self):
        return self.lastname

    def set_email(self,email):
        self.email=email

    def get_email(self):
        return self.email

    
class ContactForm(FlaskForm):
    fname=StringField('First Name', validators=[DataRequired()], description='Please enter your first name.')
    lname=StringField('Last Name', validators=[DataRequired()], description='Please enter your last name.')
    email=StringField('E-mail', validators=[DataRequired(), Email()], description='Please enter your email address.')
    subject=StringField('Subject', validators=[DataRequired()], description='Please enter the subject for your complaint.')
    message=TextAreaField('Message', validators=[DataRequired()], description='Please enter the complaint below.')

    def set_fname(self,fname):
        self.fname=fname

    def get_fname(self):
        return self.fname

    def set_lname(self,lname):
        self.lname=lname
        
    def get_lname(self):
        return self.lname

    def set_email(self,email):
        self.email=email

    def get_email(self):
        return self.email

    def set_subject(self,subject):
        self.subject=subject

    def get_subject(self):
        return self.subject

    def set_message(self,message):
        self.message=message
        
    def get_message(self):
        return self.message