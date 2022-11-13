from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from datetime import timedelta
from flask_login import LoginManager, UserMixin, current_user, login_user


app = Flask(__name__)
app.secret_key = "111"
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://postgres:Init123#@localhost:5432/pizza_shop"
app.permanent_session_lifetime = timedelta(days=365)
db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)


class Pizzas(db.Model):
    id = db.Column(db.INTEGER, primary_key=True)
    name = db.Column(db.VARCHAR)
    properties = db.Column(db.TEXT)
    price = db.Column(db.REAL)
    image = db.Column(db.TEXT)


class Users(db.Model, UserMixin):
    id = db.Column(db.INTEGER, primary_key=True)
    login = db.Column(db.VARCHAR)
    password = db.Column(db.VARCHAR)
    adress = db.Column(db.TEXT)
    phone = db.Column(db.VARCHAR)


@login_manager.user_loader
def load_user(login):
    user = Users.query.get(login)
    return user


@app.route('/')
def main_page():
    pizzas = Pizzas.query.all()
    users = Users.query.all()
    context = {
        'pizzas': pizzas,
        'user': users,
        'current_user': current_user,
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
        user_id = db.session.query(db.func.max(Users.id)).first()[0] + 1
        new_user = Users(login=login, password=password, adress=adress, phone=phone, id=user_id)
        db.session.add(new_user)
        db.session.commit()
        login_user(new_user)

    return render_template("registration.html", title="Регистрация")


@app.route("/login", methods=['GET', 'POST'])
def log():
    title = 'hello'
    if request.method == 'POST':
        login = request.form.get('login')
        password = request.form.get('password')
        users = Users.query.all()
        for user in users:
            if user.login == login:
                if user.password == password:
                    login_user(user)
                    title = current_user.login
    return render_template("form.html", title=title)


if __name__ == '__main__':
    app.run()
