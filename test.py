from data import load_data
from matsmart import get_available_items_json

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
    test_result = get_available_items_json()
    correct_result = load_data(filename="test_data/results.json")
    assert ordered(test_result) == ordered(correct_result), "Should be same result"


if __name__ == "__main__":
    test_available_result()
    print("Passed")
