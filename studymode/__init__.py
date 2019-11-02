from flask import Flask, render_template
from flask_googlemaps import GoogleMaps

app = Flask(__name__)
app.config['SECRET_KEY'] = '5791628bb0b13ce0c676dfde280ba245'
app.config['GOOGLEMAPS_KEY'] = "AIzaSyDXtCfWA1EuXPc4geNQTm2NsIb8xllcCac"
GoogleMaps(app)

#@app.route("/")
#@app.route("/home")
#def home():
  #  return render_template('home.html')


@app.route("/about")
def about():
    return render_template('about.html')




from studymode import routes

