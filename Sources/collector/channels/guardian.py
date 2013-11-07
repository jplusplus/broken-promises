#!/usr/bin/env python
# Encoding: utf-8
# -----------------------------------------------------------------------------
# Project : Broken Promises
# -----------------------------------------------------------------------------
# Author : Edouard Richard                                  <edou4rd@gmail.com>
# -----------------------------------------------------------------------------
# License : proprietary journalism++
# -----------------------------------------------------------------------------
# Creation : 29-Oct-2013
# Last mod : 29-Oct-2013
# -----------------------------------------------------------------------------

from collector          import Article
from collector.channels import Channel, channel
import collector.utils  as utils

@channel("The Guardian")
class TheGuardian(Channel):
	"""
	Key Rate Limits
		12      Calls per second
		5,000   Calls per day
	"""

	URI     = "http://content.guardianapis.com/search"
	API_KEY = "79t54uxw5duhevew9arubq4v"

	def get_articles(self, year, month=None, day=None):
		different_date_formats = utils.get_all_date_formats(year, month, day)
		articles = []
		for format in different_date_formats:
			try:
				response = self.request_api(keyword=format)
			except Exception as e:
				# TODO: log error
				# print e
				continue
			for article in response['response']['results']:
				# escaping conditions
				if article.get('web_url') in [_.url for _ in articles] :
					# this url is already added in the response
					continue
				a = Article(TheGuardian.__module__)
				a.url      = article.get('webUrl')
				a.title    = article.get('webTitle')
				a.source   = "The Guardian"
				a.pub_date = article.get('webPublicationDate')
				a.snippet  = article.get('fields').get('trailText')
				# a.images   = TODO
				# scrape body from page
				a.body     = self.scrape_body_article(a.url)
				if a.body:
					articles.append(a)
				else:
					# TODO Loggin
					# print a, a.url
					pass
		return articles

	def request_api(self, keyword):
		payload  = {
			"api-key"     : TheGuardian.API_KEY,
			"q"           : "\"%s\"" % (keyword),
			"show-fields" : "all",
			# section list here: http://content.guardianapis.com/sections
			"section"     : "-fashion,-music,-artanddesign,-film",
			"page-size"   : 50 # maximum
		}
		r = self.session.get(TheGuardian.URI, params=payload)
		if r.status_code != 200:
			raise Exception("API returns an error:\n %s\n\n%s" % (r.text, payload))
		return r.json()

	def scrape_body_article(self, url):
		r = self.session.get(url)
		paragraphs = self.HTML.parse(r.text).query('#article-body-blocks')
		if not paragraphs:
			paragraphs =  self.HTML.parse(r.text).query('#live-blog-blocks')
		# return None if nothing found
		if not paragraphs:
			# TODO : Logging
			return None
		paragraphs = paragraphs[0]
		# fitlers
		paragraphs = filter(lambda  _: _.name() != "script"                       , paragraphs)
		paragraphs = filter(lambda  _: "This article was amended" not in _.text() , paragraphs)

		return "\n".join(map(lambda _:_.text() ,paragraphs))

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
