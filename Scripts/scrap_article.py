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
# Last mod : 27-Nov-2013
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
import dateparser
import argparse
import json

def get_channel(_id):
	return brokenpromises.channels.Catalogue.CHANNELS[_id]['class']()

if __name__ == "__main__":
	parser = argparse.ArgumentParser(description='')
	parser.add_argument('url', type=str, help='url to scrap')
	parser.add_argument('--with-filters', dest='filters', action='store_true', default=False, help='Apply filters to remove unwanted dates')
	parser.add_argument('--dates', dest='dates', action='store_true', default=False, help='Return the date found in the article')

	args = parser.parse_args()
	url = args.url
	available_channels = brokenpromises.channels.get_available_channels()
	brokenpromises.channels.perform_channels_import(available_channels)
	channel = None
	if "nytimes.com" in url:
		channel = get_channel('nytimes')
	elif "theguardian.com" in url:
		channel = get_channel('guardian')
	if channel:
		if args.dates:
			args.filters = True
		body = channel.scrape_body_article(url, filter_=args.filters)
		if args.dates:
			dates = []
			for date_obj, date_row, date_position in dateparser.find_dates(body):
				dates.append(date_obj)
			print json.dumps(dates)
		else:
			print body.encode('utf-8', 'ignore')

# EOF
