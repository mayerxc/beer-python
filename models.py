from app import db

class BeerTreeHouse(db.Model):
    __tablename__ = 'treehouse'

    id = db.Column(db.Integer, primary_key=True)
    item = db.Column(db.String())
    status = db.Column(db.String())
    price = db.Column(db.Float, nullable=True)

    def __init__(self, item, status, price):
        self.item = item
        self.status = status
        self.price = price

    def __repr__(self):
        return '<id {}>'.format(self.id)
    
    def serialize(self):
        return {
            'id': self.id, 
            'brewery': 'Tree House',
            'item': self.item,
            'status': self.status,
            'price':self.price
        }