#!/usr/bin/env python
# Encoding: utf-8
# -----------------------------------------------------------------------------
# Project : OKF - Spending Stories
# -----------------------------------------------------------------------------
# Author : Edouard Richard                                  <edou4rd@gmail.com>
# -----------------------------------------------------------------------------
# License : proprietary journalism++
# -----------------------------------------------------------------------------
# Creation : 28-Oct-2013
# Last mod : 31-Oct-2013
# -----------------------------------------------------------------------------

import optparse
from collector import Collector
import collector.utils as utils

oparser = optparse.OptionParser(usage ="\n./%prog [options] year \n./%prog [options] year month\n./%prog [options] year month day")
oparser.add_option("-C", "--nocache", action="store_true", dest="nocache",
	help = "Prevents from using the cache", default=False)
oparser.add_option("-f", "--channelslistfile", action="store", dest="channels_file",
	help = "Use this that as channels list to use", default=None)
oparser.add_option("-c", "--channels", action="store", dest="channels_list",
	help = "channels list comma separated", default=None)
oparser.add_option("-m", "--mongodb", action="store", dest="mongodb_uri",
	help = "uri to mongodb instance to persist results", default=None)
options, args = oparser.parse_args()
assert len(args) > 0 and len(args) <= 3

channels = utils.get_available_channels()
if options.channels_file:
	with open(options.channels_file) as f:
		channels = [line.replace("\n", "") for line in f.readlines()]
if options.channels_list:
	channels = options.channels_list.split(",")

results = Collector(channels).get_articles(*args)

#  MONGO
if options.mongodb_uri:
	from pymongo import MongoClient
	from bson.json_util import dumps
	from urlparse import urlparse

	client     = MongoClient(options.mongodb_uri)
	db         = client[urlparse(options.mongodb_uri).path.split("/")[-1]]
	collection = db['articles']

	for article in results:
		previous = collection.find_one({"url" : article.url})
		if not previous:
			collection.insert(article.__dict__)
		else:
			collection.update({'_id':previous['_id']}, article.__dict__)

# OUTPUT
print dumps([_.__dict__ for _ in results])

exit()
# EOF
