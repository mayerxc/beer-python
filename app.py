import os
import requests
from bs4 import BeautifulSoup
from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from decouple import config


app = Flask(__name__)

# app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['APP_SETTINGS']
# app.config['SQLALCHEMY_DATABASE_URI'] = 'postgressql://localhost/beer'
# app.config.from_object(os.environ['APP_SETTINGS'])

def get_env_variable(name):
    try:
        # print(os.environ[name])
        return os.environ[name]
    except KeyError:
        message = "Expected environment variable '{}' not set.".format(name)
        raise Exception(message)

# the values of those depend on your setup
POSTGRES_URL = get_env_variable("POSTGRES_URL")
POSTGRES_USER = get_env_variable("POSTGRES_USER")
POSTGRES_PW = get_env_variable("POSTGRES_PW")
POSTGRES_DB = get_env_variable("POSTGRES_DB")


DB_URL = 'postgresql+psycopg2://{user}:{pw}@{url}/{db}'.format(user=POSTGRES_USER,pw=POSTGRES_PW,url=POSTGRES_URL,db=POSTGRES_DB)
# config['SQLALCHEMY_DATABASE_URI'] = DB_URL
app.config['SQLALCHEMY_DATABASE_URI'] = POSTGRES_URL
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False # silence the deprecation warning

db = SQLAlchemy(app)
migrate = Migrate(app, db)

# from models import BeerTreeHouse

class BeerTreeHouse(db.Model):
    __tablename__ = 'treehouse'

    id = db.Column(db.Integer, primary_key=True)
    brewery = db.Column(db.String())
    item = db.Column(db.String())
    status = db.Column(db.String())
    price = db.Column(db.Float, nullable=True)

    def __init__(self, brewery, item, status, price):
        self.brewery = brewery
        self.item = item
        self.status = status
        self.price = price

    def __repr__(self):
        return '<id {}>'.format(self.id)
    
    def serialize(self):
        return {
            'id': self.id, 
            'brewery': self.brewery,
            'item': self.item,
            'status': self.status,
            'price':self.price
        }


def convertToFloat(value):
    try:
        return float(value)
    except ValueError:
        return None

@app.route('/')
def index():
    return "<h1>Please go to /beer to get the JSON</h1>"


@app.route('/beer')
def getBeer():
    beerHtml = requests.get("https://www.treehouseonthefly.com/shop")
    
    soup = BeautifulSoup(beerHtml.text, 'html.parser')
    soupBeerList = []

    # timestampStr = dateTimeObj.strftime("%d-%b-%Y (%H:%M:%S.%f)")
    # print(timestampStr)
    for item in soup.findAll('section', {'class':'grid-meta-wrapper'}):
        try:
            beerDict = {
                'brewery': 'Tree House',
                'item': item.find(class_='grid-title').text,
                'status': item.find(class_='grid-meta-status').text.strip(),
                'price': convertToFloat(item.find(class_='product-price').text.strip())
            }
            beerToAdd = BeerTreeHouse(brewery='Tree House', item=beerDict['item'], status=beerDict['status'], price=beerDict['price'])
            db.session.add(beerToAdd)
            db.session.commit()
        except Exception as e:
            return (str(e))


        soupBeerList.append({
            'brewery': 'Tree House',
            'item': item.find(class_='grid-title').text,
            'status': item.find(class_='grid-meta-status').text.strip(),
            'price': convertToFloat(item.find(class_='product-price').text.strip())
        })
    return jsonify(soupBeerList)


@app.route('/environment')
def environment(): 
    print(POSTGRES_URL)
    return jsonify({'url': POSTGRES_URL})



# @app.route('/treehouse')
# def treeHouse():
    # requests.get

# if __name__ == '__main__':
#     # Threaded option to enable multiple instances for multiple user access support
#     app.run(threaded=True, port=5000, debug=True)
