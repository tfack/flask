from flask import Flask, render_template, request, redirect
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, IntegerField, DateField
from wtforms.validators import DataRequired, Length, EqualTo, Email, InputRequired, NumberRange
from wiki import find_titles
from flask_login import current_user, login_user, login_required, logout_user
from models import db, login, UserModel
from datetime import datetime
# from dateutil import parser

# #//passwords={}
# #//passwords['tos@uw.edu']='qwerty'

# now = datetime.now()
# parser(now)

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your secret key'

events = [
    {
        'title' : 'Tutorial',
        'start' : '2022-05-18',
        'end': '',
        'url': ''
    },
    {
        'title' : 'Tutorial',
        'start' : '2022-05-19',
        'end': '',
        'url': ''
    },
    ] 
    
app.secret_key="a secret"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db/login.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
login.init_app(app)

def addUser(email, password):
    print(f"adding user: {email}, password: {password}")
    user=UserModel()
    user.set_password(password)
    user.email = email
    db.session.add(user)
    db.session.commit()
    print(f"user {user} added")
    return user

@app.before_first_request
def create_table():
    db.create_all()
    user = UserModel.query.filter_by(email = 'tos@uw.edu').first()
    if user is None:
        addUser('tos@uw.edu', 'qwerty')

class loginForm(FlaskForm):
    email=StringField(label="Email address",validators=[DataRequired(),Email()])
    password=PasswordField(label="Enter password",validators=[DataRequired(), Length(min=6,max=16)])
    submit=SubmitField(label="Login")

class signupForm(FlaskForm):
    email=StringField(label="Email address",validators=[DataRequired(),Email()])
    password=PasswordField(label="Enter password",validators=[DataRequired(), Length(min=6,max=16)])
    submit=SubmitField(label="Register")

class bdayForm(FlaskForm):
    date = DateField(label='Birth date', format="%Y-%m-%d")
    # date = DateField(label='Birth date')
    numresults = IntegerField('Max # returns', validators=[InputRequired(), NumberRange(min=1,max=20,
                                                            message='Must enter number between 1 and 20')])
    submit=SubmitField(label="Search")

class searchForm(FlaskForm):
    search_text=StringField(validators=[DataRequired()])
    submit=SubmitField(label="Search")

# @app.route("/home",methods=['GET','POST'])
# @login_required
# def home():
#     form=searchForm()
#     if form.validate_on_submit():
#         srch = str(form.text.data)
#         return render_template("home.html", myData=srchIMDB(srch),form=form)
#     return render_template("home.html",form=form)

@app.route("/search",methods=['GET','POST'])
@login_required
def search():
    form = searchForm()
    if form.validate_on_submit():
        if request.method == "POST":
            title = request.form["search_text"]
            return render_template("search.html", myData=find_titles(title),form=form)
        else:
            return render_template("search.html", form=form)
    else:
        print(form.errors)
    return render_template("search.html",form=form)

@app.route("/home",methods=['GET','POST'])
# @login_required
def home():
    # form=bdayForm()
    # if form.validate_on_submit():
    #     dte_str = str(form.date.data)
    #     dte_obj = datetime.strptime(dte_str, "%Y-%m-%d")
    #     year = dte_obj.strftime("%Y")
    #     dd = dte_obj.strftime("%d")
    #     mm = dte_obj.strftime("%m")
    #     date = f"{mm}/{dd}"
    #     numresults = request.form["numresults"]
    #     return render_template("home.html", myData=findBirths(date, year, numresults),form=form)
    # else:
    #     print(f"error: {form.date.data}")
    #     print(form.errors)
    # return render_template("home.html",form=form)
    return render_template("index.html")

@app.route("/")
def redirectToLogin():
    return redirect("/home")

@app.route("/signin",methods=['GET','POST'])
def signin():
    form=loginForm()
    if form.validate_on_submit():
        if request.method == "POST":
            email=request.form["email"]
            pw=request.form["password"]
            user = UserModel.query.filter_by(email = email).first()
            if email is not None and user.check_password(pw):
                login_user(user)
                print(f"logging in user: {user}")
                return redirect('/search')
    return render_template("signin.html",form=form)

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

@app.route('/test')
def test():
    return render_template("test.html")

@app.route('/base')
def base():
    return render_template("base.html")

@app.route('/test2')
def test2():
    return render_template("test2.html")

@app.route('/index.html')
def index():
    return render_template("index.html")

@app.route('/signup.html',methods=['GET','POST'])
def signup():
    form=signupForm()
    # if form.validate_on_submit():
    if request.method == "POST":
        email=request.form["email"]
        pw=request.form["password"]
        user = UserModel.query.filter_by(email = email).first()
        print(f"user: {user}")
        if user is None:
            newuser = addUser(email, pw)
            print(f"adding user: {newuser}")
            login_user(newuser)
            print(f"logged in user: {newuser}")
            return redirect('/search')
        else:
            print(f"else user is not none: {user}")
            return redirect('/signin')
    else:
        print("GET request")
    return render_template("signup.html",form=form)

# @app.route('/signin.html')
# def signin():
#     return render_template("signin.html")

@app.route('/calendar')
def calendar():
    if request.method == 'POST':
        title = request.form['title']
        start = request.form['start']
        end = request.form['end']
        url = request.form['url']
        if end == '':
            end=start
        events.append({
            'title' : title,
            'start' : start,
            'end': end,
            'url': url
        },
        )
    return render_template("calendar.html", events=events)

@app.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        title = request.form['title']
        start = request.form['start']
        end = request.form['end']
        url = request.form['url']
        if end == '':
            end=start
        events.append({
            'title' : title,
            'start' : start,
            'end': end,
            'url': url
        },
        )
    return render_template("calendar.html", events=events)

if __name__ == "__main__":
    app.run(host='0.0.0.0',debug=True)
