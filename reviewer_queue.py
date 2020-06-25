from model import dbconnect, Product, Reviewer, Review
from sqlalchemy import exc

def add_reviewer_from_queue(request_dict):
    session = dbconnect()
    try:
        product_instance = session.query(Product).filter(Product.id == request_dict["product_id"]).one()
    except:
        print("Region does not exist, please add it")
    try:
        reviewer = Reviewer()
        reviewer.amazon_reviewerID = request_dict["reviewerID"]  
        reviewer.reviewer_name = request_dict["reviewerName"]
        reviewer.product = product_instance
        session.add(reviewer)
        session.commit()
        return reviewer.id

    except exc.IntegrityError:
        session.rollback()
        return "already exists. something broken with q function."
