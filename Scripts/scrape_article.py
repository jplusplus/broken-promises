#!/usr/bin/env python
# Encoding: utf-8
# -----------------------------------------------------------------------------
# Project : Broken Promises
# -----------------------------------------------------------------------------
# Author : Edouard Richard                                  <edou4rd@gmail.com>
# -----------------------------------------------------------------------------
# License : GNU General Public License
# -----------------------------------------------------------------------------
# Creation : 19-Nov-2013
# Last mod : 19-Nov-2013
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

import brokenpromises.channels
import sys

def get_channel(_id):
	return brokenpromises.channels.Catalogue.CHANNELS[_id]['class']()

if __name__ == "__main__":
	url = sys.argv[1]
	available_channels = brokenpromises.channels.get_available_channels()
	brokenpromises.channels.perform_channels_import(available_channels)
	channel = None
	if "nytimes.com" in url:
		channel = get_channel('nytimes')
	elif "theguardian.com" in url:
		channel = get_channel('guardian')
	if channel:
		body = channel.scrape_body_article(url)
		print body.encode('utf-8')

# EOF
