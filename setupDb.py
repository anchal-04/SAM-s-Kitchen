from restaurant import db, app
from restaurant.models import Table, User, Item, Order


with app.app_context():
    db.drop_all()
    db.create_all()




 