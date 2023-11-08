import os, random
from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)

# Change the path for project folder to the pathway of your own pc/laptop.
project_folder = os.path.abspath(r"C:\Users\nicom\OneDrive\Bureaublad\PizzaProject\project")
db_folder = os.path.join(project_folder, "database")
db_file = os.path.join(db_folder, "mydatabase.db")
app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{db_file}"  
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    password = db.Column(db.String(80))

class Pizza(db.Model):
    id = db.Column(db.Integer)
    description = db.Column(db.String(200))
    size = db.Column(db.String(20), primary_key=True)
    price = db.Column(db.Float)
    name = db.Column(db.String(80), primary_key=True)

class Drink(db.Model):
    id = db.Column(db.Integer)
    name = db.Column(db.String(80), primary_key=True)
    price = db.Column(db.Float)

class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    pizza_id = db.Column(db.Integer, db.ForeignKey('pizza.id'))
    drink_id = db.Column(db.Integer, db.ForeignKey('drink.id'))
    date = db.Column(db.DateTime, default=datetime.now)

# function to clear the tables
def clear_tables():
    User.query.delete()
    Pizza.query.delete()
    Drink.query.delete()
    Order.query.delete()
    db.session.commit()

def add_fixed_items():
    # Pizza items
    pizza1 = Pizza(size='Small', description='Tomato, Mozzarella, Salami Piccante, Bell Pepper, Parmesan, Spicy Oil, Oregano', price='8.99', name='Rafaella')
    pizza2 = Pizza(size='Medium', description='Tomato, Mozzarella, Salami Piccante, Bell Pepper, Parmesan, Spicy Oil, Oregano', price='10.99', name='Rafaella')
    pizza3 = Pizza(size='Large', description='Tomato, Mozzarella, Salami Piccante, Bell Pepper, Parmesan, Spicy Oil, Oregano', price='12.99', name='Rafaella')
    pizza4 = Pizza(size='Small', description='Tomato, Mozzarella, Parmesan, Basil, Extra Virgin Olive Oil.', price='8.99', name='Margherita')
    pizza5 = Pizza(size='Medium', description='Tomato, Mozzarella, Parmesan, Basil, Extra Virgin Olive Oil.', price='10.99', name='Margherita')
    pizza6 = Pizza(size='Large', description='Tomato, Mozzarella, Parmesan, Basil, Extra Virgin Olive Oil.', price='12.99', name='Margherita')
    pizza7 = Pizza(size='Small', description='Mozzarella, Gouda, Parmesan, Gorgonzola.', price='8.99', name='Quattro Formaggi')
    pizza8 = Pizza(size='Medium', description='Mozzarella, Gouda, Parmesan, Gorgonzola.', price='10.99', name='Quattro Formaggi')
    pizza9 = Pizza(size='Large', description='Mozzarella, Gouda, Parmesan, Gorgonzola.', price='12.99', name='Quattro Formaggi')
    pizza10 = Pizza(size='Small', description='Tomato, Mozzarella, Pancetta, Mushrooms, Olives, Artichoke.', price='8.99', name='Capricciosa')
    pizza11 = Pizza(size='Medium', description='Tomato, Mozzarella, Pancetta, Mushrooms, Olives, Artichoke.', price='10.99', name='Capricciosa')
    pizza12 = Pizza(size='Large', description='Tomato, Mozzarella, Pancetta, Mushrooms, Olives, Artichoke.', price='12.99', name='Capricciosa')
    pizza13 = Pizza(size='Small', description='Mozzarella, smoked provolone, pancetta, egg yolk, pecorino', price='8.99', name='Carbonara')
    pizza14 = Pizza(size='Medium', description='Mozzarella, smoked provolone, pancetta, egg yolk, pecorino', price='10.99', name='Carbonara')
    pizza15 = Pizza(size='Large', description='Mozzarella, smoked provolone, pancetta, egg yolk, pecorino', price='12.99', name='Carbonara')
    pizza16 = Pizza(size='Small', description='Mozzarella, ricotta, dried tomatoes, red onions, eggplant, olives', price='8.99', name='Vegetariana')
    pizza17 = Pizza(size='Medium', description='Mozzarella, ricotta, dried tomatoes, red onions, eggplant, olives', price='10.99', name='Vegetariana')
    pizza18 = Pizza(size='Large', description='Mozzarella, ricotta, dried tomatoes, red onions, eggplant, olives', price='12.99', name='Vegetariana')
    db.session.add_all([pizza1, pizza2, pizza3, pizza4, pizza5, pizza6, pizza7, pizza8, pizza9, pizza10, pizza11, pizza12, pizza13, pizza14, pizza15, pizza16, pizza17, pizza18])

    # Drink items
    drink1 = Drink(name='Homemade Lemonade', price=2.99)
    drink2 = Drink(name='Coke', price=1.99)
    drink3 = Drink(name='Moretti beer', price=2.99)
    drink4 = Drink(name='none', price=0)


    db.session.add_all([drink1, drink2, drink3, drink4])

    db.session.commit()

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/menu', methods=['GET', 'POST'])
def mario():
    return render_template('menu.html')

@app.route('/order')
def order():
    return render_template('order.html')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/order', methods=['POST', 'GET'])
def pizzas():   
    return render_template('order.html')

@app.route('/drinks')
def drinks():
    return render_template('drinks.html', drinks=drinks)

@app.route('/checkout', methods=['GET', 'POST'])
def checkout():
    if request.method == 'POST':
        
        size = request.form['size']
        name = request.form['pizza']
        quantity = int(request.form['quantity'])
        beverage = request.form['beverage']
        bev_quantity = int(request.form['bevquantity']) 
        pizzas = []
        ordered_pizzas = Pizza.query.filter_by(size=size, name=name).all()
        
        for pizza in ordered_pizzas:
            pizzas.append(name)
        pizza_price_query = Pizza.query.filter_by(size=size, name=name).with_entities(Pizza.price).first()
        pizza_price = float(str(pizza_price_query[0]))
        bev_price_query = Drink.query.filter_by(name=beverage).with_entities(Drink.price).first()
        bev_price = float(str(bev_price_query[0]))
        total_price = (pizza_price * quantity) + (bev_price * bev_quantity)
        
    return render_template('checkoutpage.html', pizzas=pizzas,
                            size=size, name=name, quantity=quantity,
                            pizza_price=pizza_price, beverage=beverage, bev_quantity=bev_quantity, bev_price=bev_price, total_price=total_price)

@app.route('/orderdone', methods=['GET', 'POST'])
def orderdone():
    return render_template('orderdone.html')




if __name__ == '__main__':
    with app.app_context():
        db.create_all() 
        # add_fixed_items() #use to add the fixed items
        # clear_tables() #use to clear the tables
    app.run(debug=True)
