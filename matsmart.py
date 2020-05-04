import json
import sys
from pandas import DataFrame
from data import get_all_products, get_products_from_ids


###
# TODO
# escape swedish letters
###

# Used for initial testing, exchange this for an excel document
# dumped in the same directory
test_item_list = ["bovete", "chia", "matvete", "quinoa", "havregryn"]
interesting_item_list = test_item_list


def is_available_item(item_row):
    # The item is available if it's: published, has status and atleast a category
    # NOTE: There could be a corrolation between unavailable and "exclude-from-list",
    # although a category seems to trump this column.
    if (
        int(item_row["published"])
        and int(item_row["status"])
        and len(item_row["categories"])
    ):
        return any(int(product["stock"]) for product in item_row["products"])
    return False


def is_interesting_simplified_item(simplified_item_row):
    if sys.modules[__name__] == "test":
        return any(item in simplified_item_row for item in test_item_list)
    return any(item in simplified_item_row for item in interesting_item_list)


def get_simplified_interesting_items_dataframe():
    products = get_all_products()
    products_dataframe = DataFrame(products)
    products_dataframe.drop_duplicates("id", inplace=True)

    simplified_interesting_items_mask = products_dataframe["alias"].apply(
        is_interesting_simplified_item
    )
    return products_dataframe[simplified_interesting_items_mask]


def get_available_items_dataframe():
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


def get_available_items_json():
    available_items_dataframe = get_available_items_dataframe()
    return available_items_dataframe.to_dict(orient="record")
