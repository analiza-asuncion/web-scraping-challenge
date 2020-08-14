from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars
import time
import pymongo
from pymongo import MongoClient

# Create an instance of Flask
app = Flask(__name__)

# Use PyMongo to establish Mongo connection
mongo = PyMongo(app, uri="mongodb://localhost:27017/mars")


@app.route("/")
def index():
    
    # Find one record of data from the mongo database
    mars_data = mongo.db.collection.find_one()
    return render_template("index.html", mars_data=mars_data)




@app.route("/scrape")
def scraper():


    mars_data = scrape_mars.mars_news_scrape()
    mongo.db.collection.update({}, mars_data, upsert=True)
    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)







