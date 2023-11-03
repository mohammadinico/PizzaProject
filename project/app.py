import os
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)

# Set the path for the database file
project_folder = os.path.abspath("project")
db_folder = os.path.join(project_folder, "database")
db_file = os.path.join(db_folder, "mydatabase.db")
app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{db_file}"  # SQLite database file
db = SQLAlchemy(app)

# Define User, Pizza, Drink, and Order models
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    password = db.Column(db.String(80))

class Pizza(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    size = db.Column(db.String(20))
    quantity = db.Column(db.Integer)
    description = db.Column(db.String(200))
    price = db.Column(db.Float)
    name = db.Column(db.String(80))

class Drink(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    size = db.Column(db.String(20))
    quantity = db.Column(db.Integer)
    name = db.Column(db.String(80))
    price = db.Column(db.Float)

class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    pizza_id = db.Column(db.Integer, db.ForeignKey('pizza.id'))
    drink_id = db.Column(db.Integer, db.ForeignKey('drink.id'))
    date = db.Column(db.DateTime, default=datetime.now)

@app.route('/pizzas')
def pizzas():
    pizzas = Pizza.query.all()
    return render_template('pizzas.html', pizzas=pizzas)

@app.route('/drinks')
def drinks():
    drinks = Drink.query.all()
    return render_template('drinks.html', drinks=drinks)

@app.route('/checkout')
def checkout():
    return render_template('checkout.html')

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
    # Create the database tables if they don't exist
    with app.app_context():
        db.create_all()
    app.run(debug=True)
