from . import db
from werkzeug.security import generate_password_hash

class UserProfile(db.Model):
    __tablename__ = 'user_profile'

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(80))
    last_name = db.Column(db.String(80))
    username = db.Column(db.String(80), unique=True)
    password = db.Column(db.String(255))
    email=db.Column(db.String(255))
    role = db.Column(db.String(64))

    def __init__(self,first_name,last_name,username,password,email,role):
        self.first_name = first_name
        self.last_name = last_name
        self.username = username
        self.email = email
        self.password = generate_password_hash(password,method='pbkdf2:sha256')
        self.role=role

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
        
class Inventory(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    item_name = db.Column(db.String(1000))
    cost_price = db.Column(db.Numeric(1000,2))
    selling_price = db.Column(db.Numeric(1000,2))
    quantity_instock = db.Column(db.Integer)
    quantity_sold = db.Column(db.Integer)
    supplier = db.Column(db.String(1000))
    perishables = db.Column(db.Integer)
    category = db.Column(db.String(1000))
    photo = db.Column(db.String(1000))

    def __init__(self,item_name,cost_price,selling_price,quantity_instock,quantity_sold,supplier,perishables,category,photo):
        self.item_name = item_name
        self.cost_price = cost_price
        self.selling_price = selling_price
        self.quantity_instock = quantity_instock
        self.quantity_sold = quantity_sold
        self.supplier = supplier
        self.perishables = perishables
        self.category = category
        self.photo = photo


class CustomerOrders(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    pid=db.Column(db.Integer)
    first_name = db.Column(db.String(1000))
    last_name = db.Column(db.String(1000))
    email = db.Column(db.String(1000))
    quantity = db.Column(db.Integer)
    item_name = db.Column(db.String(1000))
    selling_price = db.Column(db.Numeric(1000,2))
    subtotal = db.Column(db.Numeric(1000,2))
    grandsubtotal = db.Column(db.Numeric(1000,2))
    total = db.Column(db.Numeric(1000,2))
    tax = db.Column(db.Numeric(1000,2))



    def __init__(self,pid,first_name,last_name,email,quantity,item_name,cost_price,subtotal,grandsubtotal,total,tax):
        self.pid=pid
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.quantity = quantity
        self.item_name = item_name
        self.cost_price = cost_price
        self.subtotal=subtotal
        self.grandsubtotal=grandsubtotal
        self.total=total
        self.tax=tax

