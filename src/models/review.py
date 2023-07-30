from init import db, ma 
from marshmallow import fields, validates
from marshmallow.validate import Length, And, Regexp, Range
from marshmallow.exceptions import ValidationError

#field validation for recipe schema
VALID_USER_RATINGS = ('1','2','3','4','5')

#Create reviews model
class Review(db.Model):
    __tablename__ = "reviews"
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    comment = db.Column(db.Text)
    date = db.Column(db.Date) # Date created
    user_rating = db.Column(db.Integer, nullable=False)
    
    # User relationship
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    user = db.relationship('User', back_populates='reviews') 

    # Recipe relationship
    recipe_id = db.Column(db.Integer, db.ForeignKey('recipes.id'), nullable=False)
    recipe = db.relationship('Recipe', back_populates='reviews')
    
class ReviewSchema(ma.Schema):
    user = fields.Nested('UserSchema', only=['name','email'])
    recipe = fields.Nested('RecipeSchema', only=['title'])
    
    #validate title 
    title = fields.String(required=True, validate=And(
        Length(min=2, error='Title must be at least 2 characters long'),
        Regexp('^[a-zA-Z0-9 ]+$', error='Only letters, spaces and numbers are allowed')
    ))
    
    #validate difficulty rating so it is within 1-5 range
    user_rating = fields.Integer(validate=Range(min=1, max=5))
    
    @validates('user_rating')
    def validate_user_rating(self, value):
        if not 1 <= value <= 5:
            raise ValidationError('User rating must be an integer between 1 and 5.')
        
    
    class Meta:
        fields = ('id','recipe','title','comment','date','user_rating','user')
        ordered = True

review_schema = ReviewSchema()
reviews_schema = ReviewSchema(many=True)