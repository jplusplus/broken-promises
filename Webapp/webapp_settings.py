import os

DEBUG          = True
ASSETS_DEBUG   = DEBUG

# Authentication
SECRET_KEY         = "49602ea637a8369917c5ef57d269522ed6d9c809"
SUPERUSER_PASSWORD = os.environ.get('SUPERUSER_PASSWORD', "brokenpromises")

# MongoDB
MONGOLAB_URI = os.environ.get('MONGOLAB_URI')
if MONGOLAB_URI:
	from urlparse import urlparse
	uri = urlparse(MONGOLAB_URI)
	MONGO_HOST     = uri.hostname
	MONGO_PORT     = uri.port
	MONGO_DBNAME   = uri.path.lstrip("/")
	MONGO_USERNAME = uri.username
	MONGO_PASSWORD = uri.password
else:
	MONGO_HOST   = 'localhost'
	MONGO_PORT   = 27017
	MONGO_DBNAME = 'broken-promises'

from brokenpromises import settings
REDIS_URL = settings.REDIS_URL

# EOF
