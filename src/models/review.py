from init import db, ma 
from marshmallow import fields 


#Create reviews model
class Review(db.model):
    __tablename__ = "reviews"
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    comment = db.Column(db.Text)
    date = db.Column(db.Date) # Date created
    user_rating = db.Column(db.Integer)
    
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    
    user = db.relationship('User', back_populates='comments')
    
    recipes = db.relationship('Recipe', back_populates='user')
    recipe_id = db.Column(db.Integer, db.ForeignKey('recipes.id'), nullable=False)
    
class CommentSchema(ma.Schema):
    user = fields.Nested('UserSchema', only=['name','email'])
    recipe = fields.Nested('RecipeSchema', only=['title'])
    
    class Meta:
        fields = ('id','title','comment','date','user_rating','user_id')
        ordered = True

comment_schema = CommentSchema()
comments_schema = CommentSchema(many=true)