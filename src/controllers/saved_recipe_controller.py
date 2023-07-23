from flask import Blueprint, request 
from init import db
from models.saved_recipe import SavedRecipe, saved_recipe_schema, saved_recipes_schema

#create recipes route 
saved_recipes_bp = Blueprint('saved_recipes',__name__, url_prefix='/saved_recipes')

@saved_recipes_bp.route('/')
def get_all_saved_recipes():
    stmt = db.select(Saved_Recipe).order_by(Recipe.desc())
    recipes = db.session.scalars(stmt)
    return recipes_schema.dump(saved_recipes)

#Get one recipe 
@saved_recipes_bp.route('/<int:id>')
def get_one_saved_recipe():
    stmt = db.select(Saved_Recipe).filter_by(id=id)
    recipes = db.session.scalars(stmt)
    return recipe_schema.dump(saved_recipe)
