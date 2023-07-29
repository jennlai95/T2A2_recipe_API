from flask import Blueprint, request, jsonify
from init import db
from datetime import date 
from models.saved_recipe import SavedRecipe, saved_recipe_schema, saved_recipes_schema
from models.recipe import Recipe
from models.user import User
from flask_jwt_extended import get_jwt_identity, jwt_required
from psycopg2 import errorcodes
from sqlalchemy.exc import IntegrityError

#create recipes route 
saved_recipes_bp = Blueprint('saved_recipes',__name__, url_prefix='/saved_recipes')

@saved_recipes_bp.route('/', methods=['GET'])
@jwt_required()
def get_all_saved_recipes():
    current_user_id = get_jwt_identity()
    saved_recipes = SavedRecipe.query.filter_by(user_id=current_user_id).all()
    return saved_recipes_schema.dump(saved_recipes)
    
#Get one recipe and return error if recipe id doesn't exist
@saved_recipes_bp.route('/<int:id>', methods=['GET'])
@jwt_required()
def get_one_recipe(id):
    stmt = db.select(SavedRecipe).filter_by(id=id)
    SavedRecipe = db.session.scalar(stmt)
    if recipe:
       return saved_recipe_schema.dump(saved_recipes)
    else: 
       return {'error': f'saved recipes not found with id {id}'}, 404 

# #Create post method for recipe

@saved_recipes_bp.route('/', methods=['POST'])
@jwt_required()
def create_saved_recipe():
    try: 
        body_data = request.get_json()
        #create a new Recipe model instance 
        saved_recipe = SavedRecipe(
            date  = date.today(),
            user_id = get_jwt_identity(),
            recipe_id = body_data.get('recipe_id'),
        )
        # Add the recipe to the session
        db.session.add(saved_recipe)
        #Commit 
        db.session.commit()
        #return respond to the client
        return saved_recipe_schema.dump(saved_recipe), 201
    except IntegrityError as err:
        if err.orig.pgcode == errorcodes.NOT_NULL_VIOLATION:
            return {'error': 'The  is required'}, 409

#Delete method for recipe, requires recipe id to delete and user loging

@saved_recipes_bp.route('/<int:id>', methods = ['DELETE'])
@jwt_required()
def delete_one_saved_recipe(id):
    stmt = db.select(saved_recipe).filter_by(id=id)
    saved_recipe = db.session.scalar(stmt)
    if saved_reciperecipe: 
        db.session.delete(saved_recipe)
        db.session.commit()
        return {'message': f'saved_recipe  deleted successfully'}
    else: 
        return {'error': f'Recipe not found with id {id}'}, 404

# #create put and patch method, editing method
# @saved_recipes_bp.route('/<int:id>', methods = ['PUT','PATCH'])
# @jwt_required()   
# def update_one_saved_recipe(id):
#     body_data = request.get_json()
#     stmt = db.select(SavedRecipeRecipe).filter_by(id=id)
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
