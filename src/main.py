from flask import Flask 
import os 
from init import db, ma, bcrypt, jwt
from controllers.cli_controller import db_commands
from controllers.auth_controller import auth_bp
from controllers.recipe_controller import recipes_bp
from controllers.review_controller import reviews_bp
from controllers.saved_recipe_controller import saved_recipes_bp
from datetime import timedelta
from marshmallow.exceptions import ValidationError

def create_app():
    app = Flask(__name__)
    
    #app.config ['JSON_SORT_KEYS'] = FALSE 
    app.json.sort_keys = False 
    
    app.config["SQLALCHEMY_DATABASE_URI"]=os.environ.get("DATABASE_URL")
    app.config["JWT_SECRET_KEY"]=os.environ.get("JWT_SECRET_KEY")
    
    @app.errorhandler(ValidationError)
    def validation_error(err):
        return {'error': err.messages}, 400
    
    db.init_app(app)
    ma.init_app(app)
    bcrypt.init_app(app)
    jwt.init_app(app)
    
    app.register_blueprint(db_commands)
    app.register_blueprint(auth_bp)
    app.register_blueprint(recipes_bp)
    app.register_blueprint(reviews_bp)
    app.register_blueprint(saved_recipes_bp)
  
    
    return app