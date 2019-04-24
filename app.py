# Import our pymongo library, which lets us connect our Flask app to our Mongo database.
import pymongo
from scrape_mars import scrape
from flask import Flask, render_template, make_response
from bs4 import BeautifulSoup

# Create an instance of our Flask app.
app = Flask(__name__)



# Set route scrape
@app.route('/scrape')
def scr():
    
    # Create connection variable
    conn = 'mongodb://localhost:27017'
    # Pass connection to the pymongo instance.
    client = pymongo.MongoClient(conn)
    # Cnnect to a database. Will create one if not already available.
    db = client.mars_db
    # Drops collection if available to remove duplicates
    db.scrape_results.drop()
    # Creates a collection in the database and inserts two documents
    mars_dict=scrape()
    db.scrape_results.insert_many([mars_dict])
    return render_template('index.html', mars_dict=mars_dict)
    

# Set route
@app.route('/')
def indx():
    # Create connection variable
    conn = 'mongodb://localhost:27017'
    # Pass connection to the pymongo instance.
    client = pymongo.MongoClient(conn)
    # Cnnect to a database. Will create one if not already available.
    db = client.mars_db
    mars_dict=db.scrape_results.find()[0]
    return render_template('index.html', mars_dict=mars_dict)


if __name__ == "__main__":
    app.run(debug=True)
