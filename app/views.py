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
from flask import render_template, request, redirect, url_for, flash, session, abort, send_from_directory,make_response
from .forms import AddItemForm, UpdateItemForm, SubscriberForm, ComplaintForm, SignupForm, AdminLoginForm, SearchForm
from flask_login import login_user, logout_user, current_user, login_required
from app.forms import LoginForm
from app.models import UserProfile, Subscriber, Complaint, Inventory,CustomerOrders
from werkzeug.security import check_password_hash,generate_password_hash
from werkzeug.utils import secure_filename
from functools import wraps
import pdfkit
from flask import Markup
import datetime

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

@requires_roles('admin')
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

@app.route('/edit_item/<id>', methods=['GET','POST'])
@requires_roles('admin')
def edit_item(id):
    newid=id
    id = Inventory.query.filter_by(id=id).first()
    form=UpdateItemForm()

    if request.method=="GET":
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

        form.setitem(form.itemname.data)
        form.setcostprice(form.costprice.data)
        form.setsellingprice(form.sellingprice.data)
        form.setquantityinstock(form.quantityinstock.data)
        form.setquantitysold(form.quantitysold.data)
        form.setsupplier(form.supplier.data)
        form.setperishables(form.perishables.data)
        form.setcategory(form.category.data)
        photo = form.photo.data
        form.setphoto(photo)
        filename = secure_filename(photo.filename)
        photo.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

        db=connect_db()
        cur=db.cursor()
        sql="UPDATE inventory SET item_name=%s,cost_price=%s,selling_price=%s,quantity_instock=%s,quantity_sold=%s,supplier=%s,perishables=%s,category=%s,photo=%s WHERE id=%s"
        cur.execute(sql,(form.getitem(),form.getcostprice(),form.getsellingprice(),form.getquantityinstock(),form.getquantitysold(),form.getsupplier(),form.getperishables(),form.getcategory(),filename,newid))
        db.commit()

        flash('Updated','success')
        return redirect(url_for('displayinventory'))
    return render_template('updateItem.html',form=form, id=id)

def MagerDicts(dict1,dict2):
    if isinstance(dict1,list) and isinstance(dict2,list):
        return dict1+dict2
    elif isinstance(dict1,dict) and isinstance(dict2,dict):
        return dict(list(dict1.items())+list(dict2.items()))
    return False

@app.route('/addtocart', methods=['POST', 'GET'])
@requires_roles('customer')
@login_required
def addtocart():
    try:
        product_id=request.form.get('product_id')
        quantity=request.form.get('quantity')
        product=Inventory.query.filter_by(id=product_id).first()
        if product_id and quantity and request.method=='POST':
            DictItems={product_id:{'name': product.item_name,'price':float(product.selling_price),'quantity': quantity,'stock':product.quantity_instock ,'image':product.photo}}
            if 'Shoppingcart' in session:
                print(session['Shoppingcart'])
                if product_id in session['Shoppingcart']:
                    for key,item in session['Shoppingcart'].items():
                        if int(key)==int(product_id):
                            session.modified=True
                            item['quantity'] += 1
                        # Check over part 28 still not working
                else:
                    session['Shoppingcart']=MagerDicts(session['Shoppingcart'],DictItems)
                    return redirect("menu")
            else:
                session['Shoppingcart']=DictItems
                return product_id
    except Exception as e:
        print(e)
    finally:
    # pass
        return redirect("menu")


@app.route("/addtodb", methods=['POST', 'GET'])
@requires_roles('customer')
@login_required
def addtodb():
    if request.method=='POST':
        subtotal1=0
        lst2,lst3,lst4=[],[],[]
        datenow=datetime.datetime.now()

        for key,items in session['Shoppingcart'].items():
            subtotal1+=float(items['price'])*int(items['quantity'])
            tax=round((0.15 * float(subtotal1)),2)
            grandtotal=round(float(subtotal1)+float(tax),2)
            grandsubtotal=subtotal1
            lst2.append(tax)
            lst3.append(grandtotal)
            lst4.append(grandsubtotal)

            db=connect_db()
            cur=db.cursor()
            cur.execute('SELECT MAX(order_id) FROM customer_orders')        
            maxid = cur.fetchone()
            maxidd=0
            if maxid[0]==None:
                maxidd=1
            else:
                maxidd=maxid[0]+1

        # for key,items in session['Shoppingcart'].items():
        #     itemname=items['name']
        #     sellingprice=items['price']
        #     quantity=items['quantity']
        #     # subtotal=float(quantity)*float(sellingprice)
        #     # tax=round((0.15 * float(subtotal)),2)
        #     subtotal1+=float(items['price'])*int(items['quantity'])

        #     db=connect_db()
        #     cur=db.cursor()
        #     sql="INSERT INTO customer_orders (pid,first_name,last_name,email,quantity,item_name,selling_price,subtotal,grandsubtotal,total,tax,ord_date,order_id) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        #     cur.execute(sql,(current_user.id,current_user.first_name,current_user.last_name,current_user.email,quantity,itemname,sellingprice,subtotal,lst4[-1],lst3[-1],lst2[-1],datenow,maxidd))
        #     db.commit()

            #SUBTRACTION
            # db=connect_db()
            # cur=db.cursor()
            # sql="UPDATE Inventory SET quantity_instock=quantity_instock-%s WHERE item_name=%s"
            # cur.execute(sql,(quantity,itemname))
            # db.commit()
        flash(Markup('Successfully registered, please click <a href="{{url_for("get_pdf(Reciept)")}}" target="#" class="alert-link">here</a>'))

        flash('Order Submitted','success')
        return redirect(url_for('menu'))
    return redirect(url_for('menu'))

@app.route("/get_pdf/<invoice>", methods=['POST','GET'])
@requires_roles('customer')
@login_required
def get_pdf(invoice):
    filepath='/uploads'
    if request.method=='POST':
        for key,items in session['Shoppingcart'].items():
            itemname=items['name']
            sellingprice=items['price']
            quantity=items['quantity']
        rendered= render_template('pdf.html',invoice=invoice,itemname=itemname,sellingprice=sellingprice,quantity=quantity)
        pdf=pdfkit.from_string(rendered,False)
        response=make_response(pdf)
        response.headers['content-Type']='application/pdf'
        response.headers['content-Dispostion']='inline; filename=invoice.pdf' 
        return response
    return render_template('pdf.html')


@app.route("/carts")
@requires_roles('customer')
@login_required
def getCart():
    if 'Shoppingcart' not in session:
        return redirect("menu")
    subtotal=0
    grandsubtotal=0
    grandtotal=0
    tax=0
    for key,product in session['Shoppingcart'].items():
        subtotal+=float(product['price'])*int(product['quantity'])
        tax=round((0.15 * float(subtotal)),2)
        grandtotal=round(float(subtotal)+float(tax),2)
        grandsubtotal=subtotal
    return render_template('checkout.html',grandsubtotal=grandsubtotal,tax=tax,grandtotal=grandtotal)

@app.route("/updatecart/<code>", methods=["POST"])
@requires_roles('customer')
@login_required
def updatecart(code):
    if 'Shoppingcart' not in session and len(session['Shoppingcart'])<=0:
        return redirect('menu')
    if request.method=='POST':
        quantity=request.form.get('quantity')  
        session.modifed=True
        for key,item in session['Shoppingcart'].items():
            if key==code:
                item['quantity']=quantity
                flash('Item Updated','success')
                return redirect(url_for('getCart'))
        return redirect(url_for('getCart'))


@app.route("/deleteitemcart/<code>")
@requires_roles('customer')
@login_required
def deleteitemcart(code):
    if 'Shoppingcart' not in session and len(session['Shoppingcart'])<=0:
        return redirect('menu')
    session.modifed=True
    for key,item in session['Shoppingcart'].items():
        if key==code:
            session['Shoppingcart'].pop(key,None)
            flash('Item Removed','success')
            return redirect(url_for('getCart'))
    return redirect(url_for('getCart'))


@app.route("/clearcart")
@requires_roles('customer')
@login_required
def clearcart():
    session.pop('Shoppingcart',None)
    return redirect(url_for('getCart'))    


@app.route('/view-inventory')
@requires_roles('admin')
@login_required
def displayinventory():
    inventorylst = Inventory.query.order_by('id').all()
    return render_template('view_inventory.html',inventorylst=inventorylst)

@app.route('/view-complaints')
@requires_roles('admin')
@login_required
def displaycomplaints():
    complaint = Complaint.query.order_by('id').all()
    return render_template('viewcomplaints.html',complaint=complaint)

@app.route('/deletecomplaint/<id>', methods=["GET"])
@requires_roles('admin')
@login_required
def deletecom(id):
    db=connect_db()
    cur=db.cursor()
    cur.execute("DELETE FROM complaint where id=%s",[id])
    db.commit()
    flash('Complaint Deleted', 'success')
    return redirect(url_for('displaycomplaints'))

@app.route('/view-subscribers')
@requires_roles('admin')
@login_required
def displaysubscribers():
    subscribers = Subscriber.query.order_by('id').all()
    return render_template('viewsubscribers.html',subscribers=subscribers)

@app.route('/deletesubscriber/<id>', methods=["GET"])
@requires_roles('admin')
@login_required
def deletesub(id):
    db=connect_db()
    cur=db.cursor()
    cur.execute("DELETE FROM Subscriber where id=%s",[id])
    db.commit()
    flash('Subscriber Deleted', 'success')
    return redirect(url_for('displaysubscribers'))


@app.route('/displayitem/<itemid>')
@requires_roles('admin')
@login_required
def displayitem(itemid):
    invent = Inventory.query.filter_by(id=itemid).first()
    return render_template('individual_item.html', invent=invent)

@app.route('/menu', methods=['POST','GET'])
@requires_roles('customer')
@login_required
def menu():
    form = SearchForm()

    if request.method == 'POST' and form.validate_on_submit():
        search = form.search.data
        filterfield = form.filterfield.data

        if filterfield == 'None':
            db=connect_db()
            cur=db.cursor()
            cur.execute('SELECT * FROM Inventory WHERE item_name like %s', ('%' + search + '%',))        
            invent = cur.fetchall()
            return render_template('menu.html', invent=invent, form=form)

        if filterfield != 'None' and search != '':
            db=connect_db()
            cur=db.cursor()
            cur.execute('SELECT * FROM Inventory WHERE item_name like %s and category = %s', ('%' + search + '%', filterfield,))        
            invent = cur.fetchall()
            return render_template('menu.html', invent=invent, form=form)

        else:    
            db=connect_db()
            cur=db.cursor()
            cur.execute('SELECT * FROM Inventory WHERE category = %s', (filterfield,))        
            invent = cur.fetchall()
            return render_template('menu.html', invent=invent, form=form)
    else:
        db=connect_db()
        cur=db.cursor()
        cur.execute('SELECT * FROM Inventory')        
        invent = cur.fetchall()
        return render_template('menu.html',invent=invent, form=form)

@app.route('/deleteitem/<itemid>', methods=["GET"])
@requires_roles('admin')
@login_required
def deleteitem(itemid):
    db=connect_db()
    cur=db.cursor()
    cur.execute("DELETE FROM inventory where id=%s",[itemid])
    db.commit()
    flash('Item Deleted', 'success')
    return redirect(url_for('displayinventory'))

@app.route('/checkout')
@requires_roles('customer')
@login_required
def checkout():
    return render_template('checkout.html')

@app.route('/report')
@requires_roles('admin')
@login_required
def report():
    db=connect_db()
    cur=db.cursor()
    cur.execute('SELECT item_name,quantity_sold/quantity_instock::float*100 FROM inventory')
    values = cur.fetchall()
    inventory = Inventory.query.order_by('id').all()
    return render_template('report.html',inventory=inventory,values=values)
    
@app.route('/manage')
@requires_roles('admin')
@login_required
def manage():
    db=connect_db()
    cur=db.cursor()
    sql="SELECT order_id,array_to_string(array_agg(DISTINCT CONCAT(first_name, ' ', last_name)), ', '), array_to_string(array_agg( CONCAT(item_name)), ', '),array_to_string(array_agg( CONCAT(quantity)), ', '),array_to_string(array_agg( CONCAT(selling_price)), ', '),array_to_string(array_agg( DISTINCT CONCAT(grandsubtotal)), ', '), array_to_string(array_agg( DISTINCT CONCAT(tax)), ', '),array_to_string(array_agg( DISTINCT CONCAT(total)), ', ') as persondata FROM customer_orders GROUP BY order_id;"
    cur.execute(sql)
    orders=cur.fetchall()
    return render_template('manageord.html',orders=orders)
    

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
@requires_roles('customer')
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

            flash("Complaint Sent!", "success")    
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
@requires_roles('customer')
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
            flash("You've been successfully added!", 'success')
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
    session.clear()
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
