import json
import string
from flask import Flask, render_template, url_for, redirect, request
import random

app = Flask(__name__, template_folder="templates")

shorten_urls = {}


## making the logic for the url shortner
def url_shortener(length = 6):
    chars = string.ascii_letters + string.digits
    short_url = "".join(random.choice(chars) for _ in range(length))
    return short_url


## adding to the main homepage
@app.route('/', methods = ["GET", "POST"])
def home():
    if request.method == "POST":
        long_url = request.form['long_url']
        short_url = url_shortener()
        while short_url in shorten_urls:
            short_url = url_shortener()
        
        shorten_urls[short_url] = long_url
        return f"Shortend URLS: {request.url_root}{short_url}"
    return render_template("index.html")
        

## making the redirect to the shortend url
@app.route("/<short_url>")
def redirect_url(short_url):
    long_url = shorten_urls.get(short_url)
    if long_url:
        return redirect(long_url)
    else:
        return "URL not found ERROR 404"


if (__name__) == "__main__":

    app.run(debug=True)

