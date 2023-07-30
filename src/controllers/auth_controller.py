from flask import Blueprint, request
from init import db,bcrypt
from models.user import User, user_schema, users_schema
from flask_jwt_extended import create_access_token
from sqlalchemy.exc import IntegrityError
from psycopg2 import errorcodes
from datetime import timedelta
from flask_jwt_extended import get_jwt_identity, jwt_required

#  database_bp = Blueprint ('database_name',__name__, url_prefix = '/endpoint url name')
auth_bp = Blueprint('auth',__name__, url_prefix='/auth')

#Create register route for new users to create their user
@auth_bp.route('/register', methods=['POST'])
def auth_register():
    try: 
        body_data = request.get_json()
        
        # Create a new User model instance from the user info 
        user = User()
        user.name = body_data.get('name')
        user.email = body_data.get('email')
        if body_data.get('password'):
            user.password = bcrypt.generate_password_hash(body_data.get('password')).decode('utf-8')
        #Add the user to session
        db.session.add(user)
        #commit to add user to the database
        db.session.commit()
        #Respond to the client
        return user_schema.dump(user), 201
    except IntegrityError as err:
        if err.orig.pgcode == errorcodes.UNIQUE_VIOLATION:
            return {'error': 'Email Address already in user'}, 409
        if err.orig.pgcode == errorcodes.NOT_NULL_VIOLATION:
            return { 'error': f'The {err.orig.diag.column_name} is required' }, 409

# Create login route for users to login and to request JSON web token to autheticate
@auth_bp.route('/login', methods=['POST'])
def auth_login():
    body_data = request.get_json()
    # Find the user by email address
    stmt = db.select(User).filter_by(email=body_data.get('email'))
    user = db.session.scalar(stmt)
    # If user exists and password is correct the create token and return field
    if user and bcrypt.check_password_hash(user.password, body_data.get('password')):
        token = create_access_token(identity=str(user.id), expires_delta=timedelta(days=1))
        return { 'email': user.email, 'token': token, 'is_admin': user.is_admin }
    else:
        return { 'error': 'Invalid email or password' }, 401
    