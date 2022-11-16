from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import timedelta
from flask_login import LoginManager, UserMixin, current_user, login_user, login_required, logout_user


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
    type = db.Column(db.VARCHAR)


class Users(db.Model, UserMixin):
    id = db.Column(db.INTEGER, primary_key=True)
    login = db.Column(db.VARCHAR)
    password = db.Column(db.VARCHAR)
    adress = db.Column(db.TEXT)
    phone = db.Column(db.VARCHAR)
    role = db.Column(db.VARCHAR)
    orders = db.Column(db.ARRAY(db.INTEGER))


class Ord(db.Model):
    id = db.Column(db.INTEGER, primary_key=True)
    pizza_id = db.Column(db.INTEGER)
    size = db.Column(db.INTEGER)
    quantity = db.Column(db.INTEGER)
    price = db.Column(db.REAL)


class Receipt(db.Model):
    id = db.Column(db.INTEGER, primary_key=True)
    orders = db.Column(db.ARRAY(db.INTEGER))
    user_id = db.Column(db.INTEGER)
    total_price = db.Column(db.REAL)


@login_manager.user_loader
def load_user(login):
    user = Users.query.get(login)
    return user


def total():
    conclude = 0
    if current_user.is_active:
        if current_user.orders:
            for order in current_user.orders:
                conclude += Ord.query.get(order).price
    return conclude


def get_pizza_id(string):
    result = ''
    for letter in string:
        if letter in '0123456789':
            result += letter
    return result


@app.route('/', methods=['GET', 'POST'])
def main_page():
    pizzas = Pizzas.query.all()
    conclude = total()
    context = {
        'pizzas': pizzas,
        'current_user': current_user,
        'conclude': conclude,
        'title': "ХОЧУ ПИТСЫ"
    }
    if request.method == 'POST':
        if get_pizza_id(list(request.form.keys())[0]):
            pizza_id = get_pizza_id(list(request.form.keys())[0])
            quantity = request.form.get(f'quantity_{pizza_id}')
            if Pizzas.query.get(pizza_id).type == 'pizza':
                size = request.form.get(f'size_{pizza_id}')
                price = Pizzas.query.get(pizza_id).price * int(quantity) * (int(size) / 25)
            else:
                size = '25'
                price = Pizzas.query.get(pizza_id).price * int(quantity)
            order_id = db.session.query(db.func.max(Ord.id)).first()[0] + 1 if Ord.query.all() else 1
            order = Ord(id=order_id, pizza_id=pizza_id, size=size, quantity=quantity, price=price)
            collision = True
            if current_user.orders:
                for test in current_user.orders:
                    if Ord.query.get(test).pizza_id == int(order.pizza_id) and Ord.query.get(test).size == int(order.size):
                        Ord.query.get(test).quantity += int(order.quantity)
                        if Pizzas.query.get(pizza_id).type == 'pizza':
                            Ord.query.get(test).price = Pizzas.query.get(pizza_id).price \
                                                        * Ord.query.get(test).quantity * (int(size)/25)
                        else:
                            Ord.query.get(test).price = Pizzas.query.get(pizza_id).price * Ord.query.get(test).quantity
                        collision = False
                    else:
                        db.session.add(order)
            else:
                db.session.add(order)
            db.session.commit()
            if Users.query.get(current_user.id).orders:
                orders = Users.query.get(current_user.id).orders.copy()
                orders.append(order_id)
            else:
                orders = [order_id]
            if collision:
                Users.query.get(current_user.id).orders = orders
                db.session.commit()
                return redirect("/")
        else:
            pizza_type = request.form.get('type')
            if request.form.get('price_high'):
                price_high = request.form.get('price_high')
            else:
                price_high = int(db.session.query(db.func.max(Pizzas.price)).first()[0] + 1)
            return render_template("main.html", **context, type=pizza_type,
                                   price_high=int(price_high))
    return render_template("main.html", **context, type='all',
                           price_high=int(db.session.query(db.func.max(Pizzas.price)).first()[0] + 1))


@app.route("/add", methods=['GET', 'POST'])
def add_pizza():
    conclude = total()
    try:
        if current_user.role == 'admin':
            if request.method == 'POST':
                name = request.form.get('name')
                properties = request.form.get('properties')
                pizza_type = request.form.get('type')
                price = request.form.get('price')
                image = request.form.get('image')
                pizza_id = db.session.query(db.func.max(Pizzas.id)).first()[0] + 1 if Pizzas.query.all() else 1
                new_pizza = Pizzas(id=pizza_id, name=name, properties=properties,
                                   type=pizza_type, price=price, image=image)
                db.session.add(new_pizza)
                db.session.commit()
                return redirect('/')
            return render_template("add_pizza.html", title="Добавить пиццу", conclude=conclude)
        else:
            return render_template("error.html", title="ошибочка")
    except Exception as e:
        print(e)
        return render_template("error.html", title="ошибочка")


@app.route("/reg", methods=['GET', 'POST'])
def registration():
    conclude = total()
    if request.method == 'POST':
        login = request.form.get('login')
        password = request.form.get('password')
        adress = request.form.get('adress')
        phone = request.form.get('phone')
        user_id = db.session.query(db.func.max(Users.id)).first()[0] + 1 if Users.query.all() else 1
        new_user = Users(login=login, password=password, adress=adress, phone=phone, id=user_id, role='user')
        db.session.add(new_user)
        db.session.commit()
        login_user(new_user)
        return redirect('/')

    return render_template("registration.html", title="Регистрация", conclude=conclude)


@app.route("/login", methods=['GET', 'POST'])
def log():
    conclude = total()
    if request.method == 'POST':
        login = request.form.get('login')
        password = request.form.get('password')
        users = Users.query.all()
        for user in users:
            if user.login == login:
                if user.password == password:
                    login_user(user)
                    return redirect('/')
    return render_template("form.html", title="Вход в аккаунт", conclude=conclude)


@app.route("/bin")
def bin():
    orders = []
    conclude = 0
    pizzas = Pizzas.query.all()
    for order in current_user.orders:
        orders.append(Ord.query.get(order))
        conclude += Ord.query.get(order).price
    return render_template("bin.html", orders=orders, pizzas=pizzas, conclude=conclude)


@app.route("/edit/<int:pizza_id>", methods=['GET', 'POST'])
def edit(pizza_id):
    conclude = total()
    try:
        if current_user.role == 'admin':
            if request.method == 'POST':
                if list(request.form.keys())[0] == 'delete':
                    db.session.delete(Pizzas.query.get(pizza_id))
                    db.session.commit()
                    return render_template("edit.html", title="Редактировать", pizzas=Pizzas.query.all(), id=pizza_id)
                Pizzas.query.get(pizza_id).name = request.form.get('name')
                Pizzas.query.get(pizza_id).properties = request.form.get('properties')
                Pizzas.query.get(pizza_id).price = request.form.get('price')
                Pizzas.query.get(pizza_id).image = request.form.get('image')
                db.session.commit()
            return render_template("edit.html", title="Редактировать",
                                   pizzas=Pizzas.query.all(), id=pizza_id, conclude=conclude)
        else:
            return render_template("error.html", title="ошибочка")
    except Exception as e:
        print(e)
        return render_template("error.html", title="ошибочка")


@app.route("/profile", methods=['GET', 'POST'])
def profile():
    try:
        conclude = total()
        if request.method == 'POST':
            Users.query.get(current_user.id).adress = request.form.get('adress')
            Users.query.get(current_user.id).phone = request.form.get('phone')
            db.session.commit()
        return render_template("userdata.html", title="Профиль", current_user=current_user, conclude=conclude)
    except Exception as e:
        print(e)
        return render_template("error.html", title="ошибочка")


@app.route("/buy")
def buy():
    receipt_id = db.session.query(db.func.max(Receipt.id)).first()[0] + 1 if Receipt.query.all() else 0
    new_receipt = Receipt(id=receipt_id, orders=current_user.orders, user_id=current_user.id, total_price=total())
    db.session.add(new_receipt)
    db.session.commit()
    Users.query.get(current_user.id).orders = []
    db.session.commit()
    return redirect('/')


@app.route("/delete/<int:order>")
def delete(order):
    temp = Users.query.get(current_user.id).orders.copy()
    db.session.delete(Ord.query.get(order))
    db.session.commit()
    temp.remove(order)
    Users.query.get(current_user.id).orders = temp
    db.session.commit()
    return redirect('/bin')


@app.route("/logout")
@login_required
def logout():
    if current_user.orders:
        for order in Users.query.get(current_user.id).orders:
            db.session.delete(Ord.query.get(order))
            db.session.commit()
        Users.query.get(current_user.id).orders = []
        db.session.commit()
    logout_user()
    return redirect('/')


@app.route("/history")
def history():
    conclude = total()
    receipts = []
    if Receipt.query.all():
        for receipt in Receipt.query.all():
            if receipt.user_id == current_user.id:
                receipts.append(receipt.id)
    receipts.reverse()
    return render_template("history.html", receipts=receipts, conclude=conclude)


@app.route("/details/int:<receipt>")
def details(receipt):
    conclude = total()
    current_receipt = Receipt.query.get(receipt)
    pizzas = Pizzas.query.all()
    orders = []
    for order in current_receipt.orders:
        orders.append(Ord.query.get(order))
    return render_template("details.html", receipt=current_receipt, orders=orders, pizzas=pizzas, conclude=conclude)


@app.route("/readd/int:<receipt>")
def readd(receipt):
    receipt_id = db.session.query(db.func.max(Receipt.id)).first()[0] + 1 if Receipt.query.all() else 0
    new_receipt = Receipt(id=receipt_id, orders=Receipt.query.get(receipt).orders,
                          user_id=Receipt.query.get(receipt).user_id,
                          total_price=Receipt.query.get(receipt).total_price)
    db.session.add(new_receipt)
    db.session.commit()
    return redirect('/')


if __name__ == '__main__':
    app.run()
