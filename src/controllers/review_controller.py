from flask import Blueprint, request 
from init import db
from models.review import Review, review_schema, reviews_schema
from datetime import date 


#create reviews route 
reviews_bp = Blueprint('reviews',__name__, url_prefix='/reviews')

@reviews_bp.route('/')
def get_all_review():
    stmt = db.select(Review).order_by(date.desc())
    recipes = db.session.scalars(stmt)
    return reviews_schema.dump(reviews)
