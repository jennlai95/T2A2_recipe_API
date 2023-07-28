# R1 Identification of the problem you are trying to solve by building this particular app.

This app is a 

# R2 Why is it a problem that needs solving?

-

# R3 Why have you chosen this database system. What are the drawbacks compared to others?

This project will use PostgreSQL. 

# R4 Identify and discuss the key functionalities and benefits of an ORM

- 

# R5 Document all endpoints for your API
-
Register as user
POST: localhost:8080/auth/register

LOGIN
POST: localhost:8080/auth/login

GET recipes
GET: localhost:8080/recipes

To get individual recipes via recipe
GET: localhost:8080/recipes/(id)
e.g 
localhost:8080/recipes/5
for recipe id 5

only logged in users can post and create recipe
POST: localhost:8080/recipes
make sure to login 
on postman grab login token  and add to authorisation on post card, add bearer token.  paste the token
once done you can hit send to post/create a new recipe.

To Post a review will need to login, POST: localhost:8080/reviews
example: 
{
    "title": "Recipe 3 review update",
    "user_rating": "2",
    "comment": "recipe comment",
    "recipe_id": "2"
}


# R6 An ERD for your app




# R7 Detail any third party services that your app will use

This API project will be done in python. The third party services used is as follows:

SQLAlchemy
Flask from flask we are also importing JWT extended, Bcrypt
Marshmallow
Bcrypt 
Psycopg 
python-dotenv 

These libraries are imported and installed in requirements.txt

# R8 Describe your projects models in terms of the relationships they have with each other

- 

# R9 Discuss the database relations to be implemented in your application

The database relations that are going to be implemented are user model, recipe model, reviews model, saved recipe model (to try) and favourites model. This can be seen in the ERD. Each table will have a primary key (id) and a foreign key (FK) is used to relate the field when used in a different table. The foreign table will use the relation to source the field to the table. 

User table: 
- There is four relations as its used in all the tables. 
- Recipe - one to many. One user can create many recipes but a recipe can only relate to one user.
- Saved recipe list - one to many, one user can have one list with many recipes but the list can only have one user. 
- 

Recipe table:
- user 
- reviews = this is a many to many relation. Recipes can have multiple reviews and similarly, reviews can be done for multiple recipes 

Saved recipe table:
- user - one to one relationship, 
- recipe - one to many - one recipe can be in many different saved recipe table

reviews table:
- user - one to many. many users can have many reviews but each review can only relate to one user
- recipe - many to many, a recipe can have many reviews but each review is done for one recipe. 



# R10 Describe the way taskes are allocated and tracked in your project

Tasks are managed on Trello 
