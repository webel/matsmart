"""Check Matsmart for interesting items
:author: Evita Stenqvist
:year: 2020

Checks matsmart.se for items in interesting_item_list variable found in this document, 
when run as a module it returns a json containing the items with key value pairs from Matsmart's API.
"""

import json
import sys
from pandas import DataFrame
from data import get_all_products, get_products_from_ids, save_data

# Used for initial testing, exchange this for an excel document
# dumped in the same directory
test_item_list = ["bovete", "chia", "matvete", "quinoa", "havregryn"]
interesting_item_list = test_item_list

# The "latest incoming" products API call, indicates that exclude-from-list
# indeed should be respected regardless of category...
# ?market=SE&range=100&filter[exclude_from_list][value]=1&filter[exclude_from_list][operator]=!%3D&sort=-published


def is_available_item(item_row):
    """Checks if the item is available

    The item is available if it's: published, has status and atleast a category
    NOTE: There should be a corrolation between unavailable and "exclude-from-list",
    although a category seems to trump "exclude from list".

    :param item_row: The item to check availability for 
    :type item_row: object
    :returns: a boolean representing availability
    :rtype: bool
    """
    if (
        int(item_row["published"])
        and int(item_row["status"])
        and len(item_row["categories"])
    ):
        return any(int(product["stock"]) for product in item_row["products"])
    return False


def is_interesting_simplified_item(simplified_item_row):
    """Checks wether an item is an interesting item

    The item is interesting if it includes a subtext from the interesting_item_list.

    :param simplified_item_row: The simplified_item to check for interesting subtexts
    :type simplified_item: object
    :returns: a boolean representing if it's interesting
    :rtype: bool
    """
    if sys.modules[__name__] == "test":
        return any(item in simplified_item_row for item in test_item_list)
    return any(item in simplified_item_row for item in interesting_item_list)


def get_simplified_interesting_items_dataframe():
    """Get the simple item records from the products list

    A simple product record includes four keys, where 'alias' and 'id' are of interest.
    This function gets all the items of interest from the products.

    :returns: The simple records with interesting items
    :rtype: pandas.DataFrame
    """
    products = get_all_products()
    products_dataframe = DataFrame(products)
    products_dataframe.drop_duplicates("id", inplace=True)

    simplified_interesting_items_mask = products_dataframe["alias"].apply(
        is_interesting_simplified_item
    )
    return products_dataframe[simplified_interesting_items_mask]


def get_available_items_dataframe():
    """Get the available item records as a pandas DataFrame

    The products don't necessarily have to be available, this function returns those that are.

    :returns: The records with available items
    :rtype: pandas.DataFrame
    """
    simplified_interesting_items_dataframe = (
        get_simplified_interesting_items_dataframe()
    )
    interesting_items_ids = simplified_interesting_items_dataframe.id.to_list()

    interesting_items = get_products_from_ids(interesting_items_ids)
    interesting_items_dataframe = DataFrame(interesting_items)
    interesting_items_dataframe.drop_duplicates("id", inplace=True)

    available_items_mask = interesting_items_dataframe.apply(is_available_item, axis=1)
    available_items_dataframe = interesting_items_dataframe[available_items_mask]

    return available_items_dataframe


def get_available_items_dict():
    """Get the available item records as a dictionary

    :returns: The records with available items
    :rtype: dict
    """
    available_items_dataframe = get_available_items_dataframe()
    return available_items_dataframe.to_dict(orient="record")


if __name__ == "__main__":
    """Dumps an 'available_items.json' file in this directory"""
    available_items = get_available_items_dict()
    save_data("available_items.json", available_items)
