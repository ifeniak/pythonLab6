from flask import Flask, request, jsonify, abort
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import json
import copy


DB_URI = "mysql+pymysql://fram:29/17/02death@localhost:3306/iot-test-db"

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = DB_URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
ma = Marshmallow(app)


class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=False)
    brand_country = db.Column(db.Integer, unique=False)
    origin_country = db.Column(db.Integer, unique=False)
    brand = db.Column(db.String(64), unique=False)
    price = db.Column(db.Float, unique=False)
    recommended_age = db.Column(db.Integer, unique=False)
    creativity_type = db.Column(db.String(64), unique=False)

    def __init__(self, name, brand_country, origin_country, brand, price, recommended_age, creativity_type):
        self.name = name
        self.brand_country = brand_country
        self.origin_country = origin_country
        self.brand = brand
        self.price = price
        self.recommended_age = recommended_age
        self.creativity_type = creativity_type


class ItemSchema(ma.Schema):
    class Meta:
        fields = ('name', 'brand_country', 'origin_country', 'brand', 'price', 'recommended_age', 'creativity_type')


item_schema = ItemSchema()
items_schema = ItemSchema(many=True)


@app.route("/item", methods=["POST"])
def add_item():
    item = Item(request.json['name'],
                request.json['brand_country'],
                request.json['origin_country'],
                request.json['brand'],
                request.json['price'],
                request.json['recommended_age'],
                request.json['creativity_type']
                )
    db.session.add(item)
    db.session.commit()
    return item_schema.jsonify(item)


@app.route("/item", methods=["GET"])
def get_item():
    all_item = Item.query.all()
    result = items_schema.dump(all_item)
    return jsonify({'items': result})


@app.route("/item/<id>", methods=["GET"])
def item_detail(id):
    item = Item.query.get(id)
    if not item:
        abort(404)
    return item_schema.jsonify(item)


@app.route("/item/<id>", methods=["PUT"])
def item_update(id):
    item = Item.query.get(id)
    if not item:
        abort(404)
    old_item = copy.deepcopy(item)
    item.name = request.json['name']
    item.brand_country = request.json['brand_country']
    item.origin_country = request.json['origin_country']
    item.brand = request.json['brand']
    item.price = request.json['price']
    item.recommended_age = request.json['recommended_age']
    item.creativity_type = request.json['creativity_type']
    db.session.commit()
    return item_schema.jsonify(old_item)


@app.route("/item/<id>", methods=["DELETE"])
def item_delete(id):
    item = Item.query.get(id)
    if not item:
        abort(404)
    db.session.delete(item)
    db.session.commit()
    return item_schema.jsonify(item)


if __name__ == '__main__':
    # db.create_all()
    app.run(debug=True, host='127.0.0.1')
