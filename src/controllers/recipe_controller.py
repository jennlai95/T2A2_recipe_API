from flask import Blueprint, request 
from init import db
from models.recipe import Recipe, recipe_schema, recipes_schema
from flask_jwt_extended import get_jwt_identity, jwt_required

#create recipes route 
recipes_bp = Blueprint('recipes',__name__, url_prefix='/recipes')

@recipes_bp.route('/')
def get_all_recipes():
    stmt = db.select(Recipe).order_by(Recipe.difficulty_rating.desc())
    recipes = db.session.scalars(stmt)
    return recipes_schema.dump(recipes)

#Get one recipe and return error if recipe id doesn't exist
@recipes_bp.route('/<int:id>')
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
    #r respond to the client
    return recipe_schema.dump(recipe), 201

#Delete method for recipe, requires recipe id to delete and user loging

@recipes_bp.route('/<int:id>', methods = ['DELETE'])
@jwt_required()
def delete_one_recipe(id):
    stmt = db.select(Recipe).filter_by(id=id)
    recipe = db.session.scalar(stmt)
    if recipe: 
        db.session.delete(recipe)
        db.session.commit()
        return {'message': f'Recipe {recipe.title} deleted successfully'}
    else: 
        return {'error': f'Recipe not found with id {id}'}, 404
    