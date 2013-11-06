#!/usr/bin/env python
# Encoding: utf-8
# -----------------------------------------------------------------------------
# Project : Broken Promises
# -----------------------------------------------------------------------------
# Author : Edouard Richard                                  <edou4rd@gmail.com>
# -----------------------------------------------------------------------------
# License : proprietary journalism++
# -----------------------------------------------------------------------------
# Creation : 28-Oct-2013
# Last mod : 31-Oct-2013
# -----------------------------------------------------------------------------

import optparse
from collector.operations import CollectArticles
import collector.channels
from bson.json_util import dumps

oparser = optparse.OptionParser(usage ="\n./%prog [options] year \n./%prog [options] year month\n./%prog [options] year month day")
oparser.add_option("-C", "--nocache", action="store_true", dest="nocache",
	help = "Prevents from using the cache", default=False)
oparser.add_option("-f", "--channelslistfile", action="store", dest="channels_file",
	help = "Use this that as channels list to use", default=None)
oparser.add_option("-c", "--channels", action="store", dest="channels_list",
	help = "channels list comma separated", default=None)
oparser.add_option("-m", "--mongodb", action="store", dest="mongodb_uri",
	help = "uri to mongodb instance to persist results", default=None)
oparser.add_option("-d", "--drop", action="store_true", dest="mongodb_drop",
	help = "drop the previous articles from database before", default=False)
options, args = oparser.parse_args()
assert len(args) > 0 and len(args) <= 3

channels = collector.channels.get_available_channels()
if options.channels_file:
	with open(options.channels_file) as f:
		channels = [line.replace("\n", "") for line in f.readlines()]
if options.channels_list:
	channels = options.channels_list.split(",")

results = CollectArticles(channels, *args).run()

#  MONGO
if options.mongodb_uri:
	from pymongo import MongoClient
	from urlparse import urlparse

		

	client     = MongoClient(options.mongodb_uri)
	db         = client[urlparse(options.mongodb_uri).path.split("/")[-1]]
	collection = db['articles']

	if options.mongodb_drop:
		collection.remove()

	for article in results:
		previous = collection.find_one({"url" : article.url})
		if not previous:
			collection.insert(article.__dict__)
		else:
			collection.update({'_id':previous['_id']}, dict(previous.items() + article.__dict__.items()))

# OUTPUT
print dumps([_.__dict__ for _ in results])

exit()

# EOF
