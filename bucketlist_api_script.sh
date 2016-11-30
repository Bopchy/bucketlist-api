#!/bin/bash
# Runs migrations for bucketlist API 
python bapi/manage.py 

# Runs all the tests for bucketlist API
nosetests 