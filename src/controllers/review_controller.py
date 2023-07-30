from flask import Blueprint, request 
from init import db
from models.review import Review, review_schema, reviews_schema
from models.user import User
from models.recipe import Recipe
from datetime import date 
from flask_jwt_extended import get_jwt_identity, jwt_required
import functools

#create reviews route -  database_bp = Blueprint ('database_name',__name__, url_prefix = '/endpoint url name')
reviews_bp = Blueprint('reviews',__name__, url_prefix='/reviews')

#create admin auth
def authorise_as_admin(fn):
    @functools.wraps(fn)
    def wrapper(*args, **kwargs):
        user_id = get_jwt_identity()
        stmt = db.select(User).filter_by(id=user_id)
        user = db.session.scalar(stmt)
        if user.is_admin:
            return fn(*args, **kwargs)
        else:
            return {'error': 'Not authorised to perform delete'}, 403     
    return wrapper

# GET all reviews for a recipe - needs recipe id
# recipes/recipe_id/reviews - GET 
@reviews_bp.route('/', methods = ['GET'])
def get_all_review(recipe_id):
    # filter all review by recipe id and give all reviews under the recipe id
    review = db.session.query(Review).filter_by(recipe_id=recipe_id)
    if review:
       return reviews_schema.dump(review)
    else: 
       return {'error': f'Review not found with id {id}'}, 404 

# recipes/recipe_id/reviews - POST 
# Posting reviews under recipe id  
#Create post method for review

@reviews_bp.route('/', methods = ['POST'])
@jwt_required()
def create_review(recipe_id):
    body_data = review_schema.load(request.get_json())
    stmt = db.select(Recipe).filter_by(id=recipe_id) #select * from recipes where id = recipe_id
    recipe = db.session.scalar(stmt)
    #create a new Review instance if recipe exists
    if recipe: 
        review = Review(
            title = body_data.get('title'),
            comment = body_data.get('comment'),
            date  = date.today(),
            user_rating = body_data.get('user_rating'),
            user_id = get_jwt_identity(),
            recipe=recipe  # pass the model instance to the model field
        )
        # Add the review to the session
        db.session.add(review)
        #Commit 
        db.session.commit()
        #return respond to the client
        return review_schema.dump(review), 201
    else: 
        return {'error': f'Recipe not found with id {id}'}, 404


# Delete route for review, requires review id to delete and user login

@reviews_bp.route('/<int:review_id>', methods = ['DELETE'])
@jwt_required()
@authorise_as_admin
def delete_review(recipe_id,review_id):
    stmt = db.select(Review).filter_by(id=review_id)
    review = db.session.scalar(stmt)
    if review: 
        db.session.delete(review)
        db.session.commit()
        return {'message': f'Review {review.title} deleted successfully'}
    else: 
        return {'error': f'Review not found with id {id}'}, 404

#create put and patch route, editing method
@reviews_bp.route('/<int:review_id>', methods = ['PUT','PATCH'])
@jwt_required()   
def update_review(recipe_id,review_id):
    body_data = review_schema.load(request.get_json())
    stmt = db.select(Review).filter_by(id=review_id)
    review = db.session.scalar(stmt)
    if review:
        # check user id as only original user can update saved list
        if str (review.user_id) != get_jwt_identity():
            return {'error': 'Only the owner of the review can edit'}, 403
        review.title = body_data.get('title') or review.title 
        review.comment = body_data.get('comment') or review.comment
        review.user_rating = body_data.get('user_rating') or review.user_rating
        db.session.commit()
        return review_schema.dump(review)
    else:
        return {'error': f'Review not found with id {id}'}, 404
        