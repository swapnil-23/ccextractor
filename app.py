import json
import random
import string
from flask import Flask, render_template, url_for, redirect, request
from flask_mysqldb import MySQL
import MySQLdb.cursors
import yaml
import re

app = Flask(__name__, template_folder="templates")


## taking the config from MySQL yaml 
with open('db.yaml', 'r') as file:
    db = yaml.safe_load(file)

app.config['MYSQL_HOST'] = db['mysql_host']
app.config['MYSQL_USER'] = db['mysql_user']
app.config['MYSQL_PASSWORD'] = db['mysql_password']
app.config['MYSQL_DB'] = db['mysql_db']

mysql = MySQL(app)



## making the logic for the url shortner
def url_shortener(length = 6):
    chars = string.ascii_letters + string.digits
    short_url = "".join(random.choice(chars) for _ in range(length))
    return short_url


## adding to the main homepage
## adding to the main homepage
@app.route('/', methods=["GET", "POST"])
def home():
    if request.method == "POST":
        long_url = request.form['long_url']
        short_url = url_shortener()
        while short_url in shorten_urls:
            short_url = url_shortener()
        
        # Storing the URL in MySQL database
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO urls (short_url, long_url) VALUES (%s, %s)", (short_url, long_url))
        mysql.connection.commit()
        cur.close()
        
        return f"Shortened URL: {request.url_root}{short_url}"
    return render_template("index.html")
        

## making the redirect to the shortend url
@app.route("/<short_url>")
def redirect_url(short_url):
    cur = mysql.connection.cursor()
    cur.execute("SELECT long_url FROM urls WHERE short_url = %s", [short_url])
    url = cur.fetchone()
    cur.close()
    
    if url:
        return redirect(url[0])
    else:
        return "URL not found ERROR 404"


if (__name__) == "__main__":
    app.run(debug=True)

