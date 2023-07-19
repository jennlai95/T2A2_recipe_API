from flask import Blueprint
from init import db, bcrypt
from models.user import User 
from models.recipe import Recipe

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
        )
    ]
    
    db.session.add_all(users)
    
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
        ]
    
    db.session.add_all(recipes)
    
    db.session.commit()
    
    print("Tables seeded")