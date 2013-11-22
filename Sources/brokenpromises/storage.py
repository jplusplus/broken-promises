#!/usr/bin/env python
# Encoding: utf-8
# -----------------------------------------------------------------------------
# Project : Broken Promises
# -----------------------------------------------------------------------------
# Author : Edouard Richard                                  <edou4rd@gmail.com>
# -----------------------------------------------------------------------------
# License : GNU General Public License
# -----------------------------------------------------------------------------
# Creation : 20-Nov-2013
# Last mod : 20-Nov-2013
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

from pymongo import MongoClient
from urlparse import urlparse
from brokenpromises import settings, Article, Report

CODE_ERROR  = 0
CODE_INSERT = 1
CODE_UPDATE = 2

class Storage(object):

	COLLECTION_ARTICLES = "articles"
	COLLECTION_REPORTS  = "reports"

	def __init__(self, uri=None):
		self.mongo_uri = uri or settings.MONGODB_URI

	def get_connection(self):
		return MongoClient(self.mongo_uri)

	def get_database(self, database=None):
		db = database or urlparse(self.mongo_uri).path.split("/")[-1]
		return self.get_connection()[db]

	def get_collection(self, collection):
		return self.get_database()[collection]

	# -----------------------------------------------------------------------------
	#
	#    Articles
	#
	# -----------------------------------------------------------------------------
	def save_article(self, article):
		"""
		save or update an article using its url.
		Returns a status CODE 
		"""
		if type(article) in (list, tuple):
			return map(self.save_article, article)
		assert article.url, "article needs an url to be saved"
		articles_collection = self.get_collection(Storage.COLLECTION_ARTICLES)
		previous            = articles_collection.find_one({"url" : article.url})
		if not previous:
			articles_collection.insert(article.__dict__)
			return (article, CODE_INSERT)
		else:
			article_merged = dict(previous.items() + article.__dict__.items())
			articles_collection.update({'_id':previous['_id']}, article_merged)
			return (Article(**article_merged), CODE_UPDATE)
		return (article, CODE_ERROR)

	def _get_articles(self, date):
		articles_collection = self.get_collection(Storage.COLLECTION_ARTICLES)
		articles = articles_collection.find({"ref_dates.date": date})
		return articles

	def get_articles(self, date):
		return [Article(**article) for article in self._get_articles(date)]

	def count_articles(self, date):
		return self._get_articles(date).count()

	# -----------------------------------------------------------------------------
	#
	#    Reports
	#
	# -----------------------------------------------------------------------------
	def save_report(self, report):
		report_collection = self.get_collection(Storage.COLLECTION_REPORTS)
		if type(report) != dict:
			report = report.__dict__
		report_collection.insert(report)
		return CODE_INSERT

	def get_reports(self, name=None, searched_date=None, status=None, channels=None):
		# TODO: handle channels
		report_collection = self.get_collection(Storage.COLLECTION_REPORTS)
		search = {}
		if searched_date:
			search["meta.searched_date"] = searched_date
		if name:
			search["name"] = name
		if status:
			search["meta.status"] = status
		return [Report(**report) for report in report_collection.find(search).sort('date', 1)]

# -----------------------------------------------------------------------------
#
#    TESTS
#
# -----------------------------------------------------------------------------
import unittest

class TestStorage(unittest.TestCase):
	'''Test Class'''

	def setUp(self):
		original_mongo_uri = settings.MONGODB_URI
		original_db        = original_mongo_uri.split("/")[-1]
		self.test_db       = "test" + original_db
		test_uri           = "/".join(original_mongo_uri.split("/")[0:-1]) + "/" + self.test_db
		self.storage       = Storage(uri=test_uri)

	def tearDown(self):
		Storage().get_connection().drop_database(self.test_db)

	def test_get_connection(self):
		co = self.storage.get_connection()
		assert co

	def test_get_database(self):
		db = self.storage.get_database()
		assert db.last_status()['ok']  ==    1, db.last_status()
		assert db.last_status()['err'] is None, db.last_status()

	def test_get_collection(self):
		col_name = "test"
		col      = self.storage.get_collection(col_name)
		assert col_name in col.full_name

	def test_save_article(self):
		a   = Article(url="test")
		# insert
		res, code = self.storage.save_article(a)
		assert code in (CODE_UPDATE, CODE_INSERT)
		assert self.storage.get_collection(Storage.COLLECTION_ARTICLES).count() > 0
		assert type(res) is Article, type(res)
		assert res._id
		# update
		res, code = self.storage.save_article(a)
		assert code in (CODE_UPDATE, CODE_INSERT)
		assert self.storage.get_collection(Storage.COLLECTION_ARTICLES).count() > 0
		assert type(res) is Article, type(res)
		assert res._id

	def test_get_articles(self):
		from brokenpromises import Article
		date = (2011, 11, 2)
		a = Article(url="test")
		a.add_ref_date(date)
		self.storage.save_article(a)
		res = self.storage.get_articles(date)
		assert type(res[0]) is Article, type(res)
		assert len(res) == 1

	def test_save_report(self):
		from brokenpromises import Report
		r   = Report()
		res = self.storage.save_report(r)
		assert res in (CODE_UPDATE, CODE_INSERT)
		assert self.storage.get_collection(Storage.COLLECTION_REPORTS).count() > 0

	def test_get_reports(self):
		from brokenpromises import Report
		r   = Report()
		r.meta['searched_date'] = (2014, 10, None)
		self.storage.save_report(r)
		res_ok = self.storage.get_reports(searched_date=(2014, 10, None))
		res_ko = self.storage.get_reports(searched_date=(2014, 10, 11))
		assert len(res_ok) == 1, len(res_ok)
		assert len(res_ko) == 0, len(res_ko)
		assert type(res_ok[0]) is Report

if __name__ == "__main__":
	# unittest.main()
	suite = unittest.TestLoader().loadTestsFromTestCase(TestStorage)
	unittest.TextTestRunner(verbosity=2).run(suite)

# EOF
