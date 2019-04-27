
import sys
from flask import Flask, render_template, jsonify, redirect
from flask_pymongo import PyMongo
#import PyMongo
import scrape_mars
import os

#sys.setrecursionlimit(2000)
app = Flask(__name__)

# Use PyMongo to establish Mongo connection
mongo = PyMongo(app, uri="mongodb://localhost:27017/mars_app")


# Use flask_pymongo to set up mongo connection
#app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_app"
#mongo = PyMongo(app)

#client = PyMongo.MongoClient()
#db = client.mars_db
#collection = db.mars_facts

@app.route("/")
def home():
    #mars = list(db.mars_facts.find())
    mars = mongo.db.mars.find_one()
    #print(mars)
    return render_template("index.html", mars = mars)

@app.route('/scrape')
def scrape():
    # db.collection.remove()  
    # Run scrapped functions
    mars = mongo.db.mars
    mars_data = scrape_mars.scrape_mars_news()
    mars_data = scrape_mars.scrape_mars_image()
    mars_data = scrape_mars.scrape_mars_facts()
    mars_data = scrape_mars.scrape_mars_weather()
    mars_data = scrape_mars.scrape_mars_hemispheres()
    mars.update({}, mars_data, upsert=True)

    return redirect("/", code=302)


if __name__ == "__main__":
    app.run(debug=True)


