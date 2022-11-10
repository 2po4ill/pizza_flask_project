from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
import db_util

app = Flask(__name__)
app.secret_key = "111"
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://postgres:Init123#@localhost:5432/pizza_shop"
db = SQLAlchemy(app)

pizza_shop = db_util.Database()


class Pizzas(db.Model):
    id = db.Column(db.INTEGER, primary_key=True)
    name = db.Column(db.VARCHAR)
    properties = db.Column(db.TEXT)
    price = db.Column(db.REAL)
    image = db.Column(db.TEXT)


@app.route('/')
def main_page():
    pizzas = Pizzas.query.all()
    context = {
        'pizzas': pizzas,
        'title': "ХОЧУ ПИТСЫ"
    }
    return render_template("main.html", **context)


@app.route("/#popup_<int:pizza_id>")
def get_pizza(pizza_id):
    return render_template("main.html", id=pizza_id)


@app.route("/add", methods=['GET', 'POST'])
def add_pizza():
    if request.method == 'POST':
        name = request.form.get('name')
        properties = request.form.get('properties')
        price = request.form.get('price')
        image = request.form.get('image')
        pizza_id = db.session.query(db.func.max(Pizzas.id)).first()[0]+1
        new_pizza = Pizzas(id=pizza_id, name=name, properties=properties, price=price, image=image)
        db.session.add(new_pizza)
        db.session.commit()
    return render_template("add_pizza.html", title="Добавить пиццу")


if __name__ == '__main__':
    app.run()
