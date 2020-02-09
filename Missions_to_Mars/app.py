#import dependencies
from flask import Flask, render_template, jsonify, redirect
from flask_pymongo import PyMongo 
import scrape_mars

# Create an instance of Flask
app = Flask(__name__)
# Use PyMongo to establish Mongo connection
mongo = PyMongo(app, uri="mongodb://localhost:27017/mars")

#Route to render index.html template using data from Mongo
@app.route("/")
def home():
    mars = mongo.db.mars.find_one()
    return render_template("index.html", mars = mars)

#create a route
@app.route("/scrape")
def scrape():
    mars_data = scrape_mars.scrape()
    mongo.db.collection.update({}, scrape_mars, upsert=True)
    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)