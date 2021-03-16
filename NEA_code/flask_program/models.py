from flask_program import db, login_manager
from flask_login import UserMixin


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

follows = db.Table('follows',
        db.Column('user_id',db.Integer,db.ForeignKey('user.id')),
        db.Column('company_id',db.Integer,db.ForeignKey('companies.id'))
) #link table for users and companies 


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

    def __repr__(self):
        return f"User('{self.email}','{self.username}')"
