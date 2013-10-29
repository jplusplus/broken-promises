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
# Last mod : 29-Oct-2013
# -----------------------------------------------------------------------------
from models import Article
import importlib

# -----------------------------------------------------------------------------
#
#    Collector
#
# -----------------------------------------------------------------------------
class Collector:

	def __init__(self, channels=tuple()):
		self.channels = [channel() for channel in self.__perform_channels_import(channels)]

	def get_articles(self, year, month=None, day=None):
		results = []
		for channel in self.channels:
			results += channel.get_articles(year, month, day)
		return results

	def __perform_channels_import(self, val):
		if type(val) in (tuple, list):
			return (self.__import_channels_from_string(item) for item in val)
		elif type(val) is type(""):
			return (self.__import_channels_from_string(val),)
		else:
			return (val,)

	def __import_channels_from_string(self, val):
		parts = val.split('.')
		module_path, class_name = '.'.join(parts[:-1]), parts[-1]
		module = importlib.import_module(module_path)
		return getattr(module, class_name)

#------------------------------------------------
#
# TESTS
#
#------------------------------------------------
import unittest

class TestCollector(unittest.TestCase):
	'''Test Class'''

	def test_get_articles(self):
		collector = Collector(("collector.channels.nytimes.NewYorkTimes",))
		results   = collector.get_articles("2014", "1")
		print 
		print "results:", len(results)
		assert len(results) > 0

if __name__ == "__main__":
	# unittest.main()
	suite = unittest.TestLoader().loadTestsFromTestCase(TestCollector)
	unittest.TextTestRunner(verbosity=2).run(suite)

# EOF
