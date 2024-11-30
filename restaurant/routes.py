from restaurant import app, api
from flask import jsonify, render_template, redirect, url_for, flash, request, session, Response
from restaurant.models import Table, User, Item, Order, Cart
from restaurant.forms import RegisterForm, LoginForm, OrderIDForm, ReserveForm, AddForm, OrderForm, PaymentForm
from restaurant import db
from flask_login import login_user, logout_user, login_required, current_user
from flask import Flask, render_template, request, flash, redirect, url_for
from flask_mail import Mail, Message
import uuid
mail = Mail(app)
@app.route('/')
#HOME PAGE
@app.route('/home')
def home_page(): 
    return render_template('index.html')

@app.route('/contact', methods=['GET', 'POST'])
def contact_page():
    if request.method == 'POST':
        # Get the form data
        name = request.form.get('name')
        number = request.form.get('number')
        email = request.form.get('email')
        reason = request.form.get('reason')
        message = request.form.get('message')


        try:
            # Send the email
            msg = Message(reason,sender='noreply@gmai.com', recipients=[email])
            msg.body=message
            mail.send(msg)
            flash('Your message has been sent successfully!', 'success')
        except Exception as e:
            flash(f'An error occurred while sending your message: {str(e)}', 'danger')

        # Optional: You can save the data to the database or handle it as needed
        print(f"Contact Form Submitted: Name: {name}, Number: {number}, Email: {email}, Reason: {reason}, Message: {message}")
        
        # Provide feedback to the user (e.g., flash a message)
        flash('Thank you for reaching out! We will get back to you soon.', category='success')
        
        # Redirect to the contact page or any other page
        return redirect(url_for('contact_page'))

    # Render the contact page for GET requests
    return render_template('contact.html')

#MENU PAGE
@app.route('/menu', methods = ['GET', 'POST'])
@login_required
def menu_page():
    add_form = AddForm()
    if request.method == 'POST':
        selected_item = request.form.get('selected_item') #get the selected item from the menu page
        s_item_object = Item.query.filter_by(name = selected_item).first()
        if s_item_object:
            s_item_object.assign_ownership(current_user) #assign ownership of the ordered item to the user
        
        return redirect(url_for('menu_page'))
    
    if request.method == 'GET':
        items = Item.query.all()
        return render_template('menu.html', items = items, add_form = add_form)

#MENU PAGE
@app.route('/order', methods = ['GET', 'POST'])
@login_required
def order_page():
    add_form = AddForm()
    if request.method == 'POST':
        selected_item = request.form.get('selected_item')  # get the selected item from the menu page
        s_item_object = Item.query.filter_by(name=selected_item).first()
        if s_item_object:
            s_item_object.assign_ownership(current_user)  # assign ownership of the ordered item to the user

        return redirect(url_for('order_page'))

    if request.method == 'GET':
        print(" inside get")
        items = Item.query.all()
        print(f"Items fetched: {items}")
        print(" inside get 1", items)
        return render_template('order.html', items=items, add_form=add_form)


#CART PAGE
@app.route('/cart', methods=['GET', 'POST'])
@login_required
def cart_page():
    # Find or create an active (unplaced) order for the user
    active_order = Order.query.filter_by(
        orderer=current_user.username,
        order_placed=0
    ).first()

    if not active_order:
        active_order = Order.create_order(current_user)

    error_message = None
    total_price=0
    if request.method == 'POST':
        # Check if cart is empty
        cart_items = Cart.query.filter_by(
            orderer=current_user.username,
            order_id=active_order.order_id
        ).all()

        if not cart_items:
            error_message = "Your cart is empty. Add items before placing an order."
            # Render the template with the error
            return render_template(
                'cart.html',
                cart_items=[],
                total_price=0,
                error_message=error_message
            )

        # Place the order
        success = Cart.place_order(current_user)

        if success:
            return redirect(url_for('payment_page'))
        else:
            error_message = "Unable to place order. Please check your cart."
            return render_template(
                'cart.html',
                cart_items=cart_items,
                total_price=sum(
                    (item.item_qty or 0) * (Item.query.get(item.item_id).price or 0)
                    for item in cart_items
                ),
                error_message=error_message
            )

    if request.method == 'GET':
        # Get cart items for the active order
        cart_items = Cart.query.filter_by(
            orderer=current_user.username,
            order_id=active_order.order_id
        ).all()

        # Attach item information to cart items
        for cart_item in cart_items:
            cart_item.item_info = Item.query.get(cart_item.item_id)

        # Calculate total price
        total_price = sum(
            item.item_qty * Item.query.get(item.item_id).price
            for item in cart_items
        ) if cart_items else 0

        return render_template(
            'cart.html',
            cart_items=cart_items,
            total_price=total_price,
            error_message = error_message
        )


@app.route('/cart/modify', methods=['POST'])
@login_required
def modify_cart():
    item_id = request.form.get('item_id')
    action = request.form.get('action')

    # Find the active (unplaced) order for the user
    active_order = Order.query.filter_by(
        orderer=current_user.username,
        order_placed=0
    ).first()

    if not active_order:
        return jsonify({'error': 'No active order found.'}), 400

    # Find the specific cart item
    cart_item = Cart.query.filter_by(
        orderer=current_user.username,
        item_id=item_id,
        order_id=active_order.order_id
    ).first()

    if not cart_item:
        return jsonify({'error': 'Item not found in your cart.'}), 400

    # Get the item details
    item = Item.query.get(item_id)
    if not item:
        return jsonify({'error': 'Item not found in database.'}), 400

    # Modify cart item quantity
    if action == 'increase':
        cart_item.increase_quantity(max_quantity=item.stock)
    elif action == 'decrease':
        if cart_item.item_qty <= 1:
            # If quantity is 1 or less, delete the cart item
            cart_item.delete_cart_item()
        else:
            cart_item.decrease_quantity()

    # Recalculate cart totals
    cart_items = Cart.query.filter_by(
        orderer=current_user.username,
        order_id=active_order.order_id
    ).all()

    total_items = sum(cart_item.item_qty for cart_item in cart_items)
    total_price = sum(
        cart_item.item_qty * Item.query.get(cart_item.item_id).price
        for cart_item in cart_items
    )

    return jsonify({
        'total_items': total_items,
        'total_price': total_price,
        'item_quantity': cart_item.item_qty if cart_item else 0
    })


@app.route('/cart/add_item', methods=['POST'])
@login_required
def add_to_cart():
    item_id = request.form.get('item_id')

    # Find or create an active order
    active_order = Order.query.filter_by(
        orderer=current_user.username,
        order_placed=0
    ).first()

    if not active_order:
        active_order = Order.create_order(current_user)

    # Check if item exists
    item = Item.query.get(item_id)
    if not item:
        return jsonify({'error': 'Item not found'}), 400

    # Check if item is already in cart
    existing_cart_item = Cart.query.filter_by(
        orderer=current_user.username,
        item_id=item_id,
        order_id=active_order.order_id
    ).first()

    if existing_cart_item:
        # If item exists, increase quantity
        existing_cart_item.increase_quantity(max_quantity=item.stock)
    else:
        # Create new cart item
        new_cart_item = Cart(
            orderer=current_user.username,
            item_id=item_id,
            order_id=active_order.order_id,
            item_qty=1
        )
        db.session.add(new_cart_item)

    db.session.commit()

    return jsonify({
        'message': 'Item added to cart successfully',
        'item_name': item.name
    })
@app.route('/payment', methods=['GET', 'POST'])
@login_required
def payment_page():
    payment_form = PaymentForm()
    if request.method == 'POST':
        # Get form data
        name = request.form.get('name')
        email = request.form.get('email')
        phone = request.form.get('number')
        card_number = request.form.get('card_number')
        expiry = request.form.get('expiry')
        cvv = request.form.get('cvv')
        street = request.form.get('street')
        city = request.form.get('city')
        state = request.form.get('state')
        zip_code = request.form.get('zip')

        # Generate a unique order ID
        order_id = str(uuid.uuid4())[:8].upper()  # Generates a short unique ID

        # Create an order record
        order_info = Order(
            order_id=order_id,
            name=current_user.username,
            address=f"{street}, {city}, {state} {zip_code}",
            order_items=", ".join(
                [item.name for item in Item.query.filter_by(orderer=current_user.id, in_cart=True).all()])
        )
        db.session.add(order_info)
        db.session.commit()

        # Send confirmation email
        try:
            msg = Message('Order Confirmation from Sam\'s Kitchen',
                          sender='noreply@samskitchen.com',
                          recipients=[email])
            msg.body = f"""
                Dear {name},

                Thank you for your order from Sam's Kitchen!

                Order Details:
                Order ID: {order_id}
                Total Items: {len(list(Item.query.filter_by(orderer=current_user.id, in_cart=True).all()))}

                We will process your order shortly. Please provide your Order ID or Phone number for pick-up.

                Thank you for choosing Sam's Kitchen!

                Best regards,
                Sam's Kitchen Team
                """
            mail.send(msg)
        except Exception as e:
            print(f"Error sending email: {e}")
            flash('Order confirmed, but email confirmation failed.', 'warning')

        # Clear the cart
        cart_items = Item.query.filter_by(orderer=current_user.id, in_cart=True).all()
        for item in cart_items:
            item.remove_from_cart()
            item.remove_ownership(current_user)

        # Store order ID in session for congrats page
        session['order_id'] = order_id

        flash('Payment processed successfully!', 'success')
        return redirect(url_for('congrats_page'))

    if request.method == 'GET':
        # Get items in cart for current user
        selected_items = Item.query.filter_by(orderer=current_user.id, in_cart=True)
        total_price = sum(item.price for item in selected_items)
        return render_template('payment.html', payment_form=payment_form, selected_items=selected_items,
                               total_price=total_price, fullname=current_user.fullname,
                               phone_number=current_user.phone_number)

    return render_template('payment.html')



#CONGRATULATIONS PAGE
@app.route('/congrats')
def congrats_page():
    order_id = session.get('order_id', 'N/A')
    return render_template('congrats.html', order_id=order_id)

#TABLE RESERVATION PAGE
@app.route('/table', methods = ['GET', 'POST'])
@login_required
def table_page():
    reserve_form = ReserveForm()
    #to get rid of 'confirm form resubmission' on refresh
    if request.method == 'POST':
        reserved_table = request.form.get('reserved_table')
        r_table_object = Table.query.filter_by(table = reserved_table).first()
        if r_table_object:
            r_table_object.assign_ownership(current_user) #set the owner of the table to the current logged in user
            # flash(f"Your table {{ r_table_object.table }} has been reserved successfully!")

        return redirect(url_for('table_page'))

    if request.method == 'GET':
        tables = Table.query.filter_by(reservee = None)
        return render_template('table.html', tables = tables, reserve_form = reserve_form)

#LOGIN PAGE
@app.route('/login', methods = ['GET', 'POST'])
def login_page():
    forml = LoginForm()
    form = RegisterForm()
    if forml.validate_on_submit():
        attempted_user = User.query.filter_by(username = forml.username.data).first() #get username data entered from sign in form
        if attempted_user and attempted_user.check_password_correction(attempted_password = forml.password.data): #to check if username & password entered is in user database
            login_user(attempted_user) #checks if user is registered 
            # flash(f'Signed in successfully as: {attempted_user.username}', category = 'success')
            return redirect(url_for('home_page'))
        else:
            print("inside else of login")
            flash('Username or password is incorrect! Please Try Again', category = 'danger') #displayed in case user is not registered
    return render_template('login.html', forml = forml, form = form)

#FORGOT PASSWORD
@app.route('/forgot', methods = ['GET', 'POST'])
def forgot():
    return render_template("forgot.html")

def return_login():
    return render_template("login.html")


#LOGOUT FUNCTIONALITY
@app.route('/logout')
def logout():
    # Clear user's cart items when logging out
    cart_items = Item.query.filter_by(orderer=current_user.id, in_cart=True).all()
    for item in cart_items:
        item.remove_from_cart()
        item.remove_ownership(current_user)

    logout_user()  # Flask-Login logout
    session.clear()  # Clear entire session
    return redirect(url_for('home_page'))

#REGISTER PAGE
@app.route('/register', methods = ['GET', 'POST'])
def register_page():
    forml = LoginForm()
    form = RegisterForm() 
    #checks if form is valid
    if form.validate_on_submit():
         user_to_create = User(username = form.username.data,
                               fullname = form.fullname.data,
                               email = form.email.data,
                               address = form.address.data,
                               phone_number = form.phone_number.data,
                               password = form.password1.data,)
         db.session.add(user_to_create)
         db.session.commit()
         login_user(user_to_create) #login the user on registration 
         return render_template("index.html")
        #  return redirect(url_for('verify'))
    # else:
    #     flash("Username already exists!")

    if form.errors != {}: #if there are not errors from the validations
        for err_msg in form.errors.values():
            flash(f'There was an error with creating a user: {err_msg}')
    return render_template('login.html', form = form, forml = forml)

#ORDER ID PAGE
@app.route('/order_id', methods = ['GET', 'POST'])
def track_page():
    orderid = OrderIDForm()
    # if request.method == "POST":
    if orderid.validate_on_submit:
        #check to see if order id matches
        valid_orderid = Order.query.filter_by( order_id = orderid.orderid.data ).first()
        if valid_orderid:
            return redirect(url_for('delivery'))
        else:
            flash('Your Order-ID is invalid! Please Try Again.', category = 'danger')

    return render_template('order-id.html', orderid = orderid)

#DELIVERY TRACKING PAGE
@app.route('/deliverytracking')
def delivery():
    return render_template('track.html')

#OTP VERIFICATION
@app.route("/verify", methods=["GET", "POST"])
def verify():
    country_code = "+91"
    phone_number = current_user.phone_number
    method = "sms"
    session['country_code'] = "+91"
    session['phone_number'] = current_user.phone_number

    api.phones.verification_start(phone_number, country_code, via=method)

    if request.method == "POST":
            token = request.form.get("token") #OTP user entered

            phone_number = session.get("phone_number")
            country_code = session.get("country_code")

            verification = api.phones.verification_check(phone_number,
                                                         country_code,
                                                         token)

            if verification.ok():
                # return Response("<h1>Your Phone has been Verified successfully!</h1>")
                return render_template("index.html")
            else:
                # return Response("<center><h1>Wrong OTP!</h1><center>")
                flash('Your OTP is incorrect! Please Try Again', category = 'danger')

    return render_template("otp.html")


