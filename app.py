import os
from flask import Flask, render_template, send_from_directory, flash, url_for
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField
from wtforms.validators import DataRequired, Length, NumberRange, Email, Optional
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime



# create and configure the app
app = Flask(__name__)

# secret key
app.config['SECRET_KEY'] = os.getenv("secretkey")
# add the database
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///registrants.db'
# initialize the database
# the sqlite db is actually created by going into the python REPL and importing this file and creating it using the Registrants class
db = SQLAlchemy(app)

# create db model
class Registrants(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    address = db.Column(db.String(100), nullable=True)
    state = db.Column(db.String(25), nullable=True)
    city = db.Column(db.String(50), nullable=True)
    zip = db.Column(db.Integer, nullable=True)
    phone_number = db.Column(db.String(15), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    num_tickets = db.Column(db.Integer, nullable=False)
    date_added = db.Column(db.DateTime, default=datetime.utcnow)

    # define string to print when printing the object
    def __repr__(self):
        return '<Name %r>' % self.name

#create a Form Class
class FirstName(FlaskForm):
    name = StringField("First Name*", validators=[DataRequired()])
    submit = SubmitField('Submit')

#create a register form
class RegisterForm(FlaskForm):
    first_name = StringField("First Name *", validators=[DataRequired(message="Enter Your First Name")])
    last_name = StringField("Last Name *", validators=[DataRequired(message="Enter Your Last Name")])
    email = StringField("Email *", validators=[Email(message="Invalid Email!", check_deliverability=True)])
    address = StringField("Address")
    state = StringField("State")
    city = StringField("City")
    zip = IntegerField("Zip Code", validators=[Optional()])  
    phone_number = StringField("Phone Number *", validators=[Length(min=7, max=16, message="Invalid Phone Number!")])
    num_tickets = IntegerField("How Many Tickets Would You Like To Reserve? *", validators=[NumberRange(min=1, max=20, message="Invalid Ticket Amount!")])
    submit = SubmitField('Submit')



# a simple page that says thanks
@app.route('/user/<name>')
def thanks(name):
    return render_template("thanks.html", name=name)

@app.route('/testing', methods=['GET', 'POST'])
def testing():
    title = 'Simple Web Form'
    name = None
    form = FirstName()
    #Validates Form
    if form.validate_on_submit():
        name = form.name.data
        form.name.data = ''

    return render_template('testing.html', 
            title=title,
            name=name,
            form=form)

@app.route('/', methods=['GET', 'POST'])
def index(): 
    title = 'Registration Form'
    form = RegisterForm()
    first_name = None
    phone_number = None

    # Validates Form
    if form.validate_on_submit():
        registrant =  Registrants.query.filter_by(phone_number=form.phone_number.data).first()
        if registrant is None:
            registrant = Registrants(first_name=form.first_name.data, last_name=form.last_name.data, email=form.email.data, address=form.address.data, state=form.state.data, city=form.city.data, zip=form.zip.data, phone_number=form.phone_number.data, num_tickets=form.num_tickets.data)
            db.session.add(registrant)
            db.session.commit()
            flash("Registration Submitted!")
            first_name = form.first_name.data
            form.first_name.data = ''
            form.last_name.data = ''
            form.email.data = ''
            form.address.data = ''
            form.state.data = ''
            form.city.data = ''
            form.zip.data = ''
            form.phone_number.data = ''
            form.num_tickets.data = ''
        else:
            phone_number = registrant


    return render_template('index.html',
            title=title,
            first_name=first_name,
            phone_number=phone_number,
            form=form)


@app.errorhandler(404)
def page_not_found(e):
    return render_template('index.html'), 404 


@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                      'favicon.ico',mimetype='image/vnd.microsoft.icon')

