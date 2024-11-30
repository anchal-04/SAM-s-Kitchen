from wtforms.validators import Length
from restaurant import db, login_manager
from restaurant import bcrypt
from flask_login import UserMixin
from sqlalchemy.sql import func

#used for logging in users
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

#USER TABLE
class User(db.Model, UserMixin):
    #consider changing id to user_id
    id = db.Column(db.Integer(), primary_key = True)
    username = db.Column(db.String(length = 30), nullable = False, unique = True)
    fullname = db.Column(db.String(length = 30), nullable = False)
    address = db.Column(db.String(length = 50), nullable = False)
    phone_number = db.Column(db.Integer(), nullable = False)
    password_hash = db.Column(db.String(length = 60), nullable = False)

    tables = db.relationship('Table', backref = 'reserved_user', lazy = True) # relationship with 'Table'
    items = db.relationship('Item', backref = 'ordered_user', lazy = True) # relationship with 'Item'
    orders = db.relationship('Order', backref = 'order-id_user', lazy = True) #relationship with 'Table')

    @property
    def password(self):
        return self.password
    
    #hashes the user's password
    @password.setter
    def password(self, plain_text_password):
        self.password_hash = bcrypt.generate_password_hash(plain_text_password).decode('utf-8')

    #verifies if the entered password in sign in form matches the user's password in the database
    def check_password_correction(self, attempted_password):
        return bcrypt.check_password_hash(self.password_hash, attempted_password)
        
#TABLE RESERVATION TABLE
class Table(db.Model):
    #consider changing id to table_id
    table_id = db.Column(db.Integer(), primary_key = True)
    table = db.Column(db.Integer(), nullable = False)
    time = db.Column(db.String(length = 20), nullable = False)
    date = db.Column(db.String(length = 20), nullable = False)
    accomodation = db.Column(db.Integer(), nullable = False)
    #suggestion: you might want to change 'owner' to 'reservee'
    reservee = db.Column(db.String(), db.ForeignKey('user.id'))  #used to store info regarding user's reserved table

    #function for assigning ownership to the user's reserved table
    def assign_ownership(self, user):
        self.reservee = user.fullname 
        db.session.commit()
# table1 = Table(table = 1, time = "10:00-11:00 am", date = "24/11/21", accomodation = 4)                
# table2 = Table(table = 2, time = "10:00-11:00 am", date = "24/11/21", accomodation = 4)        
# table3 = Table(table = 6, time = "11:00-12:00 am", date = "24/11/21", accomodation = 4)
# table4 = Table(table = 4, time = "11:00-12:00 am", date = "24/11/21", accomodation = 4)
# table5 = Table(table = 5, time = "12:00-01:00 am", date = "24/11/21", accomodation = 4)        
# table6 = Table(table = 5, time = "01:00-02:00 am", date = "24/11/21", accomodation = 4)        
# table7 = Table(table = 6, time = "01:00-02:00 am", date = "24/11/21", accomodation = 4)        
# table8 = Table(table = 8, time = "02:00-03:00 am", date = "24/11/21", accomodation = 4)        
# table9 = Table(table = 1, time = "03:00-04:00 am", date = "24/11/21", accomodation = 4)        
# table10 = Table(table = 2, time = "03:00-04:00 am", date = "24/11/21", accomodation = 4)        
# db.session.add(table

#MENU TABLE
class Item(db.Model):
    #consider changing id to item_id
    item_id = db.Column(db.Integer(), primary_key = True)
    name = db.Column(db.String(length = 30), nullable = False)
    description = db.Column(db.String(length = 50), nullable = False)
    price = db.Column(db.Integer(), nullable = False)
    source = db.Column(db.String(length = 30), nullable = False)
    #suggestion: you might want to change 'owner' to 'orderer'/ 'customer'
    orderer = db.Column(db.Integer(), db.ForeignKey('user.id'))  #used to store info regarding user's ordered item
    category = db.Column(db.String(length= 30), nullable = False)
    #function for assigning ownership to the user's selected item
    def assign_ownership(self, user):
        self.orderer = user.id
        db.session.commit()

    def remove_ownership(self, user):
        self.orderer = None
        db.session.commit()

#item1 = Item( name = "Barbecue Salad", description = "Delicious Dish", price = 200, source = "plate1.png" )
#item2 = Item( name = "Salad with Fish", description = "Delicious Dish", price = 150, source = "plate2.png" )
#item3 = Item( name = "Spinach Salad", description ="Delicious Dish" , price = 100, source = "plate3.png" )
#item4 = Item( name = "Fresh Salad", description = "Delicious Dish", price = 200, source = "salad.png" )
#item5 = Item( name = "Fried Noodles", description = "Delicious Dish", price = 200, source = "noodles.png" )
#item6 = Item( name = "Roasted Chicken", description = "Delicious Dish", price = 300, source = "chicken.png" )
#item7 = Item( name = "Cheese Pizza", description = "Delicious Dish", price = 200, source = "pizza.png" )
#item8 = Item( name = "Barbecue Salad", description = "Delicious Dish", price = 200, source = "plate1.png" )
#item9 = Item( name = "Salad with Fish", description = "Delicious Dish", price = 150, source = "plate2.png" )
#db.session.add(item


#ORDERS TABLE
class Order(db.Model):
    order_id = db.Column(db.Integer(), primary_key=True)
    orderer = db.Column(db.String(length=30), db.ForeignKey('user.username'))
    datetime = db.Column(db.DateTime(timezone=True), server_default=func.now())
    order_placed = db.Column(db.Integer(), nullable=False, default=0)

    @classmethod
    def create_order(cls, user):
        """
        Create a new order for a user

        :param user: User object
        :return: Created order object or None if failed
        """
        try:
            new_order = cls(
                orderer=user.username,
                order_placed=0  # Initial state is not placed
            )
            db.session.add(new_order)
            db.session.commit()
            return new_order
        except Exception as e:
            db.session.rollback()
            print(f"Error creating order: {e}")
            return None


class Cart(db.Model):
    cart_id = db.Column(db.Integer(), primary_key=True)
    orderer = db.Column(db.String(length=30), db.ForeignKey('user.username'))
    item_id = db.Column(db.String(length=30), db.ForeignKey('item.item_id'))
    order_id = db.Column(db.Integer(), db.ForeignKey('order.order_id'))
    item_qty = db.Column(db.Integer(), nullable=False, default=1)
    datetime = db.Column(db.DateTime(timezone=True), server_default=func.now())

    def increase_quantity(self, max_quantity=5):
        """Increase quantity of the cart item"""
        try:
            if self.item_qty < max_quantity:
                self.item_qty += 1
                db.session.commit()
            return self.item_qty
        except Exception as e:
            db.session.rollback()
            print(f"Error increasing quantity: {e}")
            return None

    def decrease_quantity(self):
        """Decrease quantity of the cart item"""
        try:
            if self.item_qty <= 1:
                db.session.delete(self)
            else:
                self.item_qty -= 1
            db.session.commit()
            return self.item_qty
        except Exception as e:
            db.session.rollback()
            print(f"Error decreasing quantity: {e}")
            return None

    def delete_cart_item(self):
        """
        Delete the current cart item

        :return: Boolean indicating success
        """
        try:
            db.session.delete(self)
            db.session.commit()
            return True
        except Exception as e:
            db.session.rollback()
            print(f"Error deleting cart item: {e}")
            return False
    @classmethod
    def place_order(cls, user):
        """
        Place an order for all items in the user's cart

        :param user: User object
        :return: Boolean indicating success
        """
        try:
            # Find the most recent unplaced order for the user
            order = Order.query.filter_by(
                orderer=user.username,
                order_placed=0
            ).order_by(Order.datetime.desc()).first()

            if not order:
                print("No active order found")
                return False

            # Check if cart has items
            cart_items = cls.query.filter_by(orderer=user.username, order_id=order.order_id).all()

            if not cart_items:
                print("Cart is empty")
                return False

            # Mark the order as placed
            order.order_placed = 1
            db.session.commit()

            return True
        except Exception as e:
            db.session.rollback()
            print(f"Error placing order: {e}")
            return False

    @classmethod
    def cleanup_unplaced_orders(cls, user):
        """
        Delete unplaced orders and their associated cart items

        :param user: User object
        :return: Number of orders deleted
        """
        try:
            # Find unplaced orders for the user
            unplaced_orders = Order.query.filter_by(
                orderer=user.username,
                order_placed=0
            ).all()

            order_count = len(unplaced_orders)

            # Delete cart items for these unplaced orders
            for order in unplaced_orders:
                cls.query.filter_by(
                    orderer=user.username,
                    order_id=order.order_id
                ).delete()

                # Delete the order itself
                db.session.delete(order)

            db.session.commit()
            return order_count
        except Exception as e:
            db.session.rollback()
            print(f"Error cleaning up unplaced orders: {e}")
            return 0

    @classmethod
    def get_user_orders(cls, user, placed_only=False):
        """
        Retrieve orders with their cart items for a specific user

        :param user: User object
        :param placed_only: If True, only return placed orders
        :return: List of orders with their items
        """
        try:
            # Base query for orders
            order_query = Order.query.filter_by(orderer=user.username)

            if placed_only:
                order_query = order_query.filter_by(order_placed=1)

            # Retrieve orders
            orders = order_query.order_by(Order.datetime.desc()).all()

            # Prepare orders with their items
            order_details = []
            for order in orders:
                # Get cart items for this order
                cart_items = cls.query.filter_by(
                    orderer=user.username,
                    order_id=order.order_id
                ).all()

                order_details.append({
                    'order': order,
                    'items': cart_items
                })

            return order_details
        except Exception as e:
            print(f"Error retrieving user orders: {e}")
            return []

