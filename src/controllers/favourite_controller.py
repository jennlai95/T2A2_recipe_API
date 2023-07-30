from flask import Blueprint, request, jsonify
from init import db
from datetime import date 
from models.favourite import Favourite, favourite_schema, favourites_schema
from models.recipe import Recipe
from models.user import User
from flask_jwt_extended import get_jwt_identity, jwt_required
from psycopg2 import errorcodes
from sqlalchemy.exc import IntegrityError

#create recipes route   - database_bp = Blueprint ('database_name',__name__, url_prefix = '/endpoint url name')
favourites_bp = Blueprint('favourites',__name__, url_prefix='/favourites')

@favourites_bp.route('/', methods=['GET'])
@jwt_required()
def get_all_favourites():
    current_user_id = get_jwt_identity()
    favourites = Favourite.query.filter_by(user_id=current_user_id).all()
    return favourites_schema.dump(favourites)
    
#Get one saved recipe and return error if saved recipe id doesn't exist
@favourites_bp.route('/<int:id>', methods=['GET'])
@jwt_required()
def get_one_recipe(id):
    stmt = db.select(Favourite).filter_by(id=id)
    Favourite= db.session.scalar(stmt)
    if recipe:
       return favourite_schema.dump(favourites)
    else: 
       return {'error': f'favourite not found with id {id}'}, 404 

# #Create post method for recipe

@favourites_bp.route('/', methods=['POST'])
@jwt_required()
def create_favourite():
    try: 
        body_data = request.get_json()
        #create a new favourite Recipe model instance 
        favourite =  Favourite(
            date  = date.today(),
            user_id = get_jwt_identity(),
            recipe_id = body_data.get('recipe_id')
        )
        # Add the recipe to the session
        db.session.add(favourite)
        #Commit 
        db.session.commit()
        #return respond to the client
        return favourite_schema.dump(favourite), 201
    except IntegrityError as err:
        if err.orig.pgcode == errorcodes.NOT_NULL_VIOLATION:
            return {'error': f'The {err.orig.diag.column_name} is require'}, 409

#Delete method for recipe, requires recipe id to delete and user loging

@favourites_bp.route('/<int:id>', methods = ['DELETE'])
@jwt_required()
def delete_one_favourite(id):
    stmt = db.select(Favourite).filter_by(id=id)
    favourite = db.session.scalar(stmt)
    if favourite: 
        # delete recipe from favourites list if you are the owner
        if str (favourite.user_id) != get_jwt_identity():
            return {'error': 'Only the owner of the  list can edit'}, 403       
        db.session.delete(favourite)
        db.session.commit()
        return {'message': f'favourite recipe no. {favourite.id} deleted successfully'}
    else: 
        return {'error': f'favourite recipe not found with id {id}'}, 404

#create put and patch method, editing method
@favourites_bp.route('/<int:id>', methods = ['PUT','PATCH'])
@jwt_required()   
def update_one_favourite(id):
    body_data = favourite_schema.load(request.get_json())
    stmt = db.select(Favourite).filter_by(id=id)
    favourite = db.session.scalar(stmt)
    if favourite:
        # check user id as only original user can update saved list
        if str (saved_recipe.user_id) != get_jwt_identity():
            return {'error': 'Only the owner of the saved recipe list can edit'}, 403
        favourite.recipe_id = body_data.get('recipe_id') or saved_recipe.recipe_id
        favourite.date = date.today()

        db.session.commit()
        return favourite_schema.dump(favourite)
    else:
        return {'error': f'Saved recipe not found with id {id}'}, 404
