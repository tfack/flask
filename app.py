from flask import Flask, render_template, request, redirect
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, IntegerField, DateField
from wtforms.validators import DataRequired, Length, EqualTo, Email, InputRequired, NumberRange
from wiki import findBirths
from flask_login import current_user, login_user, login_required, logout_user
from models import db, login, UserModel
from datetime import datetime

# #//passwords={}
# #//passwords['tos@uw.edu']='qwerty'

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your secret key'

app.secret_key="a secret"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db/login.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
login.init_app(app)

def addUser(email, password):
    user=UserModel()
    user.set_password(password)
    user.email = email
    db.session.add(user)
    db.session.commit()

@app.before_first_request
def create_table():
    db.create_all()
    user = UserModel.query.filter_by(email = 'tos@uw.edu').first()
    if user is None:
        addUser('tos@uw.edu', 'qwerty')

class loginForm(FlaskForm):
    email=StringField(label="Enter email", validators=[DataRequired(),Email()])
    password=PasswordField(label="Enter password",validators=[DataRequired(), Length(min=6,max=16)])
    submit=SubmitField(label="Login")

class bdayForm(FlaskForm):
    date = DateField(label='Birth date', format="%Y-%m-%d")
    numresults = IntegerField('Max # returns', validators=[InputRequired(), NumberRange(min=1,max=20,
                                                            message='Must enter number between 1 and 20')])
    submit=SubmitField(label="Search")

@app.route("/home",methods=['GET','POST'])
@login_required
def home():
    form=bdayForm()
    if form.validate_on_submit():
        dte_str = str(form.date.data)
        dte_obj = datetime.strptime(dte_str, "%Y-%m-%d")
        year = dte_obj.strftime("%Y")
        dd = dte_obj.strftime("%d")
        mm = dte_obj.strftime("%m")
        date = f"{mm}/{dd}"
        numresults = request.form["numresults"]
        return render_template("home.html", myData=findBirths(date, year, numresults),form=form)
    else:
        print(f"error: {form.date.data}")
        print(form.errors)
    return render_template("home.html",form=form)

@app.route("/")
def redirectToLogin():
    return redirect("/login")

@app.route("/login",methods=['GET','POST'])
def login():
    form=loginForm()
    if form.validate_on_submit():
        if request.method == "POST":
            email=request.form["email"]
            pw=request.form["password"]
            user = UserModel.query.filter_by(email = email).first()
            if email is not None and user.check_password(pw):
                login_user(user)
                return redirect('/home')
    return render_template("login.html",form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect('/login')

@app.route('/owner')
def owner():
    text = "Hello world from Tos!"
    return render_template("hw2.html",text=text)

@app.route('/datetime')
def dtime():
    now = datetime.now()
    dt_string = now.strftime("%m/%d/%Y %H:%M:%S")
    text = dt_string
    return render_template("hw2.html",text=text)


if __name__ == "__main__":
    app.run(host='0.0.0.0',debug=True)