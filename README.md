### Table Creation Commands
**Product Table**
product_id
product_name
product_url
quantity
units
price
```
CREATE TABLE products(
	product_id SERIAL PRIMARY KEY,
	product_name VARCHAR(100) UNIQUE NOT NULL,
	product_url VARCHAR(200),
	quantity INT NOT NULL,
	units VARCHAR(25) NOT NULL,
	price DECIMAL(10,2)
);
```
**Store Table**
store_id
store_name
store_url
store_address
```
CREATE TABLE stores(
	store_id SERIAL PRIMARY KEY,
	store_name VARCHAR(100) NOT NULL,
	store_url VARCHAR(200),
	store_address VARCHAR(200) NOT NULL
);
```
**Category Table**
category_name
category_id
```
CREATE TABLE categories(
	category_id SERIAL PRIMARY KEY,
	category_name VARCHAR(100) NOT NULL
);
```
**Store Inventory Table**
store_id
product_id
category_id
quantity_in_stock
```
CREATE TABLE store_inventory(
	store_id INT PRIMARY KEY,
	product_id INT NOT NULL,
	category_id INT NOT NULL,
	quantity_in_stock INT NOT NULL,
	FOREIGN KEY (product_id) REFERENCES products(product_id),
	FOREIGN KEY (category_id) REFERENCES categories(category_id)
);
```
**User Table**
user_name
user_id
user_email
user_ccn - hashed
```
CREATE TABLE users(
	user_id SERIAL PRIMARY KEY,
	user_name VARCHAR(150) NOT NULL,
	user_email VARCHAR(150) UNIQUE,
	user_ccn INT
);
```
**Websites**
website_url
website_name
website_author
```
CREATE TABLE websites(
	website_url VARCHAR(200) PRIMARY KEY,
	website_name VARCHAR(100) NOT NULL,
	website_author VARCHAR(150) NOT NULL
);
```
**Recipes**
recipe_name
instructions
creator
servings
recipe_id
website_url
```
CREATE TABLE recipes(
	recipe_id SERIAL PRIMARY KEY,
	recipe_name VARCHAR(100),
	instructions TEXT,
	creator INT NOT NULL,
	servings INT NOT NULL,
	website_url VARCHAR(200),
	FOREIGN KEY (creator) REFERENCES users(user_id),
	FOREIGN KEY (website_url) REFERENCES websites(website_url)
);
```
**Saved Recipes**
recipe_id
user_id
```
CREATE TABLE saved_recipes(
	user_id INT PRIMARY KEY,
	recipe_id INT NOT NULL,
	FOREIGN KEY (recipe_id) REFERENCES recipes(recipe_id),
	FOREIGN KEY (user_id) REFERENCES users(user_id)
);
```
**Ingredients**
ingredient_id
ingredient_name
```
CREATE TABLE ingredients(
	ingredient_id SERIAL PRIMARY KEY,
	ingredient_name VARCHAR(100)
);
```
**Recipe Ingredients**
recipe_id
ingredient_id
```
CREATE TABLE recipe_ingredients(
	recipe_id INT PRIMARY KEY,
	ingredient_id INT NOT NULL,
	FOREIGN KEY (recipe_id) REFERENCES recipes(recipe_id),
	FOREIGN KEY (ingredient_id) REFERENCES ingredients(ingredient_id)
);
```
**Ingredients to Products**	
ingredient_id
product_id
```
CREATE TABLE ingredients_to_products(
	ingredient_id INT PRIMARY KEY,
	product_id INT NOT NULL,
	FOREIGN KEY (ingredient_id) REFERENCES ingredients(ingredient_id),
	FOREIGN KEY (product_id) REFERENCES products(product_id)
);
```
### Documentation
##### Implementation
For detailed documentation on each function, their input/output, and some general/formatting comments see the CLI python file.
A couple key design choices were made with this codebase that I'd like to cover:

Separate functions for each type of query.
	For simplicity's sake I divided the unique parts of each type of query into their own functions that build the string representation of a query. This is because it struck a good balance of modularity and ease of implementation.

Having the query stored in a global:
	This was mainly done for the sake of simplicity and for ease of building in transactions into the system. This is because with a global query variable it is easy to keep state between iterations of the while loop without adding much logic. 

Generalizing common query building steps:
	By pulling out pieces of the query building that applied to multiple types of queries (like asking the user for the table or the conditions) we can reduce redundancy by a lot. This makes the code base more concise and easier to maintain.

Separating the transactions from the queries:
	This just made implementing transactions easier and I feel it is more intuitive as transactions exists more as a wrapper around other SQL queries rather than a defined stand alone type of query.

##### Usage
1. First the home screen of the CLI allows you to either start a transaction, make an sql query or quit. Starting a transaction will then give you the option to make an sql query, end the transaction or quit. You may write as many sql queries between starting a transaction and ending it as you'd like.
2. If you'd like to make a query you are given a list of types of queries 1-9 and are prompted to enter a number corresponding to the query.
3. If you are to pick either insert or update one of the types of queries involving data, then you will be prompted to enter in the column name and value you'd like to set for that column in the format "columnName=value, columnName2=value2,...".
4. If you are to pick a statement with conditions like for  insert, update, search, or sorting, then you will be prompted to enter the condition which should be entered as it would appear after the WHERE clause.
5. Columns should be specified in a comma separated list and only one table mentioned at any given prompt.
6. Generally just follow the prompts on the screen, most of the time the formatting will be explained in the prompt as well.

There is some flexibility with formats of user input as the program will automatically remove any trailing or leading white space as well as correct and standardize casing in the input.