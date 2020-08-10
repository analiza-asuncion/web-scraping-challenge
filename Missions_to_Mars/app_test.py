from flask import Flask, render_template,redirect
from  flask_pymongo import  PyMongo 
from pymongo import MongoClient
import scrape_mars
import pymongo

import sys

app = Flask(__name__)

# setup mongo connection
app.config["MONGO_URI"] =  "mongodb://localhost:27017/Mars_DB"
mongo = PyMongo(app)

client = pymongo.MongoClient("mongodb://localhost:27017/") 
db = client.Mars_DB
collection = db.mars_collection

result_insert = collection.insert_one(scrape_mars.scrape())
#result_update = collection_object.update(scrape_mars.scrape())

@app.route("/")
def index():
    # write a statement that finds all the items in the db and sets it to a variable
    data=mongo.db.data.find_one()
    # render an index.html template and pass it the data you retrieved from the database
    return render_template("index.html",text="Hello Index", data=data)


@app.route("/scrape")
def scrape():     
    data = mongo.db.data
    data_mars_news    = scrape_mars.mars_news_scrape()
    data_mars_image   = scrape_mars.img_scrape()
    data_mars_weather = scrape_mars.mars_weather()
    data_mars_facts   = scrape_mars.mars_facts()
    data_mars_hem     = scrape_mars.mars_hem()
    data.update ({}, data_mars_news, data_mars_image, data_mars_weather, data_mars_facts, data_mars_hem,upsert=True)
    return redirect("/", code = 302)

if __name__ == "__main__":
    app.run(debug=True)