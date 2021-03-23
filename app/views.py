"""
Flask Documentation:     http://flask.pocoo.org/docs/
Jinja2 Documentation:    http://jinja.pocoo.org/2/documentation/
Werkzeug Documentation:  http://werkzeug.pocoo.org/documentation/
This file creates your application.
"""
import psycopg2
import os
from wtforms.fields.simple import PasswordField
from app import app, db, login_manager, models
from flask import render_template, request, redirect, url_for, flash, session, abort, send_from_directory
from .forms import AddItemForm, UpdateItemForm, SubscriberForm, ComplaintForm, SignupForm, AdminLoginForm
from flask_login import login_user, logout_user, current_user, login_required
from app.forms import LoginForm
from app.models import UserProfile, Subscriber, Complaint, Inventory
from werkzeug.security import check_password_hash,generate_password_hash
from werkzeug.utils import secure_filename
from functools import wraps

###
# Routing for your application.
###
def requires_roles(*roles):
    def wrapper(f):
        @wraps(f)
        def wrapped(*args, **kwargs):
            if current_user.role not in roles:
                # Redirect the user to an unauthorized notice!
                return "You are not authorized to access this page"
            return f(*args, **kwargs)
        return wrapped
    return wrapper


@app.route('/')
def home():
    """Render website's home page."""
    return render_template('home.html')

@app.route('/additem', methods=["GET", "POST"])
def additem():
    form = AddItemForm()

    if request.method=='POST':
        if form.validate_on_submit():
            form.set_item(form.item_name.data)
            form.set_cost_price(form.cost_price.data)
            form.set_selling_price(form.selling_price.data)
            form.set_quantity_instock(form.quantity_instock.data)
            form.set_quantity_sold(form.quantity_sold.data)
            form.set_supplier(form.supplier.data)
            form.set_perishables(form.perishables.data)
            form.set_category(form.category.data)
            photo = form.photo.data
            form.set_photo(photo)
            item_name = form.get_item
            cost_price = form.get_cost_price
            selling_price = form.get_selling_price
            quantity_instock = form.get_quantity_instock
            quantity_sold = form.get_quantity_sold
            supplier = form.get_supplier
            category = form.get_category
            perishables = form.get_perishables


            filename = secure_filename(photo.filename)
            photo.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))


            db=connect_db()
            cur=db.cursor()
            sql="INSERT INTO inventory (item_name,cost_price,selling_price,quantity_instock,quantity_sold,supplier,perishables,category,photo) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)"
            cur.execute(sql,(form.get_item(),form.get_cost_price(),form.get_selling_price(),form.get_quantity_instock(),form.get_quantity_sold(),form.get_supplier(),form.get_perishables(),form.get_category(),filename))
            db.commit()
    
            flash('Item Added', 'success')
            return redirect(url_for('displayinventory'))
            # return render_template('result.html',item=form.get_item(),cost_price=form.get_cost_price(),selling_price=form.get_selling_price(),quantity_instock=form.get_quantity_instock(),quantity_sold=form.get_quantity_sold(),supplier=form.get_supplier(),perishables=form.get_perishables(), photo=form.get_photo())
        else:
            flash_errors(form)    
    return render_template('addItem.html',form=form)

@app.route('/updateitem/<itemid>', methods=["GET", "POST"])
def updateitem(itemid):
    updateitemid = Inventory.query.filter_by(id=itemid).first()

    form = UpdateItemForm()
    form.itemname.data=updateitemid.item_name
    form.costprice.data=updateitemid.cost_price
    form.sellingprice.data=updateitemid.selling_price
    form.quantityinstock.data=updateitemid.quantity_instock
    form.quantitysold.data=updateitemid.quantity_sold
    form.supplier.data=updateitemid.supplier
    form.perishables.data=updateitemid.perishables
    form.category.data=updateitemid.category
    form.photo.data=updateitemid.photo
    if request.method=='POST':
        if form.validate_on_submit():
            form.set_item(form.item_name.data)
            form.set_cost_price(form.cost_price.data)
            form.set_selling_price(form.selling_price.data)
            form.set_quantity_instock(form.quantity_instock.data)
            form.set_quantity_sold(form.quantity_sold.data)
            form.set_supplier(form.supplier.data)
            form.set_perishables(form.perishables.data)
            form.set_category(form.category.data)
            photo = form.photo.data
            form.set_photo(photo)
            item_name = form.get_item
            cost_price = form.get_cost_price
            selling_price = form.get_selling_price
            quantity_instock = form.get_quantity_instock
            quantity_sold = form.get_quantity_sold
            supplier = form.get_supplier
            category = form.get_category
            perishables = form.get_perishables


            filename = secure_filename(photo.filename)
            photo.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))


            db=connect_db()
            cur=db.cursor()
            sql="INSERT INTO inventory (item_name,cost_price,selling_price,quantity_instock,quantity_sold,supplier,perishables,category,photo) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)"
            cur.execute(sql,(form.get_item(),form.get_cost_price(),form.get_selling_price(),form.get_quantity_instock(),form.get_quantity_sold(),form.get_supplier(),form.get_perishables(),form.get_category(),filename))
            db.commit()
    
            flash('Item Added', 'success')
            return redirect(url_for('displayinventory'))
            # return render_template('result.html',item=form.get_item(),cost_price=form.get_cost_price(),selling_price=form.get_selling_price(),quantity_instock=form.get_quantity_instock(),quantity_sold=form.get_quantity_sold(),supplier=form.get_supplier(),perishables=form.get_perishables(), photo=form.get_photo())
        else:
            flash_errors(form)    
    return render_template('updateItem.html',updateitemid=updateitemid,form=form)
    # form=UpdateItemForm()
    # updateitemid = Inventory.query.filter_by(id=itemid).first()

    # if request.method=='POST':
    #     if form.validate_on_submit():

            # form.itemname.data=updateitemid.item_name
            # form.costprice.data=updateitemid.cost_price
            # form.sellingprice.data=updateitemid.selling_price
            # form.quantityinstock.data=updateitemid.quantity_instock
            # form.quantitysold.data=updateitemid.quantity_sold
            # form.supplier.data=updateitemid.supplier
            # form.perishables.data=updateitemid.perishables
            # form.category.data=updateitemid.category
            # form.photo.data=updateitemid.photo

            # updateitemid.item_name=form.itemname.data
            # updateitemid.cost_price=form.costprice.data
            # updateitemid.selling_price= form.sellingprice.data
            # updateitemid.quantity_instock= form.quantityinstock.data
            # updateitemid.quantity_sold= form.quantitysold.data
            # updateitemid.supplier=form.supplier.data
            # updateitemid.perishables= form.perishables.data
            # updateitemid.category=form.category.data
            # updateitemid.photo=form.photo.data
            # db.session.commit()
    #         return redirect(url_for('displayinventory'))
    

    # return render_template('updateItem.html',form=form)
    # form.setitem(form.itemname.data)
    # form.setcostprice(form.costprice.data)
    # form.sellingprice(form.sellingprice.data)
    # form.setquantityinstock(form.quantityinstock.data)
    # form.setquantitysold(form.quantitysold.data)
    # form.setsupplier(form.supplier.data)
    # form.setperishables(form.perishables.data)
    # form.setcategory(form.category.data)
    # photo = form.photo.data
    # form.set_photo(photo)
    # item_name = form.get_item
    # cost_price = form.get_cost_price
    # selling_price = form.get_selling_price
    # quantity_instock = form.get_quantity_instock
    # quantity_sold = form.get_quantity_sold
    # supplier = form.get_supplier
    # category = form.get_category
    # perishables = form.get_perishables


    # filename = secure_filename(photo.filename)
    # photo.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

    # db=connect_db()
    # cur=db.cursor()
    # cur.execute("UPDATE inventory SET item_name=%s,cost_price%s,selling_price%s,quantity_instock%s,quantity_sold%s,supplier%s,perishables%s,category%s,photo%s WHERE id=%s",(form.getitem(),form.getcostprice(),form.getsellingprice(),form.getquantityinstock(),form.getquantitysold(),form.getsupplier(),form.getperishables(),form.getcategory(),form.getphoto()))
    # db.commit()
    # flash('Item Updated', 'success')
    # return render_template('result.html',item=form.getitem(),costprice=form.getcostprice(),sellingprice=form.getsellingprice(),quantityinstock=form.getquantityinstock(),quantitysold=form.getquantitysold(),supplier=form.getsupplier(),perishables=form.getperishables(),category=form.getcategory(),photo=itemform.getphoto()) 

@app.route('/edit_item/<id>',methods=['GET','POST'])
def edit_item(id):
    id = Inventory.query.filter_by(id=id).first()
    form=UpdateItemForm()


    form.itemname.data=id.item_name
    form.costprice.data=id.cost_price
    form.sellingprice.data=id.selling_price
    form.quantityinstock.data=id.quantity_instock
    form.quantitysold.data=id.quantity_sold
    form.supplier.data=id.supplier
    form.perishables.data=id.perishables
    form.category.data=id.category
    form.photo.data=id.photo

    if request.method=="POST":
        if form.validate_on_submit():
    
            id.item_name=form.itemname.data
            id.cost_price=form.costprice.data
            id.selling_price= form.sellingprice.data
            id.quantity_instock= form.quantityinstock.data
            id.quantity_sold= form.quantitysold.data
            id.supplier=form.supplier.data
            id.perishables= form.perishables.data
            id.category=form.category.data
            id.photo=form.photo.data
            db.session.commit()

            flash('Updated','success')
            return redirect(url_for('displayinventory',id=id.id))

    # if request.method=='POST' and form.validate_on_submit():
    #     db=connect_db()
    #     cur=db.cursor()
    #     cur.execute("UPDATE inventory SET item_name=%s,cost_price=%s,selling_price=%s,quantity_instock=%s,quantity_sold=%s,supplier=%s,perishables=%s,category=%s,photo=%s WHERE id=%s",(form.get_item(),form.get_cost_price(),form.get_selling_price(),form.get_quantity_instock(),form.get_quantity_sold(),form.get_supplier(),form.get_perishables(),form.get_category(),form.setphoto()))
    #     db.commit()
    #     flash('Updated','success')
    #     return redirect(url_for('displayinventory'))
    return render_template('updateItem.html',form=form)

@app.route('/view-inventory',)
def displayinventory():
    inventorylst = Inventory.query.all()
    return render_template('view_inventory.html',inventorylst=inventorylst)

@app.route('/displayitem/<itemid>', methods=["POST"])
def displayitem(itemid):
    invent = Inventory.query.filter_by(id=itemid).first()
    return render_template('individual_item.html', invent=invent)

@app.route('/deleteitem/<itemid>', methods=["POST"])
def deleteitem(itemid):
    db=connect_db()
    cur=db.cursor()
    cur.execute("DELETE FROM inventory where id=%s",[itemid])
    db.commit()
    flash('Item Deleted', 'success')
    return redirect(url_for('displayinventory'))



def connect_db():
    return psycopg2.connect(host="localhost",database="oodproject", user="oodproject", password="oodproject")

def get_uploaded_images():
    rootdir = os.getcwd()
    photolist = []

    for subdir, dirs, files in os.walk(rootdir + '/uploads'):
        for file in files:
            photolist += [file]
    photolist.pop(0)
    return photolist

@app.route('/uploads/<filename>')
def get_image(filename):
    rootdir2 = os.getcwd()

    return send_from_directory(os.path.join(rootdir2, app.config['UPLOAD_FOLDER']), filename)

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

# def connect_db():
#      return psycopg2.connect(host="localhost",database="present", user="present", password="present")

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
            sql="INSERT INTO user_profile (first_name,last_name,username,password,email,role) VALUES (%s,%s,%s,%s,%s,%s)"
            cur.execute(sql,(fname,lname,username,generate_password_hash(password,method='pbkdf2:sha256'),email,'customer'))
            db.commit()

            flash("Signup Successful!", 'success')
            return redirect(url_for('login'))
    return render_template('signup.html',form=form)

@app.route('/Mailing List', methods=['GET', 'POST'])
@login_required
@requires_roles('admin')
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
