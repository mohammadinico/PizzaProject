import os, sqlite3
from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)

# Change the path for project folder to the pathway of your own pc/laptop.
project_folder = os.path.abspath(r"C:\Users\Nico\Desktop\PizzaProject\project")
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
    size = db.Column(db.String(20), primary_key=True)
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
    pizza1 = Pizza(size='Small', description='Pepperoni pizza', price='8.99', name='Pepperoni Lovers')
    pizza2 = Pizza(size='Medium', description='Pepperoni pizza', price='10.99', name='Pepperoni Lovers')
    pizza3 = Pizza(size='Large', description='Pepperoni pizza', price='12.99', name='Pepperoni Lovers')
    pizza4 = Pizza(size='Small', description='Margherita pizza', price='8.99', name='Classic Margherita')
    pizza5 = Pizza(size='Medium', description='Margherita pizza', price='10.99', name='Classic Margherita')
    pizza6 = Pizza(size='Large', description='Margherita pizza', price='12.99', name='Classic Margherita')
    pizza7 = Pizza(size='Small', description='Vegetarian pizza', price='8.99', name='Veggie Delight')
    pizza8 = Pizza(size='Medium', description='Vegetarian pizza', price='10.99', name='Veggie Delight')
    pizza9 = Pizza(size='Large', description='Vegetarian pizza', price='12.99', name='Veggie Delight')

    db.session.add_all([pizza1, pizza2, pizza3, pizza4, pizza5, pizza6, pizza7, pizza8, pizza9])

    # Drink items
    drink1 = Drink(size='0.33L', name='Coca-Cola', price=1.99)
    drink2 = Drink(size='0.5L', name='Coca-Cola', price=2.49)
    drink3 = Drink(size='0.33L', name='Sprite', price=1.99)
    drink4 = Drink(size='0.5L', name='Sprite', price=2.49)
    drink5 = Drink(size='0.33L', name='Sprite', price=1.99)
    drink6 = Drink(size='0.5L', name='Sprite', price=2.49)

    db.session.add_all([drink1, drink2, drink3, drink4, drink5, drink6])

    db.session.commit()

@app.route('/pizzas')
def pizzas():   
    return render_template('pizzas.html')

@app.route('/drinks')
def drinks():
    return render_template('drinks.html', drinks=drinks)

@app.route('/checkout', methods=['GET', 'POST'])
def checkout():
    if request.method == 'POST':
        
        size = request.form['size']
        name = request.form['name']
        quantity = int(request.form['quantity'])
        pizzas = []
        ordered_pizzas = Pizza.query.filter_by(size=size, name=name).all()
        for pizza in ordered_pizzas:
            pizzas.append(name)
        price = Pizza.query.filter_by(size=size, name=name).with_entities(Pizza.price).first()
        pizza_price = price[0]
        total_price = pizza_price * quantity
        
    return render_template('checkout.html', pizzas=pizzas,
                            size=size, name=name, quantity=quantity,
                            price=price, total_price=total_price)

@app.route('/orderdone')
def orderdone():
    return render_template('orderdone.html')

@app.route('/luigi')
def luigi():
    return render_template('luigi.html')

@app.route('/mario')
def mario():
    return render_template('mario.html')

if __name__ == '__main__':
    with app.app_context():
        db.create_all() 
        # add_fixed_items() #use to add the fixed items
        # clear_tables() #use to clear the tables
    app.run(debug=True)
