from datetime import datetime

""" Function that serializes objects of the datetime class, 
that are not JSON serializable by default - by representing 
them in their ISO 8601 format eg. 
('2012, 12, 4').isoformat() == '2012-12-4'. """

def json_serializer(python_object):
	
	if isinstance(python_object, datetime):
		serial = python_object.isoformat()
		return serial
	raise TypeError('Type is not a date, and is not serializable.')
