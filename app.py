import cv2
from pyzbar.pyzbar import decode
from flask import Flask, render_template,request,render_template, url_for,redirect,flash,session
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

app =Flask(__name__)
app.secret_key="thisissecreatkey"
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:sai@localhost:5432/inventory_management'

db= SQLAlchemy(app)
bcrypt = Bcrypt(app)

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    brand = db.Column(db.String(255))
    model = db.Column(db.String(255))
    price = db.Column(db.Numeric(10, 2))
    description = db.Column(db.Text)
    Qty=db.Column(db.Integer)
with app.app_context():
    db.create_all() 

class Customer(db.Model):
    customer_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    shop_name = db.Column(db.String(100))
    address = db.Column(db.Text)
with app.app_context():
    db.create_all() 

class Dispatch(db.Model):
    dispatch_id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
    customer_id = db.Column(db.Integer, db.ForeignKey('customer.customer_id'), nullable=False)
    qty_allocated = db.Column(db.Integer, nullable=False)
    dispatch_date = db.Column(db.TIMESTAMP, nullable=False, default=db.func.current_timestamp())

    # Define relationship with Product and Customer tables
    product = db.relationship('Product', backref=db.backref('dispatches', lazy=True))
    customer = db.relationship('Customer', backref=db.backref('dispatches', lazy=True))
with app.app_context():
    db.create_all() 

@app.route('/')
def index():
    
    dispatch_history=Dispatch.query.join(Product).join(Customer).all()
    return render_template('index.html',dispatch_history=dispatch_history)

@app.route('/start_scanner')
def start_scanner():
    cam = cv2.VideoCapture(0)
    cam.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    cam.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
    
    while True:
        success, frame = cam.read()
    
        if not success:
            print("Failed to capture frame")
            break
    
        for barcode in decode(frame):
            barcode_data = barcode.data.decode('utf-8')
            print("Barcode data:", barcode_data)  # Add this line to inspect barcode data
            data_lines = barcode_data.split('\n')
            print("Data lines:", data_lines) 
            Product_name=data_lines[0].split(': ')[1]
            brand = data_lines[1].split(': ')[1]
            model = data_lines[2].split(': ')[1]
            price = float(data_lines[3].split(': ')[1].replace('$', '').replace(',', ''))
            description = data_lines[4].split(': ')[1]
            print("Barcode type:", barcode.type)
            print("Barcode data:", barcode_data)
            
            # Close the scanner after scanning one product
            cam.release()
            cv2.destroyAllWindows()
            
            # Query the database to check if the product already exists
            product =Product.query.filter_by(name=Product_name).first()
            
            if product:
                # If the product exists, redirect to its product page
                return redirect(url_for('product', product_id=product.id))
            else:
                # If the product doesn't exist, create a new product entry
                new_product = Product(name=Product_name, brand=brand, model=model, price=price, description=description,Qty=0)
                db.session.add(new_product)
                db.session.commit()
                
                # Redirect to the newly created product's page
                return redirect(url_for('product', product_id=new_product.id))
        
        cv2.imshow("QR_code_scanner", frame)
    
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cam.release()
    cv2.destroyAllWindows()

    return ''

@app.route('/product/<int:product_id>',  methods=['GET', 'POST'])
def product(product_id):
    product = Product.query.get(product_id)
    shops = Customer.query.all()  # Retrieve all shops from the database
    if request.method == 'POST':
        quantity = int(request.form['quantity'])
        if product:
            product.Qty += quantity
            db.session.commit()
        return redirect(url_for('product', product_id=product_id))
    else:
        # Render the product page with its details
        if product:
            return render_template('product.html', product=product, shops=shops)
        else:
            # If the product doesn't exist, return a 404 error
            return 'Product not found', 404


@app.route('/product_list')
def product_list():
    products = Product.query.all()
    return render_template('product_list.html', products=products)

 
@app.route('/dispatch_product', methods=['POST'])
def dispatch_product():
    if request.method == 'POST':
        product_id = int(request.form['product_id'])
        quantity = int(request.form['quantity'])
        shop_id = int(request.form['shop'])

        # Retrieve the product and shop from the database
        product = Product.query.get(product_id)
        shop = Customer.query.get(shop_id)

        if product and shop:
            # Decrease the quantity of the product from the inventory
            if product.Qty >= quantity:
                product.Qty -= quantity
                db.session.commit()
                
                # Add the dispatch entry to the Dispatch table
                new_dispatch = Dispatch(product_id=product_id, customer_id=shop_id, qty_allocated=quantity)
                db.session.add(new_dispatch)
                db.session.commit()
                flash(f'{quantity} units of {product.name} dispatched to {shop.name}')
            else:
                flash('Insufficient quantity in inventory')

    # Redirect back to the product page
    return redirect(url_for('product', product_id=product_id))


if __name__ == '__main__':
    app.run(debug=True) 