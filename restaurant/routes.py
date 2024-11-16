from restaurant import app, api
from flask import jsonify, render_template, redirect, url_for, flash, request, session, Response
from restaurant.models import Table, User, Item, Order
from restaurant.forms import RegisterForm, LoginForm, OrderIDForm, ReserveForm, AddForm, OrderForm
from restaurant import db
from flask_login import login_user, logout_user, login_required, current_user

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
        print(" inside get")
        items = Item.query.all()
        print(f"Items fetched: {items}")
        print(" inside get 1", items)
        return render_template('menu.html', items = items, add_form = add_form)

#MENU PAGE
@app.route('/order', methods = ['GET', 'POST'])
@login_required
def order_page():
    add_form = AddForm()
    if request.method == 'POST':
        selected_item = request.form.get('selected_item') #get the selected item from the menu page
        s_item_object = Item.query.filter_by(name = selected_item).first()
        if s_item_object:
            s_item_object.assign_ownership(current_user) #assign ownership of the ordered item to the user
        
        return redirect(url_for('order_page'))
    
    if request.method == 'GET':
        print(" inside get")
        items = Item.query.all()
        print(f"Items fetched: {items}")
        print(" inside get 1", items)
        return render_template('order.html', items = items, add_form = add_form)

#CART PAGE
@app.route('/cart', methods = ['GET', 'POST'])
def cart_page():
    order_form = OrderForm()
    if request.method == 'POST':
        ordered_item = request.form.get('ordered_item') #get the ordered item(s) from the cart page
        o_item_object = Item.query.filter_by(name = ordered_item).first()
        order_info = Order(name = current_user.fullname,
                           address = current_user.address,
                           order_items = o_item_object.name ) 

        db.session.add(order_info)
        db.session.commit()

        o_item_object.remove_ownership(current_user)    
        #return congrats page on successfull order
        return redirect(url_for('congrats_page'))
    
    if request.method == 'GET':
        selected_items = Item.query.filter_by(orderer = current_user.id)#get items which user has added to the cart
        return render_template('cart.html', order_form = order_form, selected_items = selected_items)
@app.route('/payment', methods=['GET', 'POST'])
def payment_page():
    if request.method == 'POST':
        # Process payment details
        data = request.form
        first_name = data.get('first-name')
        last_name = data.get('last-name')
        phone_number = data.get('phone-number')
        email = data.get('email')
        visa_type = data.get('visa-type')
        card_type = data.get('card-type')
        card_number = data.get('card-number')
        name_on_card = data.get('name-on-card')
        cvv = data.get('cvv')
        
        # Add payment processing logic here (e.g., integrate with a payment gateway)
        return jsonify({
            'message': 'Payment processed successfully',
            'data': {
                'name': f'{first_name} {last_name}',
                'email': email,
                'visa_type': visa_type,
                'card_type': card_type
            }
        })
    
    return render_template('payment.html')

#CONGRATULATIONS PAGE
@app.route('/congrats')
def congrats_page():
    return render_template('congrats.html')   

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
    logout_user() #used to log out
    flash('You have been logged out!', category = 'info')
    return redirect(url_for("home_page")) 

#REGISTER PAGE
@app.route('/register', methods = ['GET', 'POST'])
def register_page():
    forml = LoginForm()
    form = RegisterForm() 
    #checks if form is valid
    if form.validate_on_submit():
         user_to_create = User(username = form.username.data,
                               fullname = form.fullname.data,
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


