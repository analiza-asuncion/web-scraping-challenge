from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars
import time


app = Flask(__name__)



# Use PyMongo to establish Mongo connection
app.config["MONGO_URI"] = "mongodb://localhost:27017/weather_app"
mongo = PyMongo(app)
mongo.db.mars_data.drop()


@app.route("/")
def index():
    mars_data = mongo.db.mars_data.find_one()
    return render_template("index.html", mars_data=mars_data)


@app.route("/scrape")
def scraper():
    mars_data = mongo.db.mars_data
    mars_data = scrape_mars.mars_news_scrape()
    mongo.db.collection.update({}, mars_data, upsert=True)
    return redirect("/", code=302)


if __name__ == "__main__":
    app.run(debug=True)