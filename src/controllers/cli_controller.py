from flask import Blueprint
from init import db, bcrypt
from models.user import User 
from models.recipe import Recipe
from models.review import Review
from models.saved_recipe import SavedRecipe
from models.favourite import Favourite
from datetime import timedelta, date 

db_commands = Blueprint('db',__name__)

@db_commands.cli.command('create')
def create_db():
    db.create_all()
    print("Tables Created")

@db_commands.cli.command('drop')
def drop_db():
    db.drop_all()
    print("Tables dropped")

@db_commands.cli.command('seed')
def seed_db():
    users = [
        User(
            email='admin@admin.com',
            password=bcrypt.generate_password_hash('admin123').decode('utf-8'),
            is_admin=True
        ),
        User(
            name='User User1',
            email='user1@email.com',
            password=bcrypt.generate_password_hash('user1pw').decode('utf-8')
        ),
        
        User(
            name='User User2',
            email='user2@email.com',
            password=bcrypt.generate_password_hash('user2pw').decode('utf-8')
        )
    ]
    
    db.session.add_all(users)
    
    #create recipes to seed in recipes_bp
    recipes = [ 
            Recipe (
                title = 'Recipe 1',
                description = 'Recipe 1 description',
                ingredients = 'Ingredients 1',
                cooking_time = '45',
                difficulty_rating = '2',
                user=users[0],
            ),
            Recipe (
                title = 'Recipe 2',
                description = 'Recipe 2 description',
                ingredients = 'Ingredients 2',
                cooking_time = '20',
                difficulty_rating = '3',
                user=users[0],
            ),
            
             Recipe (
                title = 'Recipe 3',
                description = 'Recipe 3 description',
                ingredients = 'Ingredients 123',
                cooking_time = '30',
                difficulty_rating = '5',
                user=users[1],
            ),
        ]
    
    db.session.add_all(recipes)
     
    #Seed table with reviews
    reviews = [ 
            Review (
                title = 'Recipe 1 review',
                comment = 'lorem ipsum',
                date=date.today(),
                user_rating = '3',
                user=users[0],
                recipe=recipes[1],
            ),
            Review (
                title = 'Recipe 2 review',
                comment = 'lorem ipsum',
                date=date.today(),
                user_rating = '5',
                user=users[0],
                recipe=recipes[2],
            ),
            
            Review (
                title = 'Recipe 2 review',
                comment = 'lorem ipsum',
                date=date.today(),
                user_rating = '1',
                user=users[1],
                recipe=recipes[2],
            ),
        ]

    
    db.session.add_all(reviews)
    
    #Seed table with saved recipe for user 0
    saved_recipes = [
                SavedRecipe (
                    date=date.today(),
                    recipe_id = 3,
                    user_id = 3,
                    status = 'To Try',
                    
                ),
                
                SavedRecipe (
                    date=date.today(),
                    recipe_id = 2,
                    user_id = 2,
                    status = 'Tried',
                    
                ),
                
                SavedRecipe (
                    date=date.today(),
                    recipe_id = 3,
                    user_id = 2,
                    status = 'Tried',
                    
                ),
    ]
    db.session.add_all(saved_recipes)
    
    favourites = [
                Favourite (
                    date=date.today(),
                    recipe_id = 1,
                    user_id = 2,
                    
                ),
                
                Favourite (
                    date=date.today(),
                    recipe_id = 3,
                    user_id= 3,
                    
                ),
                
                Favourite (
                    date=date.today(),
                    recipe_id = 1,
                    user_id= 3,
                    
                ),
    ]
    
    db.session.add_all(favourites)
    
    db.session.commit()
    
    print("Tables seeded")