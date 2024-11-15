import json
from restaurant import db, app
from restaurant.models import Table, User, Item, Order


def load_data_from_json(filename):
    with open(filename, 'r') as f:
        data = json.load(f)

    # Insert data into the User table
    for menu_data in data:
        item = Item(item_id=menu_data['item_id'], name=menu_data['name'],description=menu_data['description'],price=menu_data['price'],source=menu_data['source'],orderer=menu_data['orderer'])
        db.session.add(item)

    # Commit after adding users to ensure user IDs are generated
    db.session.commit()


load_data_from_json('schema.json')