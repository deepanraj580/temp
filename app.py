from flask import Flask, render_template, request, flash, redirect, url_for, request
from flask_sqlalchemy import SQLAlchemy
from fuzzywuzzy import process,fuzz

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_strong_and_unique_secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


# Create a model for fertilizer stock
class FertilizerStock(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    category = db.Column(db.String(255), nullable=False)
    subcategory = db.Column(db.String(255), nullable=False)
    price = db.Column(db.Float, nullable=False)
    quantity = db.Column(db.Integer, nullable=False)


# Create a model for customer details
class CustomerDetails(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), nullable=False)
    city = db.Column(db.String(255), nullable=False)
    country = db.Column(db.String(255), nullable=False)
    phone_number = db.Column(db.String(20), nullable=False)


# Create tables
with app.app_context():
    db.create_all()

# Route to display the home page
@app.route('/')
def home():
    return render_template('index.html')

# Route to display the form to add fertilizer stock
# Route to display the form to add fertilizer stock
@app.route('/add_stock', methods=['GET', 'POST'])
def add_stock():
    if request.method == 'POST':
        name = request.form['name']
        category = request.form['category']
        subcategory = request.form['subcategory']
        price = float(request.form['price'])
        quantity = int(request.form['quantity'])

        # Check if the same data already exists in the database
        existing_stock = FertilizerStock.query.filter_by(name=name, category=category, subcategory=subcategory).first()

        if existing_stock:
            return render_template('add_stock.html', message='Data already exists', alert_type='danger')

        try:
            # Insert data into fertilizer_stock table
            stock = FertilizerStock(name=name, category=category, subcategory=subcategory, price=price, quantity=quantity)
            db.session.add(stock)
            db.session.commit()
            return render_template('add_stock.html', message='Stock added successfully!', alert_type='success')
        except Exception as e:
            return render_template('add_stock.html', message=f'Error adding stock: {str(e)}', alert_type='danger')

    return render_template('add_stock.html')

# Route to update fertilizer stock
@app.route('/update_stock/<int:id>', methods=['GET', 'POST'])
def update_stock(id):
    stock = FertilizerStock.query.get(id)

    if request.method == 'POST':
        # Update stock details
        stock.name = request.form['name']
        stock.category = request.form['category']
        stock.subcategory = request.form['subcategory']
        stock.price = float(request.form['price'])
        stock.quantity = int(request.form['quantity'])

        try:
            db.session.commit()
            return redirect(url_for('stock_list'))
        except Exception as e:
            return render_template('update_stock.html', stock=stock, message=f'Error updating stock: {str(e)}', alert_type='danger')

    return render_template('update_stock.html', stock=stock)


# Route to delete fertilizer stock
@app.route('/delete_stock/<int:id>')
def delete_stock(id):
    stock = FertilizerStock.query.get(id)

    try:
        db.session.delete(stock)
        db.session.commit()
        return redirect(url_for('stock_list'))
    except Exception as e:
        return render_template('stock_list.html', message=f'Error deleting stock: {str(e)}', alert_type='danger')


# Route to display the form to add customer details
@app.route('/add_customer', methods=['GET', 'POST'])
def add_customer():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        city = request.form['city']
        country = request.form['country']
        phone_number = request.form['phone_number']

        # Insert data into customer_details table
        customer = CustomerDetails(name=name, email=email, city=city, country=country, phone_number=phone_number)
        db.session.add(customer)
        db.session.commit()

    return render_template('add_customer.html')


# Route to display the list of fertilizer stock
@app.route('/stock_list')
def stock_list():
    search_term = request.args.get('search', '')

    if search_term:
        all_stock_items = FertilizerStock.query.all()

        # Filter items where any column contains the search term
        filtered_stock_list = [item for item in all_stock_items if any(search_term.lower() in col.lower() for col in [item.name, item.category, item.subcategory])]
    else:
        filtered_stock_list = FertilizerStock.query.all()

    return render_template('stock_list.html', stock_list=filtered_stock_list)





# Route to display the list of customer details
@app.route('/customer_list')
def customer_list():
    customer_list = CustomerDetails.query.all()
    return render_template('customer_list.html', customer_list=customer_list)


if __name__ == '__main__':
    app.run(debug=True)
