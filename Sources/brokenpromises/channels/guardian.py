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
import requests
import re
import time
from bs4 import BeautifulSoup

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
					time.sleep(.11)
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
		r = requests.get(TheGuardian.URI, params=payload)
		if r.status_code != 200:
			if r.json()['response']['message'] == "only one value allowed in q parameter":
				# error known
				return None
			else:
				error("Guardian returns an error for %s:\n %s\n%s" % (TheGuardian.URI, r.text, payload))
				return None
		return r.json()

	def apply_filters(self, body):
		body = BeautifulSoup(body)
		# remove comments
		map(lambda _:_.decompose(), body.find_all(class_="element-comment"))
		# remove all the blockquotes (for tweet).
		# TODO: Should preserve a date inside the quote.
		map(lambda _:_.decompose(), body.find_all("blockquote"))
		map(lambda _:_.decompose(), body.find_all("script"))
		map(lambda _:_.extract(), body.find_all(text=re.compile("was (changed|amended|edited) on")))
		return unicode(body)

	def scrape_body_article(self, url, filter_=False):
		r       = requests.get(url)
		soup    = BeautifulSoup(r.text, 'html5lib')
		article = soup.find(id='article-body-blocks') or soup.find(id='live-blog-blocks')
		if filter_:
			article = self.apply_filters(unicode(article))
		return unicode(article)

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

	def test_apply_filters(self):
		contains = """This article was amended on 3 November 2013""" # and should be filtered
		url      = "http://www.theguardian.com/politics/2013/nov/03/gerry-adams-jean-mcconville"
		body     = self.obj.scrape_body_article(url)
		body     = self.obj.apply_filters(body)
		assert contains not in body
if __name__ == "__main__":
	# unittest.main()
	suite = unittest.TestLoader().loadTestsFromTestCase(TestTheGuardian)
	unittest.TextTestRunner(verbosity=2).run(suite)

# EOF
