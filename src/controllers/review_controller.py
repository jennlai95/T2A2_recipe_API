from flask import Blueprint, request 
from init import db
from models.review import Review, review_schema, reviews_schema
from models.user import User
from controllers.recipe_controller import recipes_bp
from datetime import date 
from flask_jwt_extended import get_jwt_identity, jwt_required

#create reviews route 
reviews_bp = Blueprint('reviews',__name__, url_prefix='/reviews')

@reviews_bp.route('/')
def get_all_review():
    stmt = db.select(Review).order_by(Review.date.desc())
    reviews = db.session.scalars(stmt)
    return reviews_schema.dump(reviews)

#Get one review and return error if review id doesn't exist
@reviews_bp.route('/<int:id>')
def get_one_review(id):
    stmt = db.select(Review).filter_by(id=id)
    review = db.session.scalar(stmt)
    if review:
       return review_schema.dump(review)
    else: 
       return {'error': f'Review not found with id {id}'}, 404 
   
#Create post method for review

@reviews_bp.route('/', methods=['POST'])
@jwt_required()
def create_review():
    body_data = request.get_json()
    #create a new Review model instance 
    review = Review(
        title = body_data.get('title'),
        comment = body_data.get('comment'),
        date  = date.today(),
        user_rating = body_data.get('user_rating'),
        user_id = get_jwt_identity(),
        recipe_id = body_data.get('recipe_id')
    )
    
    # Add the review to the session
    db.session.add(review)
    #Commit 
    db.session.commit()
    #r respond to the client
    return review_schema.dump(review), 201

# #Delete method for recipe, requires recipe id to delete and user loging

# @recipes_bp.route('/<int:id>', methods = ['DELETE'])
# @jwt_required()
# def delete_one_recipe(id):
#     stmt = db.select(Recipe).filter_by(id=id)
#     recipe = db.session.scalar(stmt)
#     if recipe: 
#         db.session.delete(recipe)
#         db.session.commit()
#         return {'message': f'Recipe {recipe.title} deleted successfully'}
#     else: 
#         return {'error': f'Recipe not found with id {id}'}, 404

# #create put and patch method, editing method
# @recipes_bp.route('/<int:id>', methods = ['PUT','PATCH'])
# @jwt_required()   
# def update_one_recipe(id):
#     body_data = request.get_json()
#     stmt = db.select(Recipe).filter_by(id=id)
#     recipe = db.session.scalar(stmt)
#     if recipe:
#         recipe.title = body_data.get('title') or recipe.title 
#         recipe.description = body_data.get('description') or recipe.description
#         recipe.ingredients = body_data.get('ingredients') or recipe.ingredients
#         recipe.cooking_time = body_data.get('cooking_time') or recipe.cooking_time
#         recipe.difficulty_rating = body_data.get('difficulty_rating') or recipe.difficulty_rating
#         db.session.commit()
#         return recipe_schema.dump(recipe)
#     else:
#         return {'error': f'Recipe not found with id {id}'}, 404
        