"""
Flask Documentation:     http://flask.pocoo.org/docs/
Jinja2 Documentation:    http://jinja.pocoo.org/2/documentation/
Werkzeug Documentation:  http://werkzeug.pocoo.org/documentation/
This file creates your application.
"""
import psycopg2
from wtforms.fields.simple import PasswordField
from app import app, db, login_manager
from flask import render_template, request, redirect, url_for, flash
from .forms import SubscriberForm, ComplaintForm,SignupForm
from flask_login import login_user, logout_user, current_user, login_required
from app.forms import LoginForm
from app.models import UserProfile, Subscriber, Complaint
from werkzeug.security import check_password_hash,generate_password_hash

###
# Routing for your application.
###



@app.route('/')
def home():
    """Render website's home page."""
    return render_template('home.html')


@app.route('/about/')
@login_required
def about():
    """Render the website's about page."""
    return render_template('about.html', name="Mary Jane")


@app.route('/complaint', methods=["GET", "POST"])
@login_required
def complaint():
    form=ComplaintForm()
    if request.method=='POST':
        if form.validate_on_submit():
            form.set_fname(form.fname.data)
            form.set_lname(form.lname.data)
            form.set_email(form.email.data)
            form.set_subject(form.subject.data)
            form.set_message(form.message.data)

            db=connect_db()
            cur=db.cursor()
            sql="INSERT INTO complaint (first_name,last_name,email,subject,message) VALUES (%s,%s,%s,%s,%s)"
            cur.execute(sql,(form.get_fname(),form.get_lname(),form.get_email(),form.get_subject(),form.get_message()))
            db.commit()
    
            return render_template('result.html',fname=form.get_fname(),lname=form.get_lname(),email=form.get_email(),subject=form.get_subject(),message=form.get_message())
    return render_template('complaint.html',form=form)

def connect_db():
     return psycopg2.connect(host="localhost",database="oodproject", user="oodproject", password="ood")

@app.route('/signup', methods=['GET', 'POST'])
def Signup():
    form=SignupForm()
    if request.method=='POST':
        if form.validate_on_submit():
            form.set_first(form.firstname.data)
            form.set_last(form.lastname.data)
            form.set_username(form.username.data)
            form.set_email(form.email.data)
            form.set_password(form.password.data)
            password=form.get_password()
            fname=form.get_first()
            lname=form.get_last()
            username=form.get_username()
            email=form.get_email()

            db=connect_db()
            cur=db.cursor()
            sql="INSERT INTO user_profile (first_name,last_name,username,password,email) VALUES (%s,%s,%s,%s,%s)"
            cur.execute(sql,(fname,lname,username,generate_password_hash(password,method='pbkdf2:sha256'),email))
            db.commit()

            flash("Signup Successful!", 'success')
            return redirect(url_for('login'))
    return render_template('signup.html',form=form)

@app.route('/Mailing List', methods=['GET', 'POST'])
@login_required
def Mailing():
    """Render the website's contact page."""
    subscriberform = SubscriberForm()

    if request.method == "POST":
        if subscriberform.validate_on_submit():
            
            subscriberform.set_first(subscriberform.firstname.data)
            subscriberform.set_last(subscriberform.lastname.data)
            subscriberform.set_email(subscriberform.email.data) 
            
            db=connect_db()
            cur=db.cursor()
            sql="INSERT INTO subscriber (first_name,last_name,email) VALUES (%s,%s,%s)"
            cur.execute(sql,(subscriberform.get_first(),subscriberform.get_last(),subscriberform.get_email()))
            db.commit()
            flash("Message successfully sent!", 'success')
            return redirect(url_for('home'))
        else:
            flash_errors(subscriberform)
    return render_template('Subscriber.html', form=subscriberform)

@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    if request.method == "POST" and form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        user = UserProfile.query.filter_by(username=username).first()
        if user is not None and check_password_hash(user.password,password):
            remember_me = False
            if 'remember_me' in request.form:
                remember_me = True
            login_user(user, remember=remember_me)
            flash('Login successful!', 'success')
            return redirect(url_for("home"))
        else:
            flash('Username or password is incorrect.', 'danger')   
    flash_errors(form)
    return render_template("login.html", form=form)

###
# The functions below should be applicable to all Flask apps.
###
@app.route("/logout")
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'danger')
    return redirect(url_for('home'))

@login_manager.user_loader
def load_user(id):
    return UserProfile.query.get(int(id))
# Flash errors from the form if validation fails
def flash_errors(form):
    for field, errors in form.errors.items():
        for error in errors:
            flash(u"Error in the %s field - %s" % (
                getattr(form, field).label.text,
                error
            ), 'danger')

@app.route('/<file_name>.txt')
def send_text_file(self,file_name):
    """Send your static text file."""
    file_dot_text = file_name + '.txt'
    return app.send_static_file(file_dot_text)


@app.after_request
def add_header(response):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also tell the browser not to cache the rendered page. If we wanted
    to we could change max-age to 600 seconds which would be 10 minutes.
    """
    response.headers['X-UA-Compatible'] = 'IE=Edge,chrome=1'
    response.headers['Cache-Control'] = 'public, max-age=0'
    return response


@app.errorhandler(404)
def page_not_found(error):
    """Custom 404 page."""
    return render_template('404.html'), 404


if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port="8080")
