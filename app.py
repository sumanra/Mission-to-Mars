
# import sys
from flask import Flask, render_template, jsonify, redirect
import pymongo
import scrape_mars

# sys.setrecursionlimit(2000)
app = Flask(__name__)


client = pymongo.MongoClient()
db = client.mars_db
collection = db.mars_facts

@app.route('/scrape')
def scrape():
    # db.collection.remove()
    # collection.remove()
    #mars = mongo.db.mars
    mars_data = scrape_mars.scrape()
    collection.update(
        {},
        mars_data,
        upsert=True
    )
    return 'Scraping Successful!'

@app.route("/")
def home():
    mars = {'news_title': "NASA Social Media and Websites Win Webby Awards", 'news_paragraph': "NASA's social media presence, the InSight mission social media accounts, NASA.gov and SolarSystem.NASA.gov will be honored at the 2019 Webby Awards - 'the Oscars of the Internet.'", 'featured_image': 'https://www.jpl.nasa.gov//spaceimages/images/largesize/PIA22911_hires.jpg', 'mars_weather': 'InSight sol 145 (2019-04-24) low -98.1ºC (-144.6ºF) high -19.3ºC (-2.8ºF) winds from the SW at 4.4 m/s (9.8 mph) gusting to 11.6 m/s (26.1 mph) pressure at 7.40 hPapic', 'hemisphere_img_url': [{'image title': 'Cerberus Hemisphere Enhanced', 'image url': 'https://astrogeology.usgs.gov//cache/images/cfa62af2557222a02478f1fcd781d445_cerberus_enhanced.tif_full.jpg'}, {'image title': 'Schiaparelli Hemisphere Enhanced', 'image url': 'https://astrogeology.usgs.gov//cache/images/3cdd1cbf5e0813bba925c9030d13b62e_schiaparelli_enhanced.tif_full.jpg'}, {'image title': 'Syrtis Major Hemisphere Enhanced', 'image url': 'https://astrogeology.usgs.gov//cache/images/ae209b4e408bb6c3e67b6af38168cf28_syrtis_major_enhanced.tif_full.jpg'}, {'image title': 'Valles Marineris Hemisphere Enhanced', 'image url': 'https://astrogeology.usgs.gov//cache/images/7cf2da4bf549ed01c17f206327be4db7_valles_marineris_enhanced.tif_full.jpg'}]}
    db.mars_facts.insert_one(mars)
    #mars = list(db.mars_facts.find())
    mars = db.mars_facts.find_one()
    return render_template('index.html', data=mars)

if __name__ == "__main__":
    app.run(debug=True)


