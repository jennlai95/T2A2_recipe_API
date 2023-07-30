from flask import Blueprint, request, jsonify
from init import db
from datetime import date 
from models.saved_recipe import SavedRecipe, saved_recipe_schema, saved_recipes_schema
from models.recipe import Recipe
from models.user import User
from flask_jwt_extended import get_jwt_identity, jwt_required
from psycopg2 import errorcodes
from sqlalchemy.exc import IntegrityError

#create recipes route   - database_bp = Blueprint ('database_name',__name__, url_prefix = '/endpoint url name')
saved_recipes_bp = Blueprint('saved_recipes',__name__, url_prefix='/saved_recipes')

@saved_recipes_bp.route('/', methods=['GET'])
@jwt_required()
def get_all_saved_recipes():
    current_user_id = get_jwt_identity()
    saved_recipes = SavedRecipe.query.filter_by(user_id=current_user_id).all()
    return saved_recipes_schema.dump(saved_recipes)
    
#Get one saved recipe and return error if saved recipe id doesn't exist
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
            status = body_data.get('status'),
        )
        # Add the recipe to the session
        db.session.add(saved_recipe)
        #Commit 
        db.session.commit()
        #return respond to the client
        return saved_recipe_schema.dump(saved_recipe), 201
    except IntegrityError as err:
        if err.orig.pgcode == errorcodes.NOT_NULL_VIOLATION:
            return {'error': f'The {err.orig.diag.column_name} is require'}, 409

#Delete method for recipe, requires recipe id to delete and user loging

@saved_recipes_bp.route('/<int:id>', methods = ['DELETE'])
@jwt_required()
def delete_one_saved_recipe(id):
    stmt = db.select(SavedRecipe).filter_by(id=id)
    saved_recipe = db.session.scalar(stmt)
    if saved_recipe: 
        if str (saved_recipe.user_id) != get_jwt_identity():
            return {'error': 'Only the owner of the saved recipe list can edit'}, 403       
        db.session.delete(saved_recipe)
        db.session.commit()
        return {'message': f'Saved recipe no. {saved_recipe.id} deleted successfully'}
    else: 
        return {'error': f'Saved Recipe not found with id {id}'}, 404

#create put and patch method, editing method
@saved_recipes_bp.route('/<int:id>', methods = ['PUT','PATCH'])
@jwt_required()   
def update_one_saved_recipe(id):
    body_data = saved_recipe_schema.load(request.get_json())
    stmt = db.select(SavedRecipe).filter_by(id=id)
    saved_recipe = db.session.scalar(stmt)
    if saved_recipe:
        # check user id as only original user can update saved list
        if str (saved_recipe.user_id) != get_jwt_identity():
            return {'error': 'Only the owner of the saved recipe list can edit'}, 403
        saved_recipe.recipe_id = body_data.get('recipe_id') or saved_recipe.recipe_id
        saved_recipe.status = body_data.get('status') or saved_recipe.status
        saved_recipe.date = date.today()

        db.session.commit()
        return saved_recipe_schema.dump(saved_recipe)
    else:
        return {'error': f'Saved recipe not found with id {id}'}, 404
