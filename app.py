from flask import Flask, render_template, request, make_response, session
from flask_sqlalchemy import SQLAlchemy
from datetime import timedelta
import db_util
from random import choice


app = Flask(__name__)
app.secret_key = "111"
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://postgres:Init123#@localhost:5432/pizza_shop"
app.permanent_session_lifetime = timedelta(days=365)
db = SQLAlchemy(app)

pizza_shop = db_util.Database()


class Pizzas(db.Model):
    id = db.Column(db.INTEGER, primary_key=True)
    name = db.Column(db.VARCHAR)
    properties = db.Column(db.TEXT)
    price = db.Column(db.REAL)
    image = db.Column(db.TEXT)


class Users(db.Model):
    login = db.Column(db.VARCHAR, primary_key=True)
    password = db.Column(db.VARCHAR)
    adress = db.Column(db.TEXT)
    phone = db.Column(db.VARCHAR)
    cookie = db.Column(db.VARCHAR)


def createcookie():
    alphabet = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
    string = ""
    for i in range(16):
        string += choice(alphabet)
    return string


@app.route('/')
def main_page():
    pizzas = Pizzas.query.all()
    users = Users.query.all()
    print(cookie().headers)
    context = {
        'pizzas': pizzas,
        'user': users,
        'cookie': cookie(),
        'title': "ХОЧУ ПИТСЫ"
    }
    return render_template("main.html", **context)


@app.route("/add", methods=['GET', 'POST'])
def add_pizza():
    if request.method == 'POST':
        name = request.form.get('name')
        properties = request.form.get('properties')
        price = request.form.get('price')
        image = request.form.get('image')
        pizza_id = db.session.query(db.func.max(Pizzas.id)).first()[0] + 1
        new_pizza = Pizzas(id=pizza_id, name=name, properties=properties, price=price, image=image)
        db.session.add(new_pizza)
        db.session.commit()
    return render_template("add_pizza.html", title="Добавить пиццу")


@app.route("/reg", methods=['GET', 'POST'])
def registration():
    if request.method == 'POST':
        login = request.form.get('login')
        password = request.form.get('password')
        adress = request.form.get('adress')
        phone = request.form.get('phone')
        guest = request.cookies.get('site')
        new_user = Users(login=login, password=password, adress=adress, phone=phone, cookie=guest)
        db.session.add(new_user)
        db.session.commit()
    return render_template("registration.html", title="Регистрация")


@app.route('/cookie/')
def cookie():
    if not request.cookies.get('site'):
        res = make_response("Setting a cookie")
        session['site'] = createcookie()
        res.set_cookie('site', session['site'], 60*60*60*365)
    else:
        res = request.cookies.get('site')
    return res


if __name__ == '__main__':
    app.run()
