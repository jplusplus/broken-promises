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
# Last mod : 28-Oct-2013
# -----------------------------------------------------------------------------

import optparse
import json
from   collector import Collector

oparser = optparse.OptionParser(usage ="\n./%prog [options] year \n./%prog [options] year month\n./%prog [options] year month day")
oparser.add_option("-C", "--nocache", action="store_true", dest="nocache",
	help="Prevents from using the cache", default=False
)
options, args = oparser.parse_args()
assert len(args) > 0 and len(args) <= 3

results = Collector().get_articles(*args)

print json.dumps([_.__dict__ for _ in results])
exit()
# EOF
