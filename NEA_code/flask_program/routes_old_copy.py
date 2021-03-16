from flask import render_template, url_for, flash, redirect,request
from flask_program import app,db,bcrypt,bootstrap
from flask_program.forms import RegistrationForm, LoginForm
from flask_program.models import User,Tweets,Companies
from flask_login import login_user, current_user, logout_user, login_required
import bokeh
from bokeh.plotting import figure
from bokeh.io import output_file,show
from bokeh.models import ColumnDataSource,CDSView,IndexFilter
from bokeh.models.tools import HoverTool
from bokeh.embed import components
from bokeh.resources import CDN
import pandas as pd

@app.route('/')
def index():
    return render_template('index1.html')

@app.route('/graph')
def plot():

    selected_comp = request.args.get('selected_comp', None)
    #step 2, get company id of desired company 
    Company_object = Companies.query.filter_by(company_name = selected_comp).first()
    Selected_comp_id = Company_object.id
    #step 3, use the company id to get the relevant tweet records
    List_of_tweets = Tweets.query.filter_by(company_id = Selected_comp_id).all()
    df = pd.read_csv('test2/sent_stock_data3.csv')
    df['date_time']= pd.to_datetime(df['date_time'])
    part = df

    source = ColumnDataSource(data=dict(x=part.date_time,y=part.stock_price,z=part.avg_sentiment))


    plot = figure(title= "Stock price with sentiment graph", x_axis_label='Date', y_axis_label='Stock price',x_axis_type='datetime')
    plot.line(x='x',y='y',source=source, line_color='blue', line_width = 5)
    #sent = "neutral"

    for a in range(len(part.date_time)):
        view = CDSView(source=source, filters=[IndexFilter([a])])
        if source.data['z'][a] > 0.1:
            sent="positive"
            plot.circle(source.data['x'][a],source.data['y'][a], source=source,view=view, fill_color='green', size=50)
        elif source.data['z'][a] < -0.1:
            sent="negative"
            plot.circle(source.data['x'][a],source.data['y'][a], source=source, view=view,fill_color='red', size=50)
        else:
            sent="neutral"
            plot.circle(source.data['x'][a],source.data['y'][a], source=source, view=view,fill_color='blue', size=50)

    hover = HoverTool()
    hover.tooltips=[
        ('Average sentiment', sent),
        ('Exact price', '@y')
    ]
    plot.add_tools(hover)

    script1, div1 = components(plot)
    cdn_js = CDN.js_files #cdn_js[0] only need this link
    cdn_json = cdn_js[0]

    return render_template('graph.html',script1=script1,div1=div1,cdn_json=cdn_json)

@app.route('/company_selector',methods=['GET','POST'])
def comp_selector():
    if request.method =='POST':
        selected_comp = request.form.get('companies')
        return redirect(url_for('plot', selected_comp=selected_comp))
    return render_template('selector.html')

@app.route('/login',methods=['GET','POST'])
def logins():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            return redirect(url_for('comp_selector'))
        else:
            flash('Login Unsuccessful. Please check username and password', 'danger')
    return render_template('logins.html',form=form)

@app.route('/register',methods=['GET','POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash(f'Your account has been created! You are now able to log in','success')
        return redirect(url_for('logins'))
    return render_template('register.html',form = form)

@app.route('/login_page')
def login():
    return render_template('login.html')

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('logins'))

if __name__ == "__main__":
    #db.create_all()
    app.run(debug=True)