import requests

api_products_url = "https://api.matsmart.se/api/v1.0/routes?market=SE"
api_product_url = (
    "https://api.matsmart.se/api/v1.0/product-displays/{}?market=SE&range=1200"
)


def process_request(request):
    if request.status_code == 200:
        json = request.json()
        return json["data"]
    raise Exception(request.reason)


def get_all_products():
    request = requests.get(api_products_url)
    return process_request(request)


def get_products_from_ids(ids_list):
    ids_string = ",".join(ids_list)
    url = api_product_url.format(ids_string)
    request = requests.get(url)
    return process_request(request)
