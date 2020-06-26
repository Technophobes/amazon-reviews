from model import dbconnect, Product, Reviewer, Review
from sqlalchemy import exc

def add_reviewer_from_queue(request_dict):
    session = dbconnect()
    try:
        product_instance = session.query(Product).filter(Product.id == request_dict["product_id"]).one()
    except:
        print("Product does not exist, please add it")
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


def add_review_from_queue(request_dict):
    session = dbconnect()
    try:
        reviewer_instance = session.query(Reviewer).filter(Reviewer.id == request_dict["reviewer_id"]).one()
    except:
        print("Reviewer does not exist, please add it")
    try:
        review = Review()
        review.helpful = request_dict["reviewerID"]  
        review.review_text = request_dict["reviewerName"]
        review.summary = request_dict["summary"]
        review.unix_review_time = request_dict["unixReviewTime"]
        review.review_time = request_dict["reviewTime"]
        review.reviewer = reviewer_instance
        session.add(review)
        session.commit()
        return review.id

    except exc.IntegrityError:
        session.rollback()
        return "already exists. something broken with q2 function."

  
