from init import db, ma 
from marshmallow import fields 

#Create recipes model
class Recipe(db.Model):
    __tablename__ = "recipes"
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    description = db.Column(db.Text)
    ingredients = db.Column(db.Text)
    cooking_time = db.Column(db.Integer) 
    difficulty_rating = db.Column(db.Integer)
    
    #import user id relation/foreign key
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    user = db.relationship('User', back_populates='recipes')
    
    reviews = db.relationship('Review', back_populates='recipe')  
    
    saved_recipes = db.relationship('SavedRecipe',back_populates='recipes')  

#create recipe schema
class RecipeSchema(ma.Schema):
    user = fields.Nested('UserSchema', only=['name','email'])
    
    class Meta:
        fields = ('id','title','description','ingredients','cooking_time','difficulty_rating','user')
        ordered = True

recipe_schema = RecipeSchema()
recipes_schema = RecipeSchema(many=True)

