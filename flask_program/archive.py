from flask import Flask, render_template,request,redirect,flash,url_for,session
from flask_sqlalchemy import SQLAlchemy
#import forms
#fromfrom forms import RegistrationForm, LoginForm
from flask_bootstrap import Bootstrap


app = Flask(__name__)#refers to this file
app.config['SECRET_KEY'] = 'asdf1234'
bootstrap = Bootstrap(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

class User(db.Model):
    _id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20),unique=True,nullable=False)
    email = db.Column(db.String(120),unique=True,nullable=False)
    password = db.Column(db.String(100),unique=True,nullable=False)

    def __repr__(self):
        return f"User('{self.email}','{self.username}')"

@app.route('/')
def index():
    return render_template('index1.html')

@app.route('/login',methods=['GET','POST'])
def logins():
    form = LoginForm()
    if form.validate_on_submit():
        if form.username.data == 'asree' and form.password.data == 'password':
            flash('You have been logged in!', 'success')
            return redirect(url_for('index'))
        else:
            flash('Login Unsuccessful. Please check username and password', 'danger')
    return render_template('logins.html',form=form)

@app.route('/register',methods=['GET','POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        flash(f'Account created for {form.username.data}','success')
        return redirect(url_for('index'))
    return render_template('register.html',form = form)

@app.route('/login_page')
def login():
    #usern = request.form['new_username']
    #passw = request.form['new_Password']
    return render_template('login.html')

#routing, below is how to define route with base url
@app.route("/home/<string:name>")#name needs to e same in func
def hello(name):
    return "Hello," + name

@app.route('/onlyget', methods=['GET'])#specifies http requests you only want
#get only gets data and post only posts and you can't get
def get_only():
    return "You can only get this webpage 2"

if __name__ == "__main__":
    db.create_all()
    app.run(debug=True)