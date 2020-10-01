import requests
from bs4 import BeautifulSoup
from flask import Flask, jsonify


app = Flask(__name__)


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
    for item in soup.findAll('section', {'class':'grid-meta-wrapper'}):
        soupBeerList.append({
            'brewery': 'Tree House',
            'item': item.find(class_='grid-title').text,
            'status': item.find(class_='grid-meta-status').text.strip(),
            'price': convertToFloat(item.find(class_='product-price').text.strip())
        })
    return jsonify(soupBeerList)


if __name__ == '__main__':
    # Threaded option to enable multiple instances for multiple user access support
    app.run(threaded=True, port=5000, debug=True)
