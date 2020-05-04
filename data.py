import api
import json
import sys
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


def get_or_load_data(filename, getter_func, getter_func_args=[], allow_saved_data=True):
    data = None
    if sys.modules[__name__] == "test":
        filename = "test_data/" + filename
    if path.exists(filename) and allow_saved_data:
        data = load_data(filename)
    else:
        data = getter_func(*getter_func_args)
        save_data(filename, data)
    return data


def get_all_products(allow_saved_data=True):
    filename = "products.json"
    getter_func = api.get_all_products
    products = get_or_load_data(
        filename, getter_func, allow_saved_data=allow_saved_data
    )
    return products


def get_products_from_ids(ids_list, allow_saved_data=True):
    filename = "interesting_items.json"
    getter_func = api.get_products_from_ids
    getter_func_args = [ids_list]
    products = get_or_load_data(
        filename, getter_func, getter_func_args, allow_saved_data
    )
    return products


def load_latest_available_items_dump():
    # Loads 'available_items_dump.json' into a json object
    # which is returned
    # NOTE: only used for testing purposes in repl
    with open("available_items_dump.json") as f:
        json_string = f.read()
        available_items = json.loads(json_string)
    return available_items
