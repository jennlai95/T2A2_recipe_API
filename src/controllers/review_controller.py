from flask import Blueprint, request 
from init import db
from models.review import Review, review_schema, reviews_schema
from models.user import User
from models.recipe import Recipe
from datetime import date 
from flask_jwt_extended import get_jwt_identity, jwt_required

#create reviews route 
reviews_bp = Blueprint('reviews',__name__, url_prefix='/reviews')


#Get  review for recipe and return error if recipe id doesn't exist
@reviews_bp.route('/')
def get_all_review(recipe_id):
    stmt = db.select(Recipe).filter_by(id=recipe_id)
    review = db.session.scalar(stmt)
    if review:
       return review_schema.dump(review)
    else: 
       return {'error': f'Review not found with id {id}'}, 404 

# recipes/recipe_id/reviews - POST 
# Posting reviews under recipe id  
#Create post method for review

@reviews_bp.route('/', methods = ['POST'])
@jwt_required()
def create_review(recipe_id):
    body_data = request.get_json()
    stmt = db.select(Recipe).filter_by(id=recipe_id) #select * from recipes where id = recipe_id
    recipe = db.session.scalar(stmt)
    #create a new Review model instance 
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
def delete_review(recipe_id,review_id):
    stmt = db.select(Review).filter_by(id=review_id)
    recipe = db.session.scalar(stmt)
    if recipe: 
        db.session.delete(review)
        db.session.commit()
        return {'message': f'Review {review.title} deleted successfully'}
    else: 
        return {'error': f'Review not found with id {id}'}, 404

#create put and patch route, editing method
@reviews_bp.route('/<int:review_id>', methods = ['PUT','PATCH'])
@jwt_required()   
def update_review(recipe_id,review_id):
    body_data = request.get_json()
    stmt = db.select(Review).filter_by(id=review_idid)
    recipe = db.session.scalar(stmt)
    if review:
        review.title = body_data.get('title') or review.title 
        review.comment = body_data.get('comment') or recipe.comment
        review.user_rating = body_data.get('user_rating') or recipe.user_rating
        db.session.commit()
        return review_schema.dump(review)
    else:
        return {'error': f'Review not found with id {id}'}, 404
        