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

import datetime

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

def get_the_date_before(year, month=None, day=None):
	if not month:
		year -= 1
	elif not day:
		month = month > 1 and month - 1 or 12
	date = datetime.date(year, month or 1, day or 1)
	return date

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

if __name__ == "__main__":
	# unittest.main()
	suite = unittest.TestLoader().loadTestsFromTestCase(TestUtils)
	unittest.TextTestRunner(verbosity=2).run(suite)

# EOF
