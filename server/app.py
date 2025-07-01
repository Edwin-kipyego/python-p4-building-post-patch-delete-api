from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from models import db, Bakery, BakedGood

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
migrate = Migrate(app, db)  # <-- ✅ Add this line

@app.route('/baked_goods', methods=['POST'])
def create_baked_good():
    name = request.form.get('name')
    price = request.form.get('price')
    bakery_id = request.form.get('bakery_id')

    if not all([name, price, bakery_id]):
        return jsonify({"error": "Missing data"}), 400

    new_good = BakedGood(name=name, price=float(price), bakery_id=int(bakery_id))
    db.session.add(new_good)
    db.session.commit()

    return jsonify(new_good.to_dict()), 201

@app.route('/bakeries/<int:id>', methods=['PATCH'])
def update_bakery(id):
    bakery = Bakery.query.get(id)
    if not bakery:
        return jsonify({"error": "Bakery not found"}), 404

    name = request.form.get('name')
    if name:
        bakery.name = name
        db.session.commit()

    return jsonify(bakery.to_dict()), 200

@app.route('/baked_goods/<int:id>', methods=['DELETE'])
def delete_baked_good(id):
    baked_good = BakedGood.query.get(id)
    if not baked_good:
        return jsonify({"error": "Baked good not found"}), 404

    db.session.delete(baked_good)
    db.session.commit()

    return jsonify({"message": "Baked good successfully deleted"}), 200

if __name__ == '__main__':
    app.run(port=5555, debug=True)
