# Import Tools
from flask import Flask, render_template, redirect, url_for
from flask_pymongo import PyMongo
import scraping

# Set up Flask
app = Flask(__name__)

# Use flask_pymongo to set up mongo connection
app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_app"
mongo = PyMongo(app)

# Define App Route to HTML Page; links visual representation of web app to code that powers it
@app.route("/")
def index():
   mars = mongo.db.mars.find_one() # Use PyMongo to find "mars" collection in db
   return render_template("index.html", mars=mars) # Return HTML template & use "mars" collection

# Define Route Flask will be using
@app.route("/scrape")
def scrape():
   mars = mongo.db.mars # Points to Mongo db
   mars_data = scraping.scrape_all() # Hold newly scraped data
   mars.update_one({}, {"$set":mars_data}, upsert=True) # Updata db w 1st match doc in collection
   return redirect('/', code=302) # Navigate back to update content page

# Run Flask
if __name__ == "__main__":
   app.run()