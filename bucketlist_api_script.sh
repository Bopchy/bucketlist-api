#!/bin/bash

#Creates migration folder for bucketlist API
python bapi/manage.py db init

# Creates the database tables from the models
python bapi/manage.py db migrate

# Upgrades the database
python bapi/manage.py db upgrade
