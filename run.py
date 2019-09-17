import os
import pymongo
from datetime import datetime
from flask import Flask, render_template, redirect, request, url_for, session, flash
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from flaskext.markdown import Markdown, Extension

app = Flask(__name__)

app.config['SECRET_KEY'] = '6e77bdc3d147ec81761e0df80b1f5a62'
app.config["MONGO_DBNAME"] = 'TheBlogsApp'
app.config["MONGO_URI"] = os.getenv('MONGO_URI', 'mongodb://localhost')

Markdown(app)
mongo = PyMongo(app)

# HOME NAVIGATION
@app.route('/')
@app.route('/index')
def index():
    return render_template("index.html")

# GET ARTICLES NAVIGATION
@app.route('/articles', methods=['POST', 'GET'])
def get_articles():
    title = "Articles"
    return render_template("articles.html",
    articles=mongo.db.articles.find().sort("create_date", pymongo.DESCENDING),
    title=title)

# GET COUNTRIES NAVIGATION
@app.route('/countries')
def get_countries():
    title = "Countries"
    return render_template("countries.html",
    locations=list(mongo.db.locations.find()),
    countries=mongo.db.countries.find(),
    title=title)

# GET ADVENTURES NAVIGATION
@app.route('/adventures')
def get_adventures():
    title = "Adventures"
    return render_template("adventures.html",
    adventures=mongo.db.adventures.find().sort("start_date", pymongo.ASCENDING),
    title=title)

# SIGN UP
@app.route('/sign_up', methods=['POST', 'GET'])
def sign_up():
    title = "Sign Up"
    return render_template('sign_up.html',
    title=title)

# SIGN IN
@app.route('/sign_in', methods=['POST', 'GET'])
def sign_in():
    title = "Sign In"
    return render_template('sign_in.html',
    title=title)

# ADDING ARTICLES, COUNTRIES AND ADVENTURES

@app.route('/write_article')
def write_article():
    title = "Write Article"
    return render_template("write_article.html",
    articles=mongo.db.articles.find(),
    title=title)

@app.route('/insert_article', methods=['POST'])
def insert_article():
    articles = mongo.db.articles
    data = request.form.to_dict()
    data["create_date"] = datetime.utcnow().strftime('%d %B %Y - %H:%M')
    articles.insert_one(data)
    return redirect(url_for('get_articles'))

@app.route('/add_country')
def add_country():
    title = "Add Country"
    return render_template("add_country.html",
    locations=mongo.db.locations.find(),
    risks=mongo.db.risks.find(),
    title=title)

@app.route('/insert_country', methods=['POST'])
def insert_country():
    countries = mongo.db.countries
    countries.insert_one(request.form.to_dict())
    return redirect(url_for('get_countries'))

@app.route('/create_adventure')
def create_adventure():
    title = "Create Adventure"
    return render_template("create_adventure.html",
    locations=list(mongo.db.locations.find()),
    countries=list(mongo.db.countries.find()),
    title=title)

@app.route('/insert_adventure', methods=['POST'])
def insert_adventure():

    start_date = datetime.strptime(request.form.get('start_date'), "%d %B, %Y")

    new_adventure = {
        "adventure_name": request.form.get('adventure_name'),
        "duration": request.form.get('duration'),
        "start_date": datetime.strftime(start_date, "%Y, %B %d"),
        "budget": request.form.get('budget'),
        "countries": request.form.getlist('countries')
    }
    inserted = mongo.db.adventures.insert_one(new_adventure)
    return redirect(url_for('get_adventures'))

# EDITING ARTICLES, COUNTRIES AND ADVENTURES

@app.route('/edit_country/<country_id>')
def edit_country(country_id):
    the_country = mongo.db.countries.find_one({"_id": ObjectId(country_id)})
    title = "Edit Country"
    return render_template('edit_country.html',
    country=the_country,
    locations=mongo.db.locations.find(),
    risks=mongo.db.risks.find(),
    title=title)

@app.route('/update_country/<country_id>', methods=['POST'])
def update_country(country_id):
    mongo.db.countries.update(
        {'_id': ObjectId(country_id)},
        {
            "country_name": request.form.get('country_name'),
            "country_location": request.form.get('country_location'),
            "country_currency": request.form.get('country_currency'),
            "country_risk": request.form.get('country_risk'),
            "country_language": request.form.get('country_language'),
            "reasons_to_go": request.form.get('reasons_to_go')
        })
    return redirect(url_for('get_countries'))

@app.route('/edit_article/<article_id>')
def edit_article(article_id):
    the_article = mongo.db.articles.find_one({"_id": ObjectId(article_id)})
    title = "Edit Article"
    return render_template('edit_article.html',
    article=the_article,
    title=title)

@app.route('/update_article/<article_id>', methods=['POST'])
def update_article(article_id):
    mongo.db.articles.update(
        {'_id': ObjectId(article_id)},
        {
            "title": request.form.get('title'),
            "author": request.form.get('author'),
            "create_date": datetime.utcnow().strftime('%d %B %Y - %H:%M'),
            "body": request.form.get('body'),
        })
    return redirect(url_for('get_articles'))

@app.route('/edit_adventure/<adventure_id>')
def edit_adventure(adventure_id):
    the_adventure = mongo.db.adventures.find_one({"_id": ObjectId(adventure_id)})
    title = "Edit Adventure"
    return render_template('edit_adventure.html',
    adventure=the_adventure,
    locations=list(mongo.db.locations.find()),
    countries=list(mongo.db.countries.find()),
    title=title)

@app.route('/update_adventure/<adventure_id>', methods=['POST'])
def update_adventure(adventure_id):

    start_date = datetime.strptime(request.form.get('start_date'), "%d %B, %Y")

    mongo.db.adventures.update(
        {'_id': ObjectId(adventure_id)},
        {
            "adventure_name": request.form.get('adventure_name'),
            "countries": request.form.getlist('countries'),
            "duration": request.form.get('duration'),
            "start_date": datetime.strftime(start_date, "%Y, %B %d"),
            "budget": request.form.get('budget')
        })
    return redirect(url_for('get_adventures'))

# DELETING ARTICLES, COUNTRIES AND ADVENTURES
@app.route('/delete_article/<article_id>')
def delete_article(article_id):
    mongo.db.articles.remove({'_id': ObjectId(article_id)})
    return redirect(url_for('get_articles'))

@app.route('/delete_country/<country_id>')
def delete_country(country_id):
    mongo.db.countries.remove({'_id': ObjectId(country_id)})
    return redirect(url_for('get_countries'))

@app.route('/delete_adventure/<adventure_id>')
def delete_adventure(adventure_id):
    mongo.db.adventures.remove({'_id': ObjectId(adventure_id)})
    return redirect(url_for('get_adventures'))

# SINGLE ARTICLE PAGE
@app.route('/article/<article_id>')
def single_article(article_id):
    article=mongo.db.articles.find_one({'_id': ObjectId(article_id)})
    title = "Article"

    return render_template('single_article.html',
    article=article,
    adventures=list(mongo.db.adventures.find()),
    countries=list(mongo.db.countries.find()),
    title=title)

# SINGLE COUNTRY PAGE
@app.route('/country/<country_id>')
def single_country(country_id):
    country=mongo.db.countries.find_one({'_id': ObjectId(country_id)})
    title = "Country"

    return render_template('single_country.html',
    country=country,
    title=title)

if __name__ == '__main__':
    app.run(host=os.getenv('IP'), port=int(os.getenv('PORT')), debug=True)
