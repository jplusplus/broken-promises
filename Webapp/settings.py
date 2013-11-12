import os

DEBUG          = True
ASSETS_DEBUG   = DEBUG

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

# Enable reads (GET), inserts (POST) and DELETE for resources/collections
# (if you omit this line, the API will default to ['GET'] and provide
# read-only access to the endpoint).
RESOURCE_METHODS = ['GET', 'POST', 'DELETE']

# Enable reads (GET), edits (PATCH), replacements (PUT) and deletes of
# individual items  (defaults to read-only item access).
ITEM_METHODS          = ['GET', 'PATCH', 'PUT', 'DELETE']
PAGINATION_DEFAULT    = 1000000
PAGINATION_LIMIT      = 1000000
EXTRA_RESPONSE_FIELDS = []
ALLOW_UNKNOWN         = True
X_DOMAINS             = '*'
schema                = {
	# Schema definition, based on Cerberus grammar. Check the Cerberus project
	# (https://github.com/nicolaiarocci/cerberus) for details.
	'title': {
		'type': 'string',
	},
	'url': {
		'type': 'string',
		'unique': True,
	},
	'source' : {
		'type' : 'string'
	},
	'body' : {
		'type' : 'string'
	},
	'pub_date' : {
		'type' : 'string'
	},
	'ref_dates' : {
		'type' : 'list'
	},
	'headline' : {
		'type' : 'string',
		'nullable' : True
	},
	'channel' : {
		'type' : 'string'
	},
	'note' : {
		'type' : 'integer'
	}
}
articles = {
	# 'title' tag used in item links. Defaults to the resource title minus
	# the final, plural 's' (works fine in most cases but not for 'people')
	'item_title': 'article',
	'schema': schema
}

DOMAIN = {
	'articles': articles,
}

# EOF

