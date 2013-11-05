#!/usr/bin/env python
# Encoding: utf-8
# -----------------------------------------------------------------------------
# Project : Broken Promises
# -----------------------------------------------------------------------------
# Author : Edouard Richard                                  <edou4rd@gmail.com>
# -----------------------------------------------------------------------------
# License : proprietary journalism++
# -----------------------------------------------------------------------------
# Creation : 05-Nov-2013
# Last mod : 05-Nov-2013
# -----------------------------------------------------------------------------
import collector.channels
import collector.utils

# -----------------------------------------------------------------------------
#
#    Collect Articles
#
# -----------------------------------------------------------------------------
class CollectArticles:

	def __init__(self, channels, year, month=None, day=None):
		self.channels = [channel() for channel in collector.channels.perform_channels_import(channels)]
		self.date     = (year, month, day)

	def run(self):
		results = []
		# retrieve articles from channels
		for channel in self.channels:
			results += channel.get_articles(*self.date)
		# search dates in the body articles
		for result in results:
			# result.ref_dates = collector.utils.get_referenced_dates(
			# 	text  = result.body,
			# 	dates_hints = (self.date,))
			pass
		return results

# -----------------------------------------------------------------------------
#
# TESTS
#
# -----------------------------------------------------------------------------
import unittest

class TestOperations(unittest.TestCase):
	'''Test Class'''

	def test_get_articles(self):
		channels = (
			"collector.channels.nytimes",
			# "collector.channels.guardian",
		)
		# channels  = collector.utils.get_available_channels()

		collector = CollectArticles(channels, "2014", "1")
		results   = collector.run()
		print 
		print "results:", len(results)
		assert len(results) > 0

if __name__ == "__main__":
	# unittest.main()
	suite = unittest.TestLoader().loadTestsFromTestCase(TestOperations)
	unittest.TextTestRunner(verbosity=2).run(suite)
