from init import db, ma 
from marshmallow import fields, validates
from marshmallow.validate import Length, And, Regexp, OneOf
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
    
    user_rating = fields.Integer(validate=OneOf(VALID_USER_RATINGS))
    
    
    @validates('user_rating')
    def validate_user_rating(self, value):
        print(self)
        if value == VALID_USER_RATINGS[3]:
            stmt = db.select(db.func.count()).select_from(Review).filter_by(status=VALID_USER_RATINGS[3])
            count = db.session.scalar(stmt)
            # if there is an ongoing review or not
            if count > 0:
                raise ValidationError('You already have an ongoing review rating')
    
    class Meta:
        fields = ('id','recipe','title','comment','date','user_rating','user')
        ordered = True

review_schema = ReviewSchema()
reviews_schema = ReviewSchema(many=True)