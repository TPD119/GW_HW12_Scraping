from flask import Flask, render_template, redirect, request
from flask_pymongo import PyMongo
import scrape_mars

app = Flask(__name__)

# Use flask_pymongo to set up mongo connection
app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_app"
mongo = PyMongo(app)

# Or set inline
# mongo = PyMongo(app, uri="mongodb://localhost:27017/craigslist_app")

@app.route("/")
def index():
    mars_data = mongo.db.mars_data.find_one()
    return render_template("index.html", mars=mars_data)

@app.route("/scrape")
def scrape():
    mars_data = mongo.db.mars
    mars_data = scrape_mars.scrape()
    mars_data = scrape_mars.scrape_featured()
    mars_data = scrape_mars.scrape_facts()
    mars_data = scrape_mars.scrape_wx()
    mars_data = scrape_mars.scrape_hemispheres()
    mongo.db.mars_data.update({}, mars_data, upsert=True)
    #render_template("index.html", mars=mars_data)
    return redirect("/", code=302)

@app.route('/shutdown')
def shutdown_server():
    func = request.environ.get('werkzeug.server.shutdown')
    if func is None:
        raise RuntimeError('Not running with the Werkzeug Server')
    func()
    return 'Shutting down Flask server...'

if __name__ == "__main__":
    app.run(debug=True)