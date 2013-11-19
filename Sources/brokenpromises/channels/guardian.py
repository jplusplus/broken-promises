#!/usr/bin/env python
# Encoding: utf-8
# -----------------------------------------------------------------------------
# Project : Broken Promises
# -----------------------------------------------------------------------------
# Author : Edouard Richard                                  <edou4rd@gmail.com>
# -----------------------------------------------------------------------------
# License : GNU General Public License
# -----------------------------------------------------------------------------
# Creation : 29-Oct-2013
# Last mod : 12-Nov-2013
# -----------------------------------------------------------------------------
# This file is part of Broken Promises.
# 
#     Broken Promises is free software: you can redistribute it and/or modify
#     it under the terms of the GNU General Public License as published by
#     the Free Software Foundation, either version 3 of the License, or
#     (at your option) any later version.
# 
#     Broken Promises is distributed in the hope that it will be useful,
#     but WITHOUT ANY WARRANTY; without even the implied warranty of
#     MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#     GNU General Public License for more details.
# 
#     You should have received a copy of the GNU General Public License
#     along with Broken Promises.  If not, see <http://www.gnu.org/licenses/>.


from brokenpromises          import Article, settings
from brokenpromises.channels import Channel, channel
import brokenpromises.utils  as utils
import datetime
import reporter

debug, trace, info, warning, error, fatal = reporter.bind(__name__)

@channel("The Guardian")
class TheGuardian(Channel):
	"""
	Key Rate Limits
		12      Calls per second
		5,000   Calls per day
	"""

	URI     = "http://content.guardianapis.com/search"
	API_KEY = settings.BP_CHANNEL_GUARDIAN_API_KEY

	def get_articles(self, year, month=None, day=None):
		different_date_formats = utils.get_all_date_formats(year, month, day)
		articles = []
		for format in different_date_formats:
			response = self.request_api(keyword=format)
			if response:
				for article in response['response']['results']:
					# escaping conditions
					if article.get('web_url') in [_.url for _ in articles] :
						# this url is already added in the response
						continue
					a = Article(TheGuardian.__module__)
					a.url      = article.get('webUrl')
					a.title    = article.get('webTitle')
					a.source   = "The Guardian"
					a.pub_date = datetime.datetime.strptime(article.get('webPublicationDate'), "%Y-%m-%dT%H:%M:%SZ")
					a.snippet  = article.get('fields').get('trailText')
					# a.images   = TODO
					# scrape body from page
					a.body     = self.scrape_body_article(a.url)
					if a.body:
						articles.append(a)
					else:
						warning("no body for article %s" % (a.__dict__))
						pass
		return articles

	def request_api(self, keyword):
		payload  = {
			"api-key"     : TheGuardian.API_KEY,
			"q"           : "\"%s\"" % (keyword),
			"show-fields" : "all",
			# section list here: http://content.guardianapis.com/sections
			"section"     : "-fashion,-music,-artanddesign,-film,-guardian-masterclasses",
			"page-size"   : 50 # maximum
		}
		r = self.session.get(TheGuardian.URI, params=payload)
		if r.status_code != 200:
			if r.json()['response']['message'] == "only one value allowed in q parameter":
				# error known
				return None
			else:
				error("Guardian returns an error for %s:\n %s\n%s" % (TheGuardian.URI, r.json(), payload))
				return None
		return r.json()

	def scrape_body_article(self, url):
		r = self.session.get(url)
		paragraphs = self.HTML.parse(r.text).query('#article-body-blocks')
		if not paragraphs:
			paragraphs =  self.HTML.parse(r.text).query('#live-blog-blocks')
		# return None if nothing found
		if not paragraphs:
			warning("there is no paragraph found for article %s" % (url))
			return None
		paragraphs = paragraphs[0]
		# fitlers
		paragraphs = filter(lambda  _: _.name() != "script"              , paragraphs)
		paragraphs = filter(lambda  _: "was amended on"  not in _.text() , paragraphs)
		paragraphs = filter(lambda  _: "was changed on"  not in _.text() , paragraphs)
		paragraphs = filter(lambda  _: "was edited on"   not in _.text() , paragraphs)
		return "".join(map(lambda _:_.html() ,paragraphs))

# -----------------------------------------------------------------------------
#
# TESTS
#
# -----------------------------------------------------------------------------
import unittest

class TestTheGuardian(unittest.TestCase):
	'''Test Class'''

	def setUp(self):
		self.obj = TheGuardian()

	def test_get_articles(self):
		date  = (2013, 12)
		articles = self.obj.get_articles(*date)
		print
		print date
		print "results: ", len(articles)
		assert len(articles) > 0
		for article in articles:
			assert article.url  is not None, article
			assert article.body is not None, article
			# print article.url

	def test_filter_article(self):
		contains = """This article was amended on 3 November 2013""" # and should be filtered
		url      = "http://www.theguardian.com/politics/2013/nov/03/gerry-adams-jean-mcconville"
		body     = self.obj.scrape_body_article(url)
		assert contains not in body
if __name__ == "__main__":
	# unittest.main()
	suite = unittest.TestLoader().loadTestsFromTestCase(TestTheGuardian)
	unittest.TextTestRunner(verbosity=2).run(suite)

# EOF
