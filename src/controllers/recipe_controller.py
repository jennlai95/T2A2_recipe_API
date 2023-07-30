from flask import Blueprint, request 
from init import db
from models.recipe import Recipe, recipe_schema, recipes_schema
from models.review import Review, review_schema, reviews_schema
from flask_jwt_extended import get_jwt_identity, jwt_required
from controllers.review_controller import reviews_bp
from psycopg2 import errorcodes
from sqlalchemy.exc import IntegrityError

#create recipes route 
recipes_bp = Blueprint('recipes',__name__, url_prefix='/recipes')
recipes_bp.register_blueprint(reviews_bp,url_prefix ='<int:recipe_id>/reviews')

#create route to retrieve all recipes 
@recipes_bp.route('/', methods = ['GET'])
def get_all_recipes():
    stmt = db.select(Recipe).order_by(Recipe.difficulty_rating.desc())
    recipes = db.session.scalars(stmt)
    return recipes_schema.dump(recipes)

#Get one recipe and return error if recipe id doesn't exist
@recipes_bp.route('/<int:id>', methods = ['GET'])
def get_one_recipe(id):
    stmt = db.select(Recipe).filter_by(id=id)
    recipe = db.session.scalar(stmt)
    if recipe:
       return recipe_schema.dump(recipe)
    else: 
       return {'error': f'Recipe not found with id {id}'}, 404 

#Create post method for recipe

@recipes_bp.route('/', methods=['POST'])
@jwt_required()
def create_recipe():
    try: 
        body_data = request.get_json()
        #create a new Recipe model instance 
        recipe = Recipe(
            title = body_data.get('title'),
            description = body_data.get('description'),
            ingredients = body_data.get('ingredients'),
            cooking_time = body_data.get('cooking_time'),
            difficulty_rating = body_data.get('difficulty_rating'),
            user_id = get_jwt_identity()
        )
        # Add the recipe to the session
        db.session.add(recipe)
        #Commit 
        db.session.commit()
        #return respond to the client
        return recipe_schema.dump(recipe), 201
    except IntegrityError as err:
        if err.orig.pgcode == errorcodes.NOT_NULL_VIOLATION:
            return {'error': f'The {err.orig.diag.column_name} is required'}, 409

#Delete method for recipe, requires recipe id to delete and user loging

@recipes_bp.route('/<int:id>', methods = ['DELETE'])
@jwt_required()
def delete_one_recipe(id):
    stmt = db.select(Recipe).filter_by(id=id)
    recipe = db.session.scalar(stmt)
    #if recipe exists then delete and if not return 404 error
    if recipe: 
        db.session.delete(recipe)
        db.session.commit()
        return {'message': f'Recipe {recipe.title} deleted successfully'}
    else: 
        return {'error': f'Recipe not found with id {id}'}, 404

#create put and patch method, editing method, uses existing data if no new data is inputted
@recipes_bp.route('/<int:id>', methods = ['PUT','PATCH'])
@jwt_required()   
def update_one_recipe(id):
    body_data = request.get_json()
    stmt = db.select(Recipe).filter_by(id=id)
    recipe = db.session.scalar(stmt)
    if recipe:
        recipe.title = body_data.get('title') or recipe.title 
        recipe.description = body_data.get('description') or recipe.description
        recipe.ingredients = body_data.get('ingredients') or recipe.ingredients
        recipe.cooking_time = body_data.get('cooking_time') or recipe.cooking_time
        recipe.difficulty_rating = body_data.get('difficulty_rating') or recipe.difficulty_rating
        db.session.commit()
        return recipe_schema.dump(recipe)
    else:
        return {'error': f'Recipe not found with id {id}'}, 404
