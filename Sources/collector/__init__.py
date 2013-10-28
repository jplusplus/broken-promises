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
# Last mod : 28-Oct-2013
# -----------------------------------------------------------------------------
from models import Article

# -----------------------------------------------------------------------------
#
#    Collector
#
# -----------------------------------------------------------------------------
# TODO
# 	[ ] Handle sources list

class Collector:

	def __init__(self, channels=[]):
		self.channels = channels

	def get_articles(self, year, month=None, day=None):
		from channels.nytimes import NewYorkTimes
		return NewYorkTimes().get_articles(year, month, day)

# EOF
