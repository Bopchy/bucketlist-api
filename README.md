[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)


# Bapi - A Flask RESTful bucketlist API

Do you need a bucketlist API in your life?

Bapi is a Flask RESTful bucketlist API. It allows you to create bucketlists and create
items inside those bucketlists. Once created, you can perform CRUD (where Create, Read,
Update and Delete refer to POST, GET, PUT, DELETE operations respectively) operations on
your bucketlists as well as the items within them. The section on functionality below
lists the endpoints for these CRUD operations.

## Functionality

Below are the list of methods and endpoints available, as well as their respective
functionalities.

METHOD | ENDPOINT | FUNCTIONALITY
--- | --- | ---
POST| ```/auth/login``` | Logs a user in
POST | ```/auth/register``` | Registers a user
POST| ```/bucketlists/``` | Creates a new bucketlist
GET|  ```/bucketlists/``` | Lists all the created bucketlists
GET|  ```/bucketlists/<id>```| Retrieves a single bucketlist
PUT| ```/bucketlists/<id>```| Updates the specified bucketlist
DELETE | ```/bucketlists/<id>```| Deletes the specified bucketlist
POST| ```/bucketlists/<id>/items/```| Creates a new item in the specified bucketlist
PUT | ```/bucketlists/<id>/items/<item_id>```|Updates specified item in the specified bucketlist
DELETE | ```/bucketlists/<id>/items/<item_id>```| Deletes specified item from the specified bucketlist

## Getting started

This section explains how to get the API up and running.

### Prerequisites

All the prerequisites for this API can be found in the requirements.txt file inside
the app folder (bapi).

### Installation

To set up the environment:

  * First, clone the repo by running

    ```git clone https://github.com/Bopchy/bucketlist-api.git```

  * Create a Python3 virtual environment called bucketlist by running

    ```virtualenv -p python3 bucketlist```

    then activate it by

    ```source bucketlist/bin/activate```

    or

    ```mkvirtualenv -p python3 bucketlist```

    then activate it by

    ```workon bucketlist```

    if you use virtualenvwrapper

  * Install the necessary prerequisites by running

    ```pip install -r requirements.txt```

    from inside the bucketlist-api folder

  * Run the bash script to set up the database, like so

    ```sh bucketlist_api_script.sh```

**Note:** You will need to set up your database paths and SECRET_KEY in your environment.
You will need to set up a path for the Development, Test and Production environments with
the respective keys mentioned in the config.py file.

### Usage

This section will utilize the Postman REST client to demonstrate  Bapi's CRUD functionality.
The body content for Postman should be set to **raw** and **JSON(application/json)** since we are using JSON.

We will also use Flask's localhost server, with port 5000.

#### Registering a user

To register a user have ```/auth/register``` as your URL, ensure that the method is a POST. Provide a username, email and password like so

   ```{"username": "bapito", "email": "bapito@email.com", "password": "pass"}
   ```

   ![Demo](/bapi/docs_images/register.png)

#### Logging in the user

To login the created user, have ```/auth/login``` as your URL; and ensure that the method is a POST. Provide a username and password

  ```{"username": "bapito", "password": "pass"}
  ```

    ![Demo](/bapi/docs_images/login.png)

Take note of the token that was produced in the response body.

#### Creating a bucketlist

To create a bucketlist, have ```/bucketlists/``` as your URL;
and ensure that the method is a POST. In order to create a bucketlist, you require an authorization token. The token that was produced when user was logged in, is what should be placed in the headers section; preceded by the word 'Token'.

    ![Demo](/bapi/docs_images/token.png)

Provide a name for the bucketlist

    ```{"name": "Bapito's first bucketlist"}
    ```

    ![Demo](/bapi/docs_images/bucketlist_creation.png)

#### Creating a bucketlist item

To create an item inside the bucketlist that was just created, have ```/bucketlists/<id>/items/``` as your URL. The <id> refers to the id of the bucketlist to
which you want the item to belong. Ensure that the method is POST. Provide a name

  ```{"name": "Go to the Netherlands"}
  ```

    ![Demo](/bapi/docs_images/bucketlist_item_creation.png)

To retrieve a single bucketlist, have ```/bucketlists/<id>``` as your URL, and the method
as GET -- where <id> is the id of the bucketlist.

    ![Demo](/bapi/docs_images/bucketlist_list.png)

#### Editing bucketlist and bucketlist item

To edit a bucketlist, have ```/bucketlists/<id>``` as your URL; and the method as PUT. Provide the new name for the bucketlist

  ```{"name": "Bapito's travel bucketlist"}
  ```

    ![Demo](/bapi/docs_images/edit_bucketlist.png)

To edit an item in the bucketlist, have ```/bucketlists/<id>/items/<item_id>``` as your URL, and your method as PUT. Then provide the new item name.

    ![Demo](/bapi/docs_images/edit_bucketlist_item.png)

The edited buckelist and bucketlist item:

    ![Demo](/bapi/docs_images/list_edited.png)

#### Searching for a bucketlist, with a limit

Bapi has a feature for searching for bucketlists by name. To do that simply have ```/bucketlists?q=``` as your URL, with the word that you wish to search for coming after q

  ```/bucketlists?q=travel
  ```

    ![Demo](/bapi/docs_images/list_edited.png)

You can also limit the number of search results that you receive in the response by using a limit parameter.

  ```/bucketlists?q=travel&limit=1
  ```

    ![Demo](/bapi/docs_images/list_searching_with_limit.png)

#### Deleting a bucketlist item and a bucketlist

You can delete an item inside a bucketlist by having ```/bucketlists/<id>/items/<item_id>``` as your URL, and the method as DELETE.

    ![Demo](/bapi/docs_images/list_item_delete.png)

The same can be achieved for a bucketlist with ```/bucketlists/<id>``` as your URL and the method as DELETE.

    ![Demo](/bapi/docs_images/list_bucketlist_delete.png)

Below we see that the bucketlist is gone.

    ![Demo](/bapi/docs_images/list_bucketlist_delete.png)

## Running the tests

To run the tests run:

  ```nosetests
  ```

To see the test coverage run:

  ```nosetests --with-coverage
  ```

## Built with

This API was built with:
  * Flask
  * Flask RESTful

## License

This project is licensed under the terms of the MIT license.
