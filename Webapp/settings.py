# import os
DEBUG          = True
# LIB_DIR        = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'lib')
# FREEZER_RELATIVE_URLS = True
ASSETS_DEBUG   = DEBUG

# EVE

MONGO_HOST = 'localhost'
MONGO_PORT = 27017
MONGO_DBNAME = 'broken-promises'

SERVER_NAME = '127.0.0.1:5000'

# Enable reads (GET), inserts (POST) and DELETE for resources/collections
# (if you omit this line, the API will default to ['GET'] and provide
# read-only access to the endpoint).
RESOURCE_METHODS = ['GET', 'POST', 'DELETE']

# Enable reads (GET), edits (PATCH), replacements (PUT) and deletes of
# individual items  (defaults to read-only item access).
ITEM_METHODS = ['GET', 'PATCH', 'PUT', 'DELETE']
PAGINATION_DEFAULT = 1000000
PAGINATION_LIMIT = 1000000
EXTRA_RESPONSE_FIELDS = []
ALLOW_UNKNOWN = True
schema = {
	# Schema definition, based on Cerberus grammar. Check the Cerberus project
	# (https://github.com/nicolaiarocci/cerberus) for details.
	'title': {
		'type': 'string',
	},
	'url': {
		'type': 'string',
		# 'required': True,
		# talk about hard constraints! For the purpose of the demo
		# 'lastname' is an API entry-point, so we need it to be unique.
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
	'ref_date' : {
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
	# 'role' is a list, and can only contain values from 'allowed'.
	# 'role': {
	#     'type': 'list',
	#     'allowed': ["author", "contributor", "copy"],
	# },
	# An embedded 'strongly-typed' dictionary.
	# 'location': {
	#     'type': 'dict',
	#     'schema': {
	#         'address': {'type': 'string'},
	#         'city': {'type': 'string'}
	#     },
	# },
	# 'born': {
	#     'type': 'datetime',
	# },
}
articles = {
	# 'title' tag used in item links. Defaults to the resource title minus
	# the final, plural 's' (works fine in most cases but not for 'people')
	'item_title': 'article',

	# by default the standard item entry point is defined as
	# '/people/<ObjectId>'. We leave it untouched, and we also enable an
	# additional read-only entry point. This way consumers can also perform
	# GET requests at '/people/<lastname>'.
	# 'additional_lookup': {
	#     'url': '[\w]+',
	#     'field': 'lastname'
	# },

	# We choose to override global cache-control directives for this resource.
	# 'cache_control': 'max-age=10,must-revalidate',
	# 'cache_expires': 10,

	# most global settings can be overridden at resource level
	# 'resource_methods': ['GET', 'POST'],

	'schema': schema
}

DOMAIN = {
	'articles': articles,
}

# EOF

