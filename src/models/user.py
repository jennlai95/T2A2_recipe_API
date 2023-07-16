from init import db, ma 

#create User model
class User(db.model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    email = db.Column(db.String, nullable=False, unique=True)
    password = db.Column(db.String, nullable=False)

#create User Schema
class UserSchema(ma.Schema):
    class Meta:
        fields = ('id','name','email','password','is_admin')
        
user_schema = UserSchema(exclude=['password'])
users_schema = UserSchema(many=True, exclude=['password'])
