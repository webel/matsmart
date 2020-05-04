import api
import json
from os import path

###
# TODO: saved data check; if *.json older than 1 day, discard and get new data
##
def save_data(filename, json_object):
    with open(filename, "w") as f:
        json_string = json.dumps(json_object)
        f.write(json_string)


def load_data(filename):
    with open(filename, "r") as f:
        json_string = f.read()
        return json.loads(json_string)


def get_all_products(allow_saved_data=True):
    filename = "products.json"
    products = None
    if path.exists(filename) and allow_saved_data:
        products = load_data(filename)
    else:
        products = api.get_all_products()
        save_data(filename, products)

    return products


def get_products_from_ids(ids_list, allow_saved_data=True):
    filename = "interesting_items.json"
    interesting_items = None
    if path.exists(filename) and allow_saved_data:
        interesting_items = load_data(filename)
    else:
        interesting_items = api.get_products_from_ids(ids_list)
        save_data(filename, interesting_items)

    return interesting_items


def load_latest_available_items_dump():
    # Loads 'available_items_dump.json' into a json object
    # which is returned
    # NOTE: only used for testing purposes
    with open("available_items_dump.json") as f:
        json_string = f.read()
        available_items = json.loads(json_string)
    return available_items
