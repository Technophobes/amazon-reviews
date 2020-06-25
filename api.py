# This api will import data to the database

from flask import Flask
from flask import jsonify
from flask import request
from flask_cors import CORS
from model import dbconnect, Product, Reviewer, Review
from sqlalchemy import exc
from redis import Redis
from rq import Queue
from reviewer_queue import add_reviewer_from_queue


app = Flask(__name__)
CORS(app)
# https://python-rq.org/
q = Queue('reviewer', connection=Redis())


@app.route('/product', methods=['POST'])
def add_product():
    session = dbconnect()
    request_dict = request.get_json()
    try:
        product_instance = Product()
        product_instance.amazon_id = request_dict["asin"]
        product_instance.overall_rating = request_dict["overall"]
        session.add(product_instance)
        session.commit()
        return jsonify(product_instance.id)
    except exc.IntegrityError:
        session.rollback()
        return "already exists", 400


@app.route('/reviewer',  methods=['POST'])
def add_reviewer():
	session = dbconnect()
	request_dict = request.get_json()
	try:
		# Check if region is existing. Why are we doing this? We do nothing with the result.
		# Make sure that we dont try and add a station without a region
		product_instance = session.query(Product).filter(Product.id == request_dict["product_id"]).one()
	except exc.IntegrityError:
		return "region does not exist", 400
	# Add the data to the queue
	q.enqueue(add_reviewer_from_queue, request_dict)
	return "OK", 200

@app.route('/product/<search_term>', methods=['GET'])
def get_product(search_term):
	session = dbconnect()
	try:
		product_instance = session.query(Product).filter(Product.amazon_id == search_term).one()
		return jsonify(product_instance.id), 200
	except:
		return "Product doesn't exist in database", 400


# This provides the error message on the url
if __name__ == '__main__':

	app.run(debug=True)