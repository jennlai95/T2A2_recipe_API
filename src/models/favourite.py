from init import db, ma 
from marshmallow import fields

# create favourites recipe list model
class Favourite(db.Model):
    __tablename__ = 'favourites'
    
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date) # Date created
    # Recipe relationship
    recipe_id = db.Column(db.Integer, db.ForeignKey('recipes.id'), nullable=False)
    recipes = db.relationship('Recipe', back_populates='favourites')
    
    #import user id relation/foreign key
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    user = db.relationship('User', back_populates='favourites')
    
    
#create favourites list Schema
class FavouriteSchema(ma.Schema):
    recipes = fields.Nested ('RecipeSchema', only = ['id','title'])
    user = fields.Nested ('UserSchema', only = ['name','email'])
     
    class Meta:
        fields = ('id','date','recipe_id','user',)
        ordered = True

favourite_schema = FavouriteSchema()
favourites_schema = FavouriteSchema(many=True)