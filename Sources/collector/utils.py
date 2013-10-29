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
import datetime
import collector.channels  as channels
import importlib
import pkgutil
import sys

def get_all_date_formats(year, month=None, day=None):
	formats = []
	if day is not None:
		assert month is not None
		day = int(day)
	if month:
		month = int(month)
	year = int(year)
	date = datetime.date(year, month or 1, day or 1)
	if day:
		formats.append("%s %s %s"       % (day, date.strftime("%B"), year))
		formats.append("%sth of %s, %s" % (day, date.strftime("%B"), year))
		formats.append("%sth in %s, %s" % (day, date.strftime("%B"), year))
		formats.append("%sth by %s, %s" % (day, date.strftime("%B"), year))
		formats.append("%sth of %s %s"  % (day, date.strftime("%B"), year))
		formats.append("%sth in %s %s"  % (day, date.strftime("%B"), year))
		formats.append("%sth by %s %s"  % (day, date.strftime("%B"), year))
		formats.append("%sth %s %s"     % (day, date.strftime("%B"), year))
		formats.append("%s of %s, %s"   % (day, date.strftime("%B"), year))
		formats.append("%s in %s, %s"   % (day, date.strftime("%B"), year))
		formats.append("%s by %s, %s"   % (day, date.strftime("%B"), year))
		formats.append("%s of %s %s"    % (day, date.strftime("%B"), year))
		formats.append("%s in %s %s"    % (day, date.strftime("%B"), year))
		formats.append("%s by %s %s"    % (day, date.strftime("%B"), year))
		formats.append("%s %s, %s"      % (day, date.strftime("%B"), year))
		formats.append(date.isoformat())
		formats.append(date.isoformat().replace("-", "/"))
	elif month:
		formats.append("%s %s"  % (date.strftime("%B"), year))
		formats.append("%s, %s" % (date.strftime("%B"), year))
	else:
		formats.append("%s" % year)
	return formats

def get_available_channels():
	return ["collector.channels.%s" % _[1] for _ in pkgutil.walk_packages(sys.modules['collector.channels'].__path__)]

def perform_channels_import(val):
	if type(val) in (tuple, list):
		return (import_channels_from_string(item) for item in val)
	elif type(val) is type(""):
		return (import_channels_from_string(val),)
	else:
		return (val,)

def import_channels_from_string(val):
	importlib.import_module(val)
	module_name = val.split('.')[-1]
	return channels.Catalogue.CHANNELS[module_name]['class']

# -----------------------------------------------------------------------------
#
# TESTS
#
# -----------------------------------------------------------------------------
import unittest

class TestUtils(unittest.TestCase):
	'''Test Class'''

	def test_get_all_date_formats(self):
		formats = get_all_date_formats("2013")
		formats.sort()
		assert(formats == ['2013'])

		formats = get_all_date_formats("2013", "10")
		formats.sort()
		assert(formats == ['October 2013', 'October, 2013'])

		formats = get_all_date_formats("2013", 10, "10")
		formats.sort()
		assert(formats == ['10 October 2013', '10 October, 2013', '10 by October 2013', '10 by October, 2013', '10 in October 2013', '10 in October, 2013', '10 of October 2013', '10 of October, 2013', '10th October 2013', '10th by October 2013', '10th by October, 2013', '10th in October 2013', '10th in October, 2013', '10th of October 2013', '10th of October, 2013', '2013-10-10', '2013/10/10']), formats

	def test_get_available_channels(self):
		channels = get_available_channels()
		assert len(channels) > 0
		assert "collector.channels.nytimes" in channels

if __name__ == "__main__":
	# unittest.main()
	suite = unittest.TestLoader().loadTestsFromTestCase(TestUtils)
	unittest.TextTestRunner(verbosity=2).run(suite)

# EOF
