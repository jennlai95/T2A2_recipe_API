from init import db, ma 
from marshmallow import fields, validates
from marshmallow.validate import Length, And, Regexp, OneOf, Range
from marshmallow.exceptions import ValidationError

#field validation for recipe schema
VALID_RATINGS = ("1","2","3","4","5")

#Create recipes model
class Recipe(db.Model):
    __tablename__ = "recipes"
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    ingredients = db.Column(db.Text, nullable = False)
    cooking_time = db.Column(db.Integer) 
    difficulty_rating = db.Column(db.Integer)
    
    #import user id relation/foreign key
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    user = db.relationship('User', back_populates='recipes')
    
    #create reviews relations
    reviews = db.relationship('Review', back_populates='recipe')  
    #create saved recipe relation 
    saved_recipes = db.relationship('SavedRecipe',back_populates='recipes')  
    #create favourites list relation
    favourites = db.relationship('Favourite',back_populates='recipes')  

#create recipe schema
class RecipeSchema(ma.Schema):
    user = fields.Nested('UserSchema', only=['name','email'])
    reviews = fields.List(fields.Nested('ReviewSchema'),exclude = ['recipe'])
    
    #validate title 
    title = fields.String(required=True, validate=And(
        Length(min=2, error='Title must be at least 2 characters long'),
        Regexp('^[a-zA-Z0-9 ]+$', error='Only letters, spaces and numbers are allowed')
    ))
    
    #validate difficulty rating so it is within 1-5 range
    difficulty_rating = fields.Integer(validate=Range(min=1, max=5))
    
    @validates('difficulty_rating')
    def validate_difficulty_rating(self, value):
        if not 1 <= value <= 5:
            raise ValidationError('Difficulty rating must be an integer between 1 and 5.')
        
    class Meta:
        fields = ('id','title','description','ingredients','cooking_time','difficulty_rating','user')
        ordered = True

recipe_schema = RecipeSchema()
recipes_schema = RecipeSchema(many=True)

