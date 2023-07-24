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


# R6 An ERD for your app




# R7 Detail any third party services that your app will use

-

# R8 Describe your projects models in terms of the relationships they have with each other

- 

# R9 Discuss the database relations to be implemented in your application



# R10 Describe the way tasks are allocated and tracked in your project

Tasks are managed on Trello 
