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
# Last mod : 05-Nov-2013
# -----------------------------------------------------------------------------

# -----------------------------------------------------------------------------
#
#    Article
#
# -----------------------------------------------------------------------------
class Article:

	def __init__(self, channel, title=None, url=None, source=None, body=None, 
				 pub_date=None, ref_date=[], images=[], headline=None, snippets=[]):
		self.title    = title
		self.url      = url
		self.source   = source
		self.body     = body
		self.pub_date = pub_date
		self.ref_date = ref_date
		self.images   = images
		self.headline = headline
		self.snippets = snippets
		self.channel  = channel

	def __unicode__(self):
		return u"\"%s - %s...\"" % (self.source, self.title[:20])
	def __repr__(self):
		return self.__unicode__()
	def __str__(self):
		return self.__unicode__()

# EOF
