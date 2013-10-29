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

from   wwwclient import HTML
import requests
import requests_cache

# Set up cache for requests
requests_cache.install_cache('broken-promise', backend='sqlite', expire_after=3000)

# -----------------------------------------------------------------------------
#
# DECORATORS
#
# -----------------------------------------------------------------------------
def channel(description):
	"""A decorator that allows to declare a specific channel with its
	documentation."""
	def wrapper(_):
		return Catalogue.RegisterChannel(_.__module__.split('.')[-1],description,_)
	return wrapper

# -----------------------------------------------------------------------------
#
# CATALOGUE
#
# -----------------------------------------------------------------------------
class Catalogue:
	"""The Catalogue is a singleton that acts a registry for data sources
	and their  channel, allowing to list and instanciate data collection
	objects."""

	CHANNELS    = {}

	@classmethod
	def RegisterChannel( self, name, description, channelClass ):
		if name in self.CHANNELS: return channelClass
		self.CHANNELS[name] = {
			"name"  :name,
			"doc"   :description,
			"class" :channelClass
		}
		return channelClass

# -----------------------------------------------------------------------------
#
#    CHANNEL BASE CLASS
#
# -----------------------------------------------------------------------------
# TODO :
#  [ ] set an environment shared by all jobs in this module.
#  [ ] handle error from scrapping, api, http requests
#  [ ] logging
class Channel:
	"""A data channel is a class that allows to retrieve information from
	a given channel (ie. The Guardian, New York Times, RSS, etc...)."""

	def __init__(self):
		self.HTML    = HTML
		self.session = requests

# EOF
