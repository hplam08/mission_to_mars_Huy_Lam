from flask import Flask, render_template, redirect
import pymongo
import scrape_mars

# Create an instance of our Flask app.
app = Flask(__name__)

# Use PyMongo to establish Mongo connection
conn = 'mongodb://localhost:27017'
client = pymongo.MongoClient(conn)
db=client.mission_to_mars

@app.route('/scrape/')
def scrape():
   # Run the scrape function from scrape_mars.py 
   result = scrape_mars.scrape()
   # Load the dictionary to the database
   db.mission_to_mars.update({}, result, upsert=True)
   # Return to the homepage
   return redirect('/')

# Set route

@app.route('/')
def index():
   # Store the entire mars collection in a list
   mars_list = db.mission_to_mars.find_one()
 
   # mars_list = mongo.db.mission_to_mars.find_one()
   print(mars_list)
   # Return the template with the mars_list passed in
   return render_template('index.html', mars_list=mars_list)
if __name__ == "__main__":
   app.run(debug=True)