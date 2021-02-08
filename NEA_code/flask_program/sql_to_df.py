from flask import Flask
import pandas as pd 
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
from flask_login import UserMixin
import bokeh
from bokeh.plotting import figure
from bokeh.io import output_file,show
from bokeh.models import ColumnDataSource,CDSView,IndexFilter
from bokeh.models.tools import HoverTool
from bokeh.embed import components
from bokeh.resources import CDN
import datetime
from datetime import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = '5791628bb0b13ce0c676dfde280ba245'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users5.db'  #location of database
db = SQLAlchemy(app) #database object

follows = db.Table('follows',
        db.Column('user_id',db.Integer,db.ForeignKey('user.id')),
        db.Column('company_id',db.Integer,db.ForeignKey('companies.id'))
)


class User(db.Model,UserMixin): #class for the model of the users database
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20),unique=True,nullable=False)
    email = db.Column(db.String(120),unique=True,nullable=False)
    password = db.Column(db.String(100),unique=True,nullable=False)
    company_following = db.relationship("Companies",secondary=follows,lazy=True)


    def __repr__(self):
        return f"User('{self.email}','{self.username}')"

class Companies(db.Model): #class for the model of the users database
    id = db.Column(db.Integer, primary_key=True)
    company_name = db.Column(db.String(20),unique=True,nullable=False)
    search_query = db.Column(db.String(120),nullable=False)
    symbol = db.Column(db.String(100),unique=True,nullable=False)
    comp_tweets = db.relationship('Tweets',backref='tweets_company',lazy=True)


    def __repr__(self):
        return f"User('{self.company_name}','{self.search_query}','{self.symbol}')"


class Tweets(db.Model): #class for the model of the users database
    id = db.Column(db.Integer, primary_key=True)
    date_time = db.Column(db.String(70),nullable=False)
    avg_sentiment = db.Column(db.Float,nullable=False)
    stock_price = db.Column(db.Float,nullable=False)
    most_pos_tweet = db.Column(db.String(500),nullable=False)
    most_neg_tweet = db.Column(db.String(500),nullable=False)
    company_id = db.Column(db.Integer, db.ForeignKey('companies.id'))

    '''def __repr__(self):
        return f"{self.date_time},{self.stock_price},{self.avg_sentiment}"'''



db.create_all()

comp = Tweets.query.filter_by(company_id=1).all()
list_of_dicts = []
for u in comp:
    data2 = u.__dict__
    del data2['_sa_instance_state']
    list_of_dicts.append(data2)

df2 = pd.DataFrame(list_of_dicts)
df2['date_time']= pd.to_datetime(df2['date_time'])
print(df2['date_time'])

source = ColumnDataSource(data=dict(x=df2.date_time,y=df2.stock_price,z=df2.avg_sentiment,a=df2.most_neg_tweet))

#print(date_list,price_list)

plot = figure(title= "Stock price with sentiment graph", x_axis_label='Date', y_axis_label='Stock price',x_axis_type='datetime')
plot.line(x="x",y="y",source=source ,line_color='blue', line_width = 5)

for a in range(len(df2.date_time)):
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
    ('Average sentiment', '@z'),
    ('Exact price', '@y'),
    ('most_neg_twt', '@a')
]
plot.add_tools(hover)

output_file("test.html")
show(plot)




