import requests
import json
import pandas as pd


df = pd.read_csv('short.csv')


def wrangle2(input_object):
    input_dict = input_object.to_dict()

    reviewer_request = requests.get("http://127.0.0.1:5000/reviewer/{}".format(input_dict["reviewerID"]))
    if reviewer_request.status_code == 400:
        reviewer_request = requests.post("http://127.0.0.1:5000/reviewer" , json=input_dict)

    input_dict["reviewer_id"] = reviewer_request.text
    requests.post("http://127.0.0.1:5000/review" , json=input_dict)



df.apply(wrangle2, axis=1)