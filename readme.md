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

This app is a RESTFUL recipe API. It allows users to save recipes to try or to browse for new recipes. This keeps tracks of all the recipes that users have tried or want to try and also reviews each recipes if they wanted to. The main point is to also be able to share this with others so the users can expand the type of recipes they try.

This is a problem as there are sometimes many recipes to try but users are unable to keep track of which recipes they've tried or how they feel about the recipe once they've tried it. With this app, users can easily keep track of recipes they've tried or wish to try.

The idea is to create a user friendly recipe API so users can easily share their recipes with others. By allowing reviews on the apps, it will also create a community of users who are willing to try new recipes and explore. 

# R2 Why is it a problem that needs solving?

It needs to be solved users can find difficult to manage multiple recipes and ingredients. It also allows users to store the recipes in a database but by creating a RESTFUL API, even users who are not familiar with SQL can store and track their recipes to share with others.
This API aims to store the recipe in a centralised database and organise it according to reviews, track saved recipe lists to try and bookmark their favourite recipes. This API will hopefully allow users to broaden their recipes to try and to enjoy a wider range of cuisines. 

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
more server or hardware resources than other databases. However, with this application the data used is not extensive so this drawback is not severe. 

# R4 Identify and discuss the key functionalities and benefits of an ORM

ORM is Object Relational Mapping and is used to interact between application and a datbase. This lets users to interact with the database by using queries rather than in SQL. It connects to database server, generates query, fetches data and serialises password. 

Some of the benefits is that ORM can be used to connect to the application with the SQL code without having to rewrite the code.It also means that users do not need any SQL knowledge to use the ORM. ORM is also easier and more cost-effective to maintain over time as it automates object-to-table and table-to-object conversion. 

# R5 Document all endpoints for your API
Each models have CRUD endpoints (Create, Read, Update and delete endpoints). For any body data request, it needs to be submitted in JSON. 

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
- this returns a serialised JWT token used to authenticate other endpoints if successful, this is then used to authorise as bearer tokens for all other endpoints 
- Error 401 will return if email or password is invalid during login


## Recipes endpoint:
- GET recipes
ROUTE ('/recipes', methods = ['GET'])
GET: /recipes e.g localhost:8080/recipes
required: user login authorisation to retrieve the data and JWT token cannot be expired

- To get individual recipes via recipe
GET: localhost:8080/recipes/(id)

    e.g 
    localhost:8080/recipes/5
    for recipe id 5

- POST/CREATE new recipes
required: only logged in users can post and create recipe
ROUTE: ('/recipes', methods = ['POST'])
e.g.
POST: localhost:8080/recipes
- make sure to login 
on postman grab login token  and add to authorisation on post card, add bearer token.  paste the token
once done you can hit send to post/create a new recipe.

![Alt text](doc/post_recipe.png)

- DELETE recipes
required: user login, needs to be an admin to be able to delete and recipe id
ROUTE: ('/recipes', methods = ['DELETE'])

- UPDATE recipes
required: user login, needs to be original user/owner of recipe to update and recipe id
ROUTE: ('/recipes', methods = ['PUT', 'PATCH'])


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

![Alt text](doc/POST_rview.png)

- GET reviews, get all reviews available under one recipe
ROUTE: /recipes/recipe_id/reviews/
METHOD: GET
required: user login, recipe id to input into the route

![Alt text](doc/get_reviews.png)

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
required: needs user authentication to update the list

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

SQLAlchemy - this is an ORM tool to translate Flask queries into SQL so we can use the PostgreSQL database and exucute the CRUD functions

Flask JWT extended - this is a package that provides JWT (JSON Web Token) for flask applications. its used for authentication and acess control in the endpoints. It authenticates the users and when succesfully authenticated, it provides a serialised bearer token to protect endpoints

Flask Marshmallow - this is a Flask extension that is popular and used for serialisation and deserialisation. It is a tool that converts data from database table into JSON format that can be returned. This simplies data handling and responses. 

Flask Bcrypt - this allows us to encrypt and hash the passwords and securely store and manage user passwords. this provides a layer of security as the password is not stored in database as inputted but are all encrypted

Psycopg = Psycopg is the most popular PostgreSQL database adapter for the Python programming language. SQL queries are executed with the help of execute() method and command. 

python-dotenv - Python-dotenv reads key-value pairs from a .env file and can set them as environment variables. This allowed us to create .env and .flaskenv system files. This is usefulk in managing sensitive configuration information such as DATABASE_URI and JWT SECRET KEYS in this API. 

These libraries are imported and installed in requirements.txt

# R8 Describe your projects models in terms of the relationships they have with each other

There were five models created in this application: 
1. User model - this is the model for users and admins that uses this applicatio
2. Recipe model - this model has the information on recipes
3. Reviews model - this is a model that reviews recipes
4. Saved recipe model - this model is a list of saved recipes and status of each saved recipes
5. Favourite model - this model is a list of favourite recipes by the user

## User model
The primary key is id and referred to as user.id as a Foreign Key in other model. If the user is deleted it will cascade a deletion for reviews, saved recipe and favourite model

There is a one to many relation for user and recipe model. A user can create many recipes.

## Recipe model 

The primary key is id and is referred to as recipe.id as a Foreign key in other models. This model is related to all the other models. 
We have a one to many relationship with user. One user can create many recipes but each recipe can only relate to one user(owner)
We have a one to many relationship with reviews model. Each recipe can have many reviews but each review is only for one recipe. Client has to review each recipe individually

## Reviews model

The primary key is id. It uses two foreign keys constraints from: user model and recipe model. 
Each review is directly tied to a recipe_id. Each review requires a user_rating and each review is for only one recipe.

## Saved recipe model

The primary key is id. It uses two foreign keys constraints from: user model and recipe model (user_id and recipe_id)
It has the option to add status to the list if you've tried the recipe or want to try the recipe

## Favourite model

The primary key is id. It uses two foreign keys constraints from: user model and recipe model. 
This is similar to saved recipe model but does not have any other independent body data and is simply a list of favourite recipe. It requires user id and recipe id as the Foreign Keys in the table. Date is saved on the day the recipes are added to the table. If user or recipe is deleted it will also cascade through the favourite model. 



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

Favourite table:
- user - one to one relationship, 
- recipe - one to many - one recipe can be in many different favourites table



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


