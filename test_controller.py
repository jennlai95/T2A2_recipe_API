# @saved_recipes_bp.route('/')
# def get_all_saved_recipes():
#     stmt = db.select(Recipe).filter_by(id=recipe_id)
#     recipes = db.session.scalars(stmt)
#     return saved_recipe_schema.dump(saved_recipes)

# #Get one recipe 
# @saved_recipes_bp.route('/<int:id>')
# def get_one_saved_recipe():
#     stmt = db.select(SavedRecipe).filter_by(id=id)
#     recipes = db.session.scalars(stmt)
#     return saved_recipe_schema.dump(saved_recipes)



@saved_recipes_bp.route('/')
def get_all_saved_recipes():
    saved_recipes = SavedRecipe.query.all()
    return saved_recipes_schema.dump(saved_recipes)

# #Get one recipe 
# @saved_recipes_bp.route('/<int:id>')
# def get_one_saved_recipe(id):
#     saved_recipe = SavedRecipe.query.get(id)
#     if not saved_recipe:
#         return jsonify({'error': 'Saved recipe not found'}), 404
#     return saved_recipe_schema.dump(saved_recipe)

@saved_recipes_bp.route('/', methods=['POST'])
@jwt_required()
def save_recipe():
    user_id = get_jwt_identity()
    if user_id is None:
        return jsonify({'error': 'User ID not found in JWT token'}), 401

    body_data = request.get_json()
    recipe_id = body_data.get('recipe_id')

    if not recipe_id:
        return jsonify({'error': 'Recipe ID is required'}), 400

    # Check if the recipe exists in the database
    if not Recipe.query.get(recipe_id):
        return jsonify({'error': 'Recipe not found'}), 404

    # Check if the saved recipe already exists for this user
    if SavedRecipe.query.filter_by(user_id=user_id, recipe_id=recipe_id).first():
        return jsonify({'error': 'Recipe already saved'}), 409

    saved_recipe = SavedRecipe(user_id=user_id, recipe_id=recipe_id)
    db.session.add(saved_recipe)
    db.session.commit()

    return jsonify({'message': 'Recipe saved successfully'}), 201
   
saved_recipes_bp.route('/<int:saved_recipe_id>', methods = ['DELETE'])
@jwt_required()
def delete_saved_recipes():
    body_data = request.get_json()
    stmt = db.select(SavedRecipe).filter_by(id=saved_recipe_id) #select * from recipes where id = saved_recipe_id
    savedrecipes = db.session.scalar(stmt)
    if savedrecipe:
       db.session.delete(saved_recipe_id)
       db.session.commit()
       return {'message': f'Save recipe {savedrecipes.id} deleted successfully'}
    else: 
       return {'error': f'Recipe not found with id {id}'}, 404 