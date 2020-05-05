from data import load_data_from_json_file
from matsmart import get_available_items

"""
Super-rudimentary testing, invoke as module;
    python -m test
Returns "Passed" if the get_available_items_json result corresponds to the saved test_results.json
"""

# test_item_list = ["bovete", "chia", "matvete", "quinoa", "havregryn"]


def ordered(obj):
    if isinstance(obj, dict):
        return sorted((k, ordered(v)) for k, v in obj.items())
    if isinstance(obj, list):
        return sorted(ordered(x) for x in obj)
    else:
        return obj


def test_available_result():
    test_result = get_available_items(as_dict=True)
    correct_result = load_data_from_json_file(filename="test_data/results.json")
    assert ordered(test_result) == ordered(correct_result), "Should be same result"


if __name__ == "__main__":
    test_available_result()
    print("Passed")
