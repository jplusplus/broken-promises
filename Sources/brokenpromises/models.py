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
# Last mod : 11-Nov-2013
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

import datetime

# -----------------------------------------------------------------------------
#
#    Article
#
# -----------------------------------------------------------------------------
class Article(object):

	def __init__(self, channel=None, title=None, url=None, source=None, body=None, 
				 pub_date=None, ref_dates=[], images=[], headline=None, created=None, 
				 *args, **kwargs):
		self.title     = title
		self.url       = url
		self.source    = source
		self.body      = body
		if type(pub_date) in (unicode, str):
			# TODO: date peuvent etre en unicode (Tue, 21 May 2013 08:23:00 GMT), doivent être parsées
			self.pub_date = pub_date
		else:
			self.pub_date = pub_date
		self.pub_date  = pub_date
		self.ref_dates = ref_dates
		self.images    = images
		self.headline  = headline
		self.channel   = channel
		self.created   = created or datetime.datetime.now()
		# set extra fields, like _id from mongodb
		for _k, _v in kwargs.items():
			if not hasattr(self, _k):
				setattr(self, _k, _v)

	def add_ref_date(self, date, **kwargs):
		kwargs['date'] = date
		self.ref_dates.append(kwargs)

	def __unicode__(self):
		return u"\"%s - %s\"" % (
			self.source,
			hasattr(self, '_id') and "id: " + self._id             \
			or self.url          and "http://..." + self.url[-30:] \
			or "untitled"
		)
	def __repr__(self):
		return self.__unicode__()
	def __str__(self):
		return self.__unicode__()

# -----------------------------------------------------------------------------
#
#    REPORT
#
# -----------------------------------------------------------------------------
class Report(object):

	def __init__(self, collector=None, caller=None, date=None, errors=[], meta={}, *args, **kwargs):
		self.date      = date
		self.collector = collector
		self.errors    = errors
		self.caller    = caller
		self.meta      = meta
		# set extra fields, like _id from mongodb
		for _k, _v in kwargs.items():
			if not hasattr(self, _k):
				setattr(self, _k, _v)

	def __unicode__(self):
		return u"Report %s (%s)" % (self.collector, self.date)
	def __repr__(self):
		return self.__unicode__()
	def __str__(self):
		return self.__unicode__()

# EOF
