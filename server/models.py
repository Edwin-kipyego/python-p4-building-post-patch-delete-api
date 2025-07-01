from flask_sqlalchemy import SQLAlchemy
from sqlalchemy_serializer import SerializerMixin

db = SQLAlchemy()

class Bakery(db.Model, SerializerMixin):
    __tablename__ = 'bakeries'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)

    baked_goods = db.relationship('BakedGood', backref='bakery')

    serialize_rules = ('-baked_goods.bakery',)


class BakedGood(db.Model, SerializerMixin):
    __tablename__ = 'baked_goods'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    price = db.Column(db.Float)

    bakery_id = db.Column(db.Integer, db.ForeignKey('bakeries.id'))

    serialize_rules = ('-bakery.baked_goods',)
