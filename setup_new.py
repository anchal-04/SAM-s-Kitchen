import json
from restaurant import db, app
from restaurant.models import Table, User, Item, Order


def load_data_from_json(filename):
    with app.app_context():
        with open(filename, 'r') as f:
            data = json.load(f)

        # Check if the JSON has a 'rows' key
        if 'rows' in data:
            for row in data['rows']:
                # Unpack the row data
                item_id, name, description, price, source, orderer, category = row

                item = Item(
                    item_id=item_id,
                    name=name.strip(),  # Remove any extra whitespace
                    description=description.strip(),
                    price=price,
                    source=source,
                    orderer=orderer,  # This will be None if null
                    category=category
                )
                db.session.add(item)

        # Commit after adding all items
        db.session.commit()
        print(f"Successfully loaded {len(data['rows'])} items.")


# Run the script
if __name__ == '__main__':
    load_data_from_json('schema_new_2.json')