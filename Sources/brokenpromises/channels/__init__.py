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
# Last mod : 05-Nov-2013
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

from   wwwclient import HTML

# -----------------------------------------------------------------------------
#
# DECORATORS
#
# -----------------------------------------------------------------------------
def channel(description):
	"""A decorator that allows to declare a specific channel with its
	documentation."""
	def wrapper(_):
		return Catalogue.RegisterChannel( _.__module__.split('.')[-1], description, _ )
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

# -----------------------------------------------------------------------------
#
# MODULE functions
#
# -----------------------------------------------------------------------------
import importlib, pkgutil, sys

def get_available_channels():
	return ["brokenpromises.channels.%s" % _[1] for _ in pkgutil.walk_packages(sys.modules['brokenpromises.channels'].__path__)]

def perform_channels_import(val):
	response = None
	if type(val) in (tuple, list):
		response = tuple(__import_channels_from_string(item) for item in val)
	elif type(val) in (unicode, str):
		response = __import_channels_from_string(val)
	else:
		response = val
	return response

def __import_channels_from_string(val):
	importlib.import_module(val)
	module_name = val.split('.')[-1]
	return Catalogue.CHANNELS[module_name]['class']

# EOF
