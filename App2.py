from flask import Flask, render_template, redirect, url_for
from sqlalchemy import UniqueConstraint
from flask_pymongo import PyMongo
import scraping


#  Set up Flask 

app = Flask(__name__)

# Use flask_pymongo to set up mongo connection

app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_app"
mongo = PyMongo(app)

# let's define the route for the HTML pag

@app.route("/")
def index():
   mars = mongo.db.mars.find_one()
   return render_template("index.html", mars=mars)


#  add the next route and function to our code

@app.route("/scrape")
def scrape():
   mars = mongo.db.mars
   mars_data = scraping.scrape_all()
   mars.update_one({}, {"$set":mars_data}, upsert=True)
   return redirect('/', code=302)

# Let's take a look at the syntax we'll use, as shown below:

if __name__ == "__main__":
   app.run()