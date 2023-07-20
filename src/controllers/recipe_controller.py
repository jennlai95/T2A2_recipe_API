from flask import Blueprint, request 
from init import db
from models.recipe import Recipe, recipe_schema, recipes_schema


recipes_bp = Blueprint('recipes',__name__, url_prefix='/recipes')

@recipes_bp.route('/')
def get_all_recipes():
    stmt = db.select(Recipe).order_by(Recipe.difficulty_rating.desc())
    recipes = db.session.scalars(stmt)
    return recipes_schema.dump(recipes)
