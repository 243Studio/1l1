# tkit3 - your link shortener
#### Video Demo: https://youtu.be/SYoiwjDwzNo
### Description: A link shortener

This web-based application is a link shortener. Something like bitly or the linkedIn link shortener.


## WHY
The idea for this project came from a personal need first. I was in need of a link shortener for my personal brand on social media. I decided to try this challenge by building this application.


## FEATURES

### index page

This is achieved in the `/` path

The user is redirected to the /show pages
But the user would need to be logged in.

### registration

This is achieve in the `/register` path
The user can register with a new account by setting up their username, email address and password and they confirm their password. When the password and confirmation password are not the same, when the username is already taken or the password or the username is empty, the user cannot create a new account.

We also use the `check_email` to check if an email address is valid using regex. If the email address is incorrect, they would not be able to create an account, and we return an apology

The password is converted into a hash that is saved into the database.
If they succeed at creating an account they will automatically receive 100 credits to create shortened links. And they are able to login to their tkit3 account.


### login

This is achieved in the `/login` path
This feature is self explanatory.

To login, the user just need to input their credentials (username and password) in order to be able to access their account. If the username and the password are incorrect, or missing they will not be able to login.

It is not the real user password that is checked. There is going to be a comparaison between the hashed version of the password saved in the database and the hash of the password the user typed while trying to login.

If they are not identical, the program should display the apology page and tell the user the the information they entered is not correct.

If they are identical, the user's id and username are saved into the browser session. And the user is logged in

### logout

This is achieved in the `/logout` path
By clicking the log out button, the user should be prompted again if they really want to logout. When the user is logged out, they cannot see the link created by any account, create a shortlink.
When the user log out, the browser session is also cleared out.

### Show (list)

This is achieved in the `/show` path
It displays the credits left, the last time the user was logged in (days) and the list of all the shortened url created by the currently logged user. There is a row with details about a link: the title of the link, how many time it was viewed, the description of the link, the original link and the new shortened link which are both clickable and openning to a new tab.


### create


A feature to help the user create shortened url. This is achieved in the `/create` path.

We will first check whether the request method is post or get. If it is post, we validate the following data: title, description, user_id and check whether the origin link is a valid link by calling the `check_url` function.

We make sure than the origin and the destination url are unique values.

The `check_url`  function takes a string as input implement some regex to check whether the string is a valid link or not. if the link is not valid. do not send the post request but redirect the user to the apology page letting them know that the origin url they submitted is not a valid link.


If the origin url is valid. generate a destination url using the `generate_slug` function. In case the user input a `custom slug` and it is less than 10 characters, generate a slug.In case the user does not input a custom slug but input the number of characters (from 4 to 7). If the number of characters is not provided a 7 characters random slug containing uppercase, lowercase as well as and number is generated.

When the destination is generated. The title, description, the user_id, the origin url and the destination url, the time the link was created are stored in the data base (in the links table).

Creating a random shortlink uses one **credits**.

A custom shortlink costs 5 credits, A randomly generated shortlink costs between 1 and 4 credits: A 7-characters link cost 1 credits, 6-characters link cost 2 credits, a 5-characters link 3 credits, a 4-characters link costs 4 credits.

If the user has zero credit or the amount of credit they have is less than the cost of the type of shortened link (e.g custom link, 5-characters link, etc) they would like to create, they should not be able to create a shortened link.

### A path to redirect the user:

This is achieved in the `/link/[slug]` path.

There is a path that takes a get method with a slug, Verify whether the submitted slug is a string, Check whether the slug is a destination of an destination link existing in the data base.

If it is in the database, increment the number of `views` for that shortened link by incrementing the `count` value in the `views table. And redirect the user to the origin link.

But if the slug is incorrect or is not associated with any data in the database, return an apology page letting the user know that the slug entered does not exist in the database.

