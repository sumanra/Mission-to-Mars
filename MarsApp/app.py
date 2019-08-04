from flask import Flask, render_template
from flask_pymongo import PyMongo
#import PyMongo
import scrape_mars
import os

app = Flask(__name__)

# Use flask_pymongo to set up mongo connection
app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_app"
mongo = PyMongo(app)
# Or set inline
# mongo = PyMongo(app, uri="mongodb://localhost:27017/mars_app")

@app.route("/")
def home():
    mars = mongo.db.mars.find_one()
    #print(mars)
    return render_template("index.html", mars = mars)

@app.route('/scrape')
def scrape():
  
    # Run scrapped functions
    mars = mongo.db.mars
    mars_data = scrape_mars.scrape()
    mars.update({}, mars_data, upsert=True)
    return "Scraping Successful!"



if __name__ == "__main__":
    app.run(debug=True)


