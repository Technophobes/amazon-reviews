import requests
import json
import pandas as pd


df = pd.read_csv('short.csv')


def wrangle(input_object):
    input_dict = input_object.to_dict()
    pload_product = {"asin": input_dict["asin"], "overall": input_dict["overall"]}

    product_request = requests.get("http://127.0.0.1:5000/product/{}".format(input_dict["asin"]))
    if product_request.status_code == 400:
        product_request = requests.post("http://127.0.0.1:5000/product" , json=pload_product)

    input_dict["product_id"] = product_request.text
    requests.post("http://127.0.0.1:5000/reviewer" , json=input_dict)



df.apply(wrangle, axis=1)
