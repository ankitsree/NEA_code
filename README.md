# Stock prediction using twitter sentiment analysis project

Welcome to my sentiment analysis python project. The aim of the project is to collect tweets about companies(in my program that is limited to 
amazon, microsoft and facebook) and conduct sentiment analysis on those tweets and plot this data on a graph along with the stock price to indicate to a user the 
pattern between public sentiment and the stock price of a company. I have made a web application to allow the user to create an account and login to see the results. 
The user's data is stored in a sqlalchemy database and verification has been added to make sure only users in the database can login if the crendentials are correct. 
This project is split into a few different components: The stock_api.py file and the NEA_code file which contains a flask_program file with all the files for the web applicaiton.


The stock_api.py file is the backend file which runs the twitter scraper and collects tweets for a pre-defined list of companies and uses and API to collect the 
stock price of each of those companies. The flask_program file in the NEA_code file contains the files for the sqlalchemy databse and the code for the web applicaiton. 
