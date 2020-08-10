from flask import Flask, render_template,redirect
import pymongo
import scrape_mars
import sys

app = Flask(__name__)

# setup mongo connection
conn = "mongodb://localhost:27017"
client = pymongo.MongoClient(conn)
db = client.mars_db
mars = db.mars_collection

mars.insert_one(scrape_mars.mars_news_scrape())

@app.route("/")
def index():
    # write a statement that finds all the items in the db and sets it to a variable
    mars_data=mars_db.find_one()
    # render an index.html template and pass it the data you retrieved from the database
    return render_template("index.html",text="Hello Index", data=mars_data)


@app.route("/scrape")
def scrape():     
    #data = scrape_mars.scrape()
    
    #data_mars_news    = scrape_mars.mars_news_scrape()
    #data_mars_image   = scrape_mars.img_scrape()
    #data_mars_weather = scrape_mars.mars_weather()
    #data_mars_facts   = scrape_mars.mars_facts()
    #data_mars_hem     = scrape_mars.mars_hem()
    #mars.update ({}, data_mars_news, data_mars_image, data_mars_weather, data_mars_facts, data_mars_hem,upsert=True)
    mongo.db.collection.update({},mars_data,upsert=True)
    return redirect("/", code = 302)

if __name__ == "__main__":
    app.run(debug=True)