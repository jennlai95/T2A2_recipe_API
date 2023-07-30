from init import db, ma 
from marshmallow import fields 

#create User model
class User(db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    email = db.Column(db.String, nullable=False, unique=True)
    password = db.Column(db.String, nullable=False)
    is_admin = db.Column(db.Boolean, default=False)
    
    #Establish relation ('Model name', backpopulates='field')
    recipes = db.relationship('Recipe', back_populates='user')
    reviews = db.relationship('Review', back_populates='user', cascade ='all,delete')
    #create saved recipe relation
    saved_recipes = db.relationship('SavedRecipe', back_populates='user', cascade ='all,delete')
    #create favourites list relation
    favourites = db.relationship('Favourite',back_populates='user', cascade ='all,delete') 

#create User Schema
class UserSchema(ma.Schema):
    recipes = fields.List(fields.Nested('RecipeSchema',exclude=['user']))
    reviews = fields.List(fields.Nested('ReviewSchema',exclude=['user']))
    saved_recipes = fields.List(fields.Nested('SavedRecipeSchema'))
    favourites = fields.List(fields.Nested('FavouriteSchema'))
    
    class Meta:
        fields = ('id','name','email','password','is_admin')
        
user_schema = UserSchema(exclude=['password'])
users_schema = UserSchema(many=True, exclude=['password'])
