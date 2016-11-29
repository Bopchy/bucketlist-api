#!/bin/bash
# Runs migrations for bucketlist API 
python api/manage.py 

# Runs all the tests for bucketlist API
nosetests 