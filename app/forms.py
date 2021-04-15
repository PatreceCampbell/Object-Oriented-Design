from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextAreaField, DecimalField, IntegerField, FileField, SelectField
from wtforms.validators import DataRequired, Email, InputRequired, Regexp
from flask_wtf.file import FileField, FileRequired, FileAllowed


class SignupForm(FlaskForm):
    firstname = StringField('First Name', validators=[DataRequired()])
    lastname = StringField('Last Name', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    username = StringField('Username', validators=[InputRequired()])
    password = PasswordField('Password', validators=[InputRequired()])

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

    def set_password(self,password):
        self.password=password
        
    def get_password(self):
        return self.password

    def set_username(self,username):
        self.username=username

    def get_username(self):
        return self.username


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[InputRequired()])
    password = PasswordField('Password', validators=[InputRequired()])

    def set_username(self,username):
        self.username=username

    def get_username(self):
        return self.username

    def set_password(self,password):
        self.password=password
        
    def get_password(self):
        return self.password

class AdminLoginForm(FlaskForm):
    username = StringField('Username', validators=[InputRequired()])
    password = PasswordField('Password', validators=[InputRequired()])

    def set_username(self,username):
        self.username=username

    def get_username(self):
        return self.username

    def set_password(self,password):
        self.password=password
        
    def get_password(self):
        return self.password

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

    
class ComplaintForm(FlaskForm):
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

class AddItemForm(FlaskForm):
    item_name = StringField('Item Name', validators=[DataRequired()])
    cost_price = DecimalField('Cost Price', validators=[DataRequired()])
    selling_price = DecimalField('Selling Price', validators=[DataRequired()])
    quantity_instock = IntegerField('Quantity Instock', validators=[DataRequired()])
    quantity_sold = IntegerField('Quantity Sold', validators=[DataRequired()])
    supplier = StringField('Supplier', validators=[DataRequired()])
    perishables = IntegerField('Perishables', validators=[DataRequired()])
    # category = SelectField('Category', validators=[DataRequired()] choices = [('Staple'), ('Juice'), ('Tin'), ('Toiletries'), ('Personal Item'), ('Powered'), ('Cooking Essential'), ('Candy'), ('Alcohol'), ('Diary')] validators=[Optional()])
    category = SelectField('Category', choices=[('Staple'), ('Juice'), ('Tin'),('Snack'), ('Toiletries'), ('Personal Item'), ('Powered'), ('Cooking Essential'), ('Candy'), ('Alcohol'), ('Diary')])
    photo = FileField('Photo', validators=[FileRequired(), FileAllowed(['jpg', 'png', 'Photos only!'])])

    def set_item(self,item_name):
        self.item_name = item_name

    def get_item(self):
        return self.item_name

    def set_cost_price(self,cost_price):
        self.cost_price = cost_price 
        
    def get_cost_price(self):
        return self.cost_price 

    def set_selling_price(self,selling_price):
        self.selling_price = selling_price 
        
    def get_selling_price(self):
        return self.selling_price 

    def set_quantity_instock(self,quantity_instock):
        self.quantity_instock = quantity_instock

    def get_quantity_instock(self):
        return self.quantity_instock

    def set_quantity_sold(self,quantity_sold):
        self.quantity_sold = quantity_sold
        
    def get_quantity_sold(self):
        return self.quantity_sold

    def set_supplier(self,supplier):
        self.supplier = supplier

    def get_supplier(self):
        return self.supplier

    def set_perishables(self,perishables):
        self.perishables = perishables 
        
    def get_perishables(self):
        return self.perishables 

    def set_category(self,category):
        self.category = category 
        
    def get_category(self):
        return self.category 
    
    def set_photo(self,photo):
        self.photo = photo 
        
    def get_photo(self):
        return self.photo 

class UpdateItemForm(FlaskForm):
    itemname = StringField('Item Name', validators=[DataRequired(), Regexp("/^[A-Za-z]+$/", flags=0, message="String Required")])
    costprice = DecimalField('Cost Price', validators=[DataRequired()])
    sellingprice = DecimalField('Selling Price', validators=[DataRequired()])
    quantityinstock = IntegerField('Quantity Instock', validators=[DataRequired()])
    quantitysold = IntegerField('Quantity Sold', validators=[DataRequired()])
    supplier = StringField('Supplier', validators=[DataRequired()])
    perishables = IntegerField('Perishables', validators=[DataRequired()])
    category = StringField('Category', validators=[DataRequired()])
    photo = FileField('Item Image', validators=[DataRequired()])

    def setitem(self,itemname):
        self.itemname = itemname

    def getitem(self):
        return self.itemname

    def setcostprice(self,costprice):
        self.costprice = costprice 
        
    def getcostprice(self):
        return self.costprice 

    def setsellingprice(self,sellingprice):
        self.sellingprice = sellingprice 
        
    def getsellingprice(self):
        return self.sellingprice 

    def setquantityinstock(self,quantityinstock):
        self.quantityinstock = quantityinstock

    def getquantityinstock(self):
        return self.quantityinstock

    def setquantitysold(self,quantitysold):
        self.quantitysold = quantitysold
        
    def getquantitysold(self):
        return self.quantitysold

    def setsupplier(self,supplier):
        self.supplier = supplier

    def getsupplier(self):
        return self.supplier

    def setperishables(self,perishables):
        self.perishables = perishables 
        
    def getperishables(self):
        return self.perishables 

    def setcategory(self,category):
        self.category = category 
        
    def getcategory(self):
        return self.category 
    
    def setphoto(self,photo):
        self.photo = photo 
        
    def getphoto(self):
        return self.photo 

class SearchForm(FlaskForm):
    search = StringField('Search', description="Please enter meal you wish to search for.")

    def setsearch(self,search):
            self.search = search 
        
    def getsearch(self):
        return self.search 

        