from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars

# Create an instance of Flask
app = Flask(__name__)

# Use PyMongo to establish Mongo connection
mongo = PyMongo(app, uri="mongodb://localhost:27017/mars_mission")


@app.route("/")
def index():
    print("I am on index.html")
    # Find one record of data from the mongo database
    mars = mongo.db.collection.find_one()

    # Return template and data
    return render_template("index.html", mars_data =mars)
	
@app.route("/scrape")
def scrape():     
    
    mars_data = scrape_mars.mars_news_scrape()

    # Update the Mongo database using update and upsert=True
    mongo.db.collection.update({}, mars_data, upsert=True)

    return redirect("/") 

if __name__ == "__main__":
    app.run(debug=True)