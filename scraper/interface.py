from flask import Flask, render_template, request
from seek_scraper import Seek_Scraper

app = Flask("SeekScrapper")

@app.route('/')
def home():
    return render_template("home.html")

@app.route('/search')
def search():
    keyword = request.args.get("keyword")
    keyword = keyword[0].upper() + keyword[1:]
    region = request.args.get("region")
    region = region[0].upper() + region[1:]
    ## TODO: get jobs using seek_scraper
    
    scraper = Seek_Scraper([keyword], region)
    jobs_db = scraper.scraper()

    return render_template("search.html", keyword = keyword, region = region, jobs_db = jobs_db)

app.run(debug=True)

