#import dependencies
from flask import Flask, render_template, jsonify, redirect
from flask_pymongo import PyMongo 
import scrape_mars

#create an instance of Flask
app = Flask(__name__)
#use PyMongo to establish Mongo connection
mongo = PyMongo(app, uri="mongodb://localhost:27017/mars.mars_data")

#route to render index.html template using data from Mongo
@app.route("/")
def home():
    mars_data = mongo.db.mars_data.find_one()
    return render_template("index.html", mars_data = mars_data)

#create a scrape route tp import scrape_mars.py script and call scrape function
@app.route("/scrape")
def scrape():
    mars_data = scrape_mars.scrape()
    mongo.db.mars_data.update({}, mars_data, upsert=True)
    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)