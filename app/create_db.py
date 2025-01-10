from flask import Flask
from models import Pizzas, Receipt, Users, Ord, db
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://postgres:Init123#@localhost:5432/pizza_shop"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)


if __name__ == '__main__':
    with app.app_context():
        db.create_all()

        # создаем тестовых исполнителей
        pizza1 = Pizzas(name='Пепперони', properties='Пикантная пепперони , увеличенная порция моцареллы, томаты , фирменный томатный соус',
                        price=309, image='https://media.dodostatic.net/image/r:292x292/11ee7d612fc7b7fca5be822752bee1e5.avif', type='pizza')
        pizza2 = Pizzas(name='Ветчина и сыр', properties='Ветчина , моцарелла, фирменный соус альфредо',
                        price=367, image='https://media.dodostatic.net/image/r:292x292/11ee7d60fda22358ac33c6a44eb093a2.avif', type='pizza')
        pizza3 = Pizzas(name='Большой Молочный коктейль с печеньем Орео', properties='Как вкуснее есть печенье? Его лучше пить! Попробуйте молочный коктейль с мороженым и дробленым печеньем «Орео»',
                        price=309, image='https://media.dodostatic.net/image/r:292x292/11ef820bf6602767b33c2d45da6eae6c.avif', type='drink')
        pizza4 = Pizzas(name='Большой лимонад Клубничный Мохито', properties='Клубничная вариация классического безалкогольного коктейля: ягодная сладость и мятная свежесть',
                        price=239, image='https://media.dodostatic.net/image/r:292x292/11ef878adb0df812ab418dfab97eb76f.avif', type='pizza')
        db.session.add_all([pizza1, pizza2, pizza3, pizza4])
        db.session.commit()