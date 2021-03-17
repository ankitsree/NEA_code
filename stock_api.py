'''import pandas as pd
from yahoo_fin import stock_info
import datetime
import matplotlib.pyplot as plt
#df = pd.read_csv(stock_url, parse_dates=True, index_col=0)
alphav_api_key= "E7LPT7HF7GMJ6QLH"
stock_url='https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY_EXTENDED&symbol=MSFT&interval=60min&slice=year1month1&apikey={}'.format(alphav_api_key)
'''
from yahoo_fin import stock_info
from textblob import TextBlob
import csv
from datetime import timedelta
import tweepy
from tweepy import OAuthHandler
import datetime
import re
import pandas as pd
import sys
from flask import Flask, render_template,request,redirect,flash,url_for,session
from flask_sqlalchemy import SQLAlchemy

#from archive import * 
from flask_program import *
from flask_program.models import Companies, Tweets
#from __init__ import *


# keys recieved when creating a developer account on twitter
consumer_key = "2f4kN1axhPOUY2TdN33ugh65P"
consumer_secret = "mkHFVL6XRHUOmhFjgoxdjzu7a1t3foRQq7doAJOOyCr3MgkI7j"
access_token = "1274365795867463681-02F6f7KEyQ2V2P1jpq6qc2kPLRT6tF"
access_token_secret = "3gp0wxDQZ1isDhvte9sUK2mD0lmfJF7ZuEWMXrmv8DGre"


class get_tweets():
    def __init__(self):
        # initialise class variables
        self.tweet_text = ""
        self.tweet_date = ""
        self.list = []#list to keep tweets to later be stored in csv
        self.date_list = []#list to keep datea of tweets to later be stored in csv
        self.time_list = []
        self.cleaned_text = ""

    def tweet_cursor(self, api,search_term):
        try:
            for tweet in tweepy.Cursor(api.search,
                                       q=f"$MSFT -filter:retweets",
                                       lang="en", since="2019-11-03", tweet_mode='extended').items(10):
                #print(tweet)
                self.tweet_text = re.sub(r"http\S+", "", tweet.full_text)#removes any links in the text 
                self.tweet_date = datetime.datetime.strptime(str(tweet.created_at), '%Y-%m-%d %H:%M:%S')#formats date into datetime object
                date_of_tweet = self.tweet_date.date()
                time_of_tweet = self.tweet_date.time()

                #date_time_obj = datetime.datetime.strptime(tweet.created_at, '%Y-%m-%d %H:%M')
                self.cleaned_text = re.sub(r"[^a-zA-Z0-9]+", ' ', self.tweet_text)#pass tweet text to get_text and preprocess the text
                self.list.append(self.cleaned_text.lower())#add cleaned text to list
                self.date_list.append(date_of_tweet)#add date to list
                self.time_list.append(time_of_tweet)
            

        except tweepy.TweepError as e:
            #error handling, so tweepy error are flagged up
            print(f"error is {e}")

    def write_to_csv(self,comp_sign,company):
        total_sent = 0
        #avg_sent = []
        try:
            for i in range(len(self.list)):
                temp_csv = open('msft5.csv', 'a', encoding="utf-8", newline="")
                #opens a file to write tweets and replaces newlines with empty string
                csvWriter = csv.writer(temp_csv)#creates writer object to srite data to csv
                textblob_sent = TextBlob(self.list[i])



                csvWriter.writerow([self.date_list[i],self.time_list[i] ,self.list[i],textblob_sent.sentiment.polarity])#writes row of data to csv
                temp_csv.close()
                if textblob_sent != 0:
                    #print(textblob_sent.sentiment.polarity)
                    total_sent += textblob_sent.sentiment.polarity
        except:
            print("Ther was an error in writing the data to the csv file, possibly due to invalid data or the list of tweets is empty")

        company_df = pd.read_csv('msft5.csv')
        company_df['Sentiment'] = pd.to_numeric(company_df['Sentiment'])
        most_pos_index = company_df['Sentiment'].argmax()
        most_neg_index = company_df['Sentiment'].argmin()
        neg_tweet = [company_df.iloc[most_neg_index]["tweet_text"],company_df.iloc[most_neg_index]['Sentiment']]
        pos_tweet = [company_df.iloc[most_pos_index]["tweet_text"],company_df.iloc[most_pos_index]['Sentiment']]
        
        avg_sent = total_sent/len(self.list)
        get_tweets.data_to_database(self,avg_sent,neg_tweet,pos_tweet,comp_sign,company)#needs to come out of func



    def data_to_database(self,avgerage_sent,most_neg_twt,most_pos_twt,company_sign,company_obj):
        time_now = datetime.datetime.now()
        now = time_now.replace(second=0, microsecond=0, minute=0, hour=time_now.hour-5)
        dt_string = now.strftime("%Y-%m-%d %H:%M:%S")


        weekno = datetime.datetime.today().weekday()
        current_time = datetime.datetime.now().time()
        start_time = datetime.time(9, 30)
        end_time = datetime.time(16, 15)
        company_share_price = stock_info.get_live_price(company_sign)
        '''data_chunk = Tweets(date_time="14/12/2020",avg_sentiment=0.3,stock_price=241.75,
                                most_pos_tweet="its decent",most_neg_tweet="its not great",tweets_company=company_obj)
        db.session.add(data_chunk)
        db.session.commit()'''
        if weekno < 5:#checks if the date is a weekday(0 for monday and 4 for Friday)
            if now.time()> start_time and now.time()< end_time:#if time is in the range of 9:00 to 16:30
                print("date is within trading hours")
                try:

                    data_chunk = Tweets(date_time=str(dt_string),avg_sentiment=float(avgerage_sent),stock_price=float(company_share_price),
                                    most_pos_tweet=str(most_pos_twt),most_neg_tweet=str(most_neg_twt),tweets_company=company_obj)

                    db.session.add(data_chunk)#add data about the company to database
                    db.session.commit()
                except:
                    print("Error in adding data to database, data may have had same values for columns that only have unique values or invalid datatype")
                print("stock market price for company stored in database")
            else:
                print("time is outside trading hours")
                


        else:
            print("date is weekend, which is outside trading hours")
            

        





if __name__ == "__main__":
    auth = OAuthHandler(consumer_key, consumer_secret)
    # create OAuthHandler object, so keys can be exchanged to authenticate a connection

    auth.set_access_token(access_token, access_token_secret)
    # sets the access token by passing the access token and secret as parameters for the function

    twitter_api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)
    #creates api object to connect cursor to the API
    '''data_chunk = Companies(company_name="Netflix",search_query="netflix",symbol="NFLX")
    db.session.add(data_chunk)
    db.session.commit()'''
    company_list = ["Microsoft","Amazon","Netflix"]
    for company in company_list:
        company_data = Companies.query.filter_by(company_name="Amazon").first()
        company_filter = company_data.search_query
        company_id = company_data.id
        company_symbol = company_data.symbol
        #print(company,company_filter,company_id)
        csvFile = open('msft5.csv', 'w', encoding="utf-8", newline="")
        csvWriter = csv.writer(csvFile)
        headers = ["date","time" ,"tweet_text","Sentiment"]
        csvWriter.writerow(headers)
        csvFile.close()

        cursor_obj = get_tweets() #creates class object
        cursor_obj.tweet_cursor(twitter_api,company_filter)#calls tweet_curosr method with twitter api as a parameter
        cursor_obj.write_to_csv(company_symbol,company_data)#calls write_to_csv method to write tweets to csv file
        #cursor_obj.graph_sentiment()
