"""Check Matsmart for interesting items
:author: Evita Stenqvist
:year: 2020

Checks matsmart.se for items in interesting_items variable found in this document, 
when run as a module it returns a json containing the items with key value pairs from Matsmart's API.
"""

import json
import sys
from pandas import DataFrame
from data import get_all_products, get_products_from_ids, save_data_to_json_file

# Used for initial testing, exchange this for an excel document
# dumped in the same directory
test_items = ["bovete", "chia", "matvete", "quinoa", "havregryn"]
interesting_items = test_items

# The "latest incoming" products API call, indicates that exclude-from-list
# indeed should be respected regardless of category...
# ?market=SE&range=100&filter[exclude_from_list][value]=1&filter[exclude_from_list][operator]=!%3D&sort=-published


def is_available_item(item):
    """Checks if the item is available

    The item is available if it's: published, has status and atleast a category
    NOTE: There should be a corrolation between unavailable and "exclude-from-list",
    although a category seems to trump "exclude from list".

    :param item: The item to check availability for 
    :type item: object
    :returns: a boolean representing availability
    :rtype: bool
    """
    if int(item["published"]) and int(item["status"]) and len(item["categories"]):
        return any(int(product["stock"]) for product in item["products"])
    return False


def is_interesting_simplified_item(simplified_item):
    """Checks wether an item is an interesting item

    The item is interesting if it includes a subtext from the interesting_items.

    :param simplified_item: The simplified_item to check for interesting subtexts
    :type simplified_item: object
    :returns: a boolean representing if it's interesting
    :rtype: bool
    """
    if sys.modules[__name__] == "test":
        return any(item in simplified_item for item in test_items)
    return any(item in simplified_item for item in interesting_items)


def get_simplified_interesting_items(as_dict=False):
    """Get the simple item records from the products list

    A simple product record includes four keys, where 'alias' and 'id' are of use.
    This function gets all the items of interest from the products.

    :param as_dict: Wether to return the records in a dictionary, instead of default DataFrame.
    :type as_dict: bool
    :returns: The simple records with interesting items
    :rtype: pandas.DataFrame (by default), dict
    """
    products = get_all_products()
    products_dataframe = DataFrame(products)
    products_dataframe.drop_duplicates("id", inplace=True)

    simplified_interesting_items_mask = products_dataframe["alias"].apply(
        is_interesting_simplified_item
    )
    simplified_interesting_items_dataframe = products_dataframe[
        simplified_interesting_items_mask
    ]
    if as_dict:
        return simplified_interesting_items_dataframe.to_dict(orient="record")
    return simplified_interesting_items_dataframe


def get_available_items(as_dict=False):
    """Get the available item records as a pandas DataFrame

    The products don't necessarily have to be available, this function returns those that are.
    :param as_dict: Wether to return the records in a dictionary, instead of default DataFrame.
    :type as_dict: bool
    :returns: The records with available items
    :rtype: pandas.DataFrame (by default), dict (if as_dict=True)
    """
    simplified_interesting_items_dataframe = get_simplified_interesting_items()
    interesting_items_ids = simplified_interesting_items_dataframe.id.to_list()

    interesting_items = get_products_from_ids(interesting_items_ids)
    interesting_items_dataframe = DataFrame(interesting_items)
    interesting_items_dataframe.drop_duplicates("id", inplace=True)

    available_items_mask = interesting_items_dataframe.apply(is_available_item, axis=1)
    available_items_dataframe = interesting_items_dataframe[available_items_mask]

    if as_dict:
        return available_items_dataframe.to_dict(orient="record")
    return available_items_dataframe


if __name__ == "__main__":
    """Dumps an 'available_items.json' file in this directory"""
    available_items = get_available_items(as_dict=True)
    save_data_to_json_file("available_items.json", available_items)
