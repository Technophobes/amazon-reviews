from sqlalchemy import Integer, Column, String, Float, ForeignKey, UniqueConstraint, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relation, sessionmaker


Base = declarative_base()

# Product is the parent class of this data set
class Product(Base):
    __tablename__ = 'Product'
    id = Column(Integer, primary_key=True)
    amazon_id = Column(Integer, unique=True)
    overall_rating = Column(Float)

    def __repr__(self):
        return "<Product(amazon_id='%s')>" % (self.amazon_id)


class Reviewer(Base):
    __tablename__ = 'Reviewer'
    id = Column(Integer, primary_key=True)
    amazon_reviewerID = Column(Integer, unique=True)
    reviewer_name = Column(String)

    product = relation("Product", backref = "Reviewer")
    product_id = Column(Integer, ForeignKey('Product.id'))

    def __repr__(self):
        return "<Reviewer(amazon_reviewerID='%s')>" % (self.amazon_reviewerID)


class Review(Base):
    __tablename__ = 'Review'
    id = Column(Integer, primary_key=True)
    helpful = Column(String, unique=True)
    review_text = Column(String)
    summary = Column(String)
    unix_review_time = Column(Integer)
    review_time = Column(String)

    reviewer = relation("Reviewer", backref = "Review")
    reviewer_id = Column(Integer, ForeignKey('Reviewer.id'))

    def __repr__(self):
        return "<Review(summary='%s')>" % (self.summary)


# This provides the connection to the database
def dbconnect():
    engine = create_engine('sqlite:///amazon-reviews.db', echo=False)
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    return Session()