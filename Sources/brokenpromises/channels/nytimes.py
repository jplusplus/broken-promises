#!/usr/bin/env python
# Encoding: utf-8
# -----------------------------------------------------------------------------
# Project : Broken Promises
# -----------------------------------------------------------------------------
# Author : Edouard Richard                                  <edou4rd@gmail.com>
# -----------------------------------------------------------------------------
# License : GNU General Public License
# -----------------------------------------------------------------------------
# Creation : 28-Oct-2013
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
from bs4 import BeautifulSoup

debug, trace, info, warning, error, fatal = reporter.bind(__name__)

# TODO
#   [ ] handle pagination

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
	API_KEY = settings.BP_CHANNEL_NYTIMES_API_KEY

	def get_articles(self, year, month=None, day=None):
		different_date_formats = utils.get_all_date_formats(year, month, day)
		articles = []
		for format in different_date_formats:
			response = self.request_api(keyword=format)
			if response:
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
					a.pub_date = datetime.datetime.strptime(article.get('pub_date'), "%Y-%m-%dT%H:%M:%SZ")
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
		r = requests.get(NewYorkTimes.URI, params=payload)
		if r.status_code != 200:
			error("Nytimes returns an error for %s:\n %s\n%s" % (NewYorkTimes.URI, r.text, payload))
			return None
		return r.json()

	def scrape_body_article(self, url, filter_=False):
		r       = requests.get(url)
		soup    = BeautifulSoup(r.text)
		article = soup.find_all(class_='articleBody')
		article = u"".join([str(a).decode("utf-8", 'ignore') for a in article])
		if filter_:
			article = self.apply_filters(article)
		return unicode(article)

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
		body = self.obj.scrape_body_article("http://www.nytimes.com/2013/11/20/your-money/how-doctors-die.html?src=me&ref=general")
		assert type(body) is unicode, type(body)
		assert body != u"", body
		# start of the article
		assert u"You hear that word a" in body
		# end of the article
		assert u"hard to get answers." in body

if __name__ == "__main__":
	# unittest.main()
	suite = unittest.TestLoader().loadTestsFromTestCase(TestNewYorkTimes)
	unittest.TextTestRunner(verbosity=2).run(suite)

# EOF
