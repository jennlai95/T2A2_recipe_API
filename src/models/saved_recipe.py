from init import db, ma 
from marshmallow import fields 

# create saved recipes to try list model
class Saved_Recipe(db.Model):
    __tablename__ = 'saved_recipes'
    
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date) # Date created
    
    recipes = db.relationship('Recipe', back_populates='saved_recipes')
    #import user id relation/foreign key
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    user = db.relationship('User', back_populates='saved_recipes')
    
    
#create To_Try list Schema
class UserSchema(ma.Schema):
    recipes = fields.List(fields.Nested('RecipeSchema',exclude=['user']))
    class Meta:
        fields = ('id','date','recipes','user')

saved_recipe_schema = Saved_RecipeSchema()
saved_recipes_schema = Saved_RecipeSchema(many=True)

