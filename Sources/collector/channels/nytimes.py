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
# Last mod : 28-Oct-2013
# -----------------------------------------------------------------------------

from collector          import Article
from collector.channels import Channel, channel
import collector.utils  as utils

@channel("The New-York Times")
class NewYorkTimes(Channel):
	"""
	based on NYT ARTICLE SEARCH API VERSION 2

		doc: http://developer.nytimes.com/docs/read/article_search_api_v2#building-search

		restrictions for `articlesearch`:
			10      Calls per second
			10,000  Calls per day
	"""

	URI     = "http://api.nytimes.com/svc/search/v2/articlesearch.json"
	API_KEY = "fb70195272f6883497bbda131a223746:5:68327206"

	def get_articles(self, year, month=None, day=None):
		different_date_formats = utils.get_all_date_formats(year, month, day)
		articles = []
		for format in different_date_formats:
			response = self.request_api(keyword=format)
			for article in response['response']['docs']:
				# escaping conditions
				if article.get('document_type') not in ('article', 'blog'):
					# it's not an article
					continue
				if article.get('web_url') in [_.url for _ in articles] :
					# this url is already added in the response
					continue
				a = Article(NewYorkTimes.__module__)
				a.url      = article.get('web_url')
				a.title    = article.get('headline')['main']
				a.source   = article.get('source') or "The New York Times"
				a.pub_date = article.get('pub_date')
				a.snippet  = article.get('snippet')
				# a.images   = TODO
				# scrape body from page
				a.body     = self.scrape_body_article(a.url)
				articles.append(a)
		return articles

	def request_api(self, keyword):
		payload  = {
			"api-key" : NewYorkTimes.API_KEY,
			"fq"      : "body:\"%s\"" % keyword
		}
		r = self.session.get(NewYorkTimes.URI, params=payload)
		return r.json()

	def scrape_body_article(self, url):
		r = self.session.get(url)
		paragraphs = self.HTML.parse(r.text).query('.articleBody')
		body = " ".join(map(lambda _:_.text() ,paragraphs))
		return body

# -----------------------------------------------------------------------------
#
# TESTS
#
# -----------------------------------------------------------------------------
import unittest

class TestNewYorkTimes(unittest.TestCase):
	'''Test Class'''

	def setUp(self):
		self.obj = NewYorkTimes()

	def test_get_articles(self):
		date  = (2013,)
		articles = self.obj.get_articles(*date)
		print
		print date
		print "results: ", len(articles)
		assert len(articles) > 0
		for article in articles:
			assert article.url  is not None
			assert article.body is not None
			# print article.url

	def test_scrape_body_article(self):
		body = self.obj.scrape_body_article("http://www.nytimes.com/reuters/2013/10/24/world/africa/24reuters-kenya-security-australia.html?gwh=FD09ABA7920134DF9952DDAC7B08B332&_r=0")
		assert type(body) is unicode
		assert body != ""
		# start of the article
		assert "Militants may be planning attacks on nightclubs and other" in body
		# end of the article
		assert "indications of an imminent attack by Islamist militants." in body

if __name__ == "__main__":
	# unittest.main()
	suite = unittest.TestLoader().loadTestsFromTestCase(TestNewYorkTimes)
	unittest.TextTestRunner(verbosity=2).run(suite)

# EOF
