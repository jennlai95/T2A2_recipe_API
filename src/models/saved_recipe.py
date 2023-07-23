from init import db, ma 
from marshmallow import fields 

# create saved recipes to try list model
class SavedRecipe(db.Model):
    __tablename__ = 'saved_recipes'
    
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date) # Date created
    
    # Recipe relationship
    recipe_id = db.Column(db.Integer, db.ForeignKey('recipes.id'), nullable=False)
    recipes = db.relationship('Recipe', back_populates='saved_recipes')
    #import user id relation/foreign key
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    user = db.relationship('User', back_populates='saved_recipes')
    
    
#create To_Try list Schema
class SavedRecipeSchema(ma.Schema):
    user = fields.List(fields.Nested('SavedRecipeSchema',exclude=['user']))
    
    class Meta:
        fields = ('id','date','recipes','user')

saved_recipe_schema = SavedRecipeSchema()
saved_recipes_schema = SavedRecipeSchema(many=True)

