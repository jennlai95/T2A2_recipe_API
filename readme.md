# T2A2 API webserver application - Jennifer Lai

https://github.com/jennlai95/T2A2_recipe_API


# Installation

Download or clone the folder from github

Start PostgreSQL server in the terminal

    sudo service PostgreSQL start on windows or linux

Connect to Postgresql database from flask application
    psql

Create a database recipe_mvc_db in PostgreSQL

    CREATE DATABASE recipe_mvc_db;

Create a role with password for example recipe_dev
    
    CREATE USER 'recipe_dev' WITH PASSWORD 'password';

Grant all privileges and schema to the user

    GRANT ALL PRIVILEGES ON DATABASE recipe_mvc_db TO recipe_dev;

    GRANT ALL ON SCHEMA public TO recipe_dev;



open another terminal to install a virtual environment

    cd src
    python3 -m .venv venv
    source .venv/bin/activate

install the required imports

    pip install -r requirements.txt

Create a .env file inside the src folder following the .envsample . for example:

    DATABASE_URL="postgresql+psycopg2://database_user_name:password@localhost:___/database name
                                                                    # port
                            
    JWT_SECRET_KEY="



once done you can connect to database from psql with user name

    \c "database name" "username";
    e.g
    \c recipe_mvc_db recipe_dev;

or from flask venv

    psql -U recipe_dev -h 127.0.0.1 -d recipe_mvc_db

Create and seed database inside the virtual environment

    flask db create
    flask db seed
    flask run

once done you can run this app on Postman to make requests

# R1 Identification of the problem you are trying to solve by building this particular app.

This app is a recipe API. It allows users to save recipes to try or to browse for new recipes. This keeps tracks of all the recipes that users have tried or want to try and also reviews each recipes if they wanted to. The main point is to also be able to share this with others so the users can expand the type of recipes they try.

This is a problem as there are sometimes many recipes to try but users are unable to keep track of which recipes they've tried or how they feel about the recipe once they've tried it

# R2 Why is it a problem that needs solving?

It needs to be solved as many times it is hard to keep track of each recipes and ingredients as there are multiple.

# R3 Why have you chosen this database system. What are the drawbacks compared to others?

This project will use PostgreSQL. I have chosen to use this relational database as it is one of the most popular RDBMs with many resources available to support and use the database management. 

PostgreSQL is a database commonly used in Flask applications. It is a relational database 
management system that is also ACID compliant. 

One of the pros of using PostgreSQL is that it is free and open source so it has a large active 
community of developers. This means that it is regularly updated and with new database system 
features. You can easily create new data, remove data or update the data on the 
database. Its features include foreign keys for linking data in two tables. It is also an in-demand
solution for web applications projects. It also has high performance and can support a 
wide range of data and scales well with large quantity of data. 

The con of this database is it is slow compared to another database. The installation is also 
complicated for beginners and the extensive resources and documentation are also mostly in English
which makes it less useful for non-English users. There is a learning curve to using PostgreSQL and even 
installing it may be difficult to do without documentation or guidance. Another con is the extensive 
memory usage because of the architecture of PostgreSQL. This means it requires
more server or hardware resources than other databases.

# R4 Identify and discuss the key functionalities and benefits of an ORM

- 

# R5 Document all endpoints for your API
Each models have CRUD endpoints (Create, Read, Update and delete endpoints). The request needs to be submitted in JSON. 
USER model endpoints: 

## AUTH_CONTROLLER endpoints:
- Register as user
HTTPS request verb: POST
ROUTE ('auth/register', methods = 'POST')
Example:POST: localhost:8080/auth/register
- this allows someone to sign up and create a new account with their username, email and password
- All the data is required and not nullable 

- LOGIN as user :
HTTPS request: POST /auth/login
Example =  POST: localhost:8080/auth/login
- this allows user to login using their email and password
- this returns a serialised JWT token used to authenticate other endpoints if successful 
- Error 401 will return if email or password is invalid during login


## Recipes endpoint:
- GET recipes
ROUTE ('/recipes', methods = ['GET'])
GET: /recipes e.g localhost:8080/recipes
required: user login to retrieve the data and JWT token cannot be expired

- To get individual recipes via recipe
GET: localhost:8080/recipes/(id)

    e.g 
    localhost:8080/recipes/5
    for recipe id 5

- POST/CREATE new recipes
required: only logged in users can post and create recipe
POST: localhost:8080/recipes
make sure to login 
on postman grab login token  and add to authorisation on post card, add bearer token.  paste the token
once done you can hit send to post/create a new recipe.

![Alt text](doc/post_recipe.png)


## REVIEWS  endpoint:
- To Post a review will need to login, 
ROUTE: POST: /reviews  e.g. localhost:8080/reviews
required: user id, recipe id and user_rating is required for a review

example: 
{
    "title": "Recipe 3 review update",
    "user_rating": 2,
    "comment": "recipe comment",
    "recipe_id": "2"
}

- UPDATE reviews
ROUTE: PUT OR PATCH
/recipes/recipe_id/reviews/review_id
required: needs to be original user to delete. requires review_id and user login

![Alt text](doc/review_update.png)

![Alt text](doc/rating_error.png)


- DELETE reviews
Route: DELETE /recipes/recipe_id/reviews/review_id
required: authorisation as admin to delete
if a regular user tried to delete
![Alt text](doc/delete_review.png)

admin can delete

![Alt text](doc/delete_review_admin.png)

## Saved recipe endpoint: 

- POST CREATE recipe
ROUTE: POST: (/saved_recipes)

Required: recipe_id, user_id is needed and needs to be posted in JSON
user needs to be loggged in to save a recipe and to save a recipe you need the recipe id.
Status is not required but if a status is inputted it needs to be "To Try" or "Tried", these are case sensitive
IF any other status is put in it will return a validation error below:

{
    "error": {
        "status": [
            "Must be one of: To Try, Tried."
        ]
    }
}

- READ saved recipe list
ROUTE: GET: /saved_recipes
Required: user login required to get the recipes
example of list of recipes

![GET saved recipe](/doc/getsavedrecipe.png)

- PUT or PATCH saved recipe list
ROUTE: PUT or PATCH: /saved_recipes/id

![Patch](doc/PATCH_saved_recipe.png)

- DELETE saved recipe
- user can delete certain recipe from their saved recipe list. only the owner can remove recipe from their list
- Required: user login
- ROUTE: DELETE: /saved_recipes/id

![Alt text](doc/delete_saved_recipe.png)
![Alt text](doc/delete_saved_recipe_notowner.png)

## Favourites list endpoints

- POST
ROUTE: /favourites  
method: 'POST'
REQUIRED: user id and recipe id are required
- UPDATE
ROUTE: /favourites/id
method: 'PUT' OR 'PATCH', 
REQUIRED: user id and recipe id are required
- GET 
ROUTE: /favourites  
method: 'GET'
REQUIRED: user id is required

- DELETE
ROUTE: /favourites/id
method: 'DELETE'
REQUIRED: user id and recipe id is required. only the owner of the list can delete a favourited recipe
![Alt text](doc/delete_favourite.png)

# R6 An ERD for your app

![Alt text](doc/updated_ERD.png)

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
- favourites list - one to many, one user can have one list with many recipes but the list can only have one user. 
- reviews - one to many. user can create many reviews but each review is linked to only one user

Recipe table:
- user - many to one. each recipe is linked to only one user but user can create many recipes
- reviews = this is a one to many relation. Recipes can have multiple reviews and similarly, reviews can be done for multiple recipes but each review is linked to one recipe only. 

Saved recipe table:
- user - one to one relationship, 
- recipe - one to many - one recipe can be in many different saved recipe table

reviews table:
- user - one to many. many users can have many reviews but each review can only relate to one user
- recipe - many to many, a recipe can have many reviews but each review is done for one recipe. 



# R10 Describe the way taskes are allocated and tracked in your project

Tasks are managed on Trello : https://trello.com/b/XYz6FNaD/t2a2-recipe-tracker-api


yellow tasks are reminders , purple tasks are related to endpoint documentations
All tasks are important and necessary but urgent tasks are prioritised by date 
DAY 1
![Alt text](./doc/trello_day1.png)

DAY 3
![Alt text](</doc/Day 3.png>)

Week 3
![Alt text](/doc/image.png)


