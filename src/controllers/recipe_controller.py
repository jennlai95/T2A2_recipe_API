from flask import Blueprint, request 
from init import db
from models.recipe import Recipe, recipe_schema, recipes_schema

#create recipes route 
recipes_bp = Blueprint('recipes',__name__, url_prefix='/recipes')

@recipes_bp.route('/')
def get_all_recipes():
    stmt = db.select(Recipe).order_by(Recipe.difficulty_rating.desc())
    recipes = db.session.scalars(stmt)
    return recipes_schema.dump(recipes)

#Get one recipe 
@recipes_bp.route('/<int:id>')
def get_one_recipe():
    stmt = db.select(Recipe).filter_by(id=id)
    recipes = db.session.scalars(stmt)
    return recipe_schema.dump(recipe)
