from init import db, ma 
from marshmallow import fields, validates
from marshmallow.validate import Length, And, Regexp, OneOf
from marshmallow.exceptions import ValidationError

#field validation for saved_recipe
VALID_STATUSES = ("To Try","Tried")

# create saved recipes to try list model
class SavedRecipe(db.Model):
    __tablename__ = 'saved_recipes'
    
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date) # Date created
    status = db.Column(db.String)
    # Recipe relationship
    recipe_id = db.Column(db.Integer, db.ForeignKey('recipes.id'), nullable=False)
    recipes = db.relationship('Recipe', back_populates='saved_recipes')
    
    #import user id relation/foreign key
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    user = db.relationship('User', back_populates='saved_recipes')
    
    
#create To_Try list Schema
class SavedRecipeSchema(ma.Schema):
    recipes = fields.Nested ('RecipeSchema', only = ['id','title'])
    user = fields.Nested ('UserSchema', only = ['name','email'])
    
    status = fields.String(validate=OneOf(VALID_STATUSES))
    
    @validates('status')
    def validate_status(self, value):
        if value == VALID_STATUSES[1]:
            stmt = db.select(db.func.count()).select_from(SavedRecipe).filter_by(status=VALID_STATUSES[1])
            count = db.session.scalar(stmt)
            # if there is an ongoing status saved or not
            if count > 0:
                raise ValidationError('You already have an ongoing status')
     
    class Meta:
        fields = ('id','date','recipe_id','user','status')
        ordered = True

saved_recipe_schema = SavedRecipeSchema()
saved_recipes_schema = SavedRecipeSchema(many=True)

