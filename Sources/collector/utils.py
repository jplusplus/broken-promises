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

def get_snippets(body, to_find=[]):
	snippets = []
	if type(to_find) == type(""):
		to_find = [to_find]
	for elmt in to_find:
		pos = body.find(elmt)
		if pos > -1:
			sentences = body.split(".")
			cur_pos = 0
			for sentence in sentences:
				cur_pos += len(sentence) + 1 # +1 for dot
				if pos <= cur_pos:
					snippets.append({
						"element"             : elmt,
						"context"             : sentence,
						"position"            : [pos, pos + len(elmt)],
						"position_in_context" : [sentence.find(elmt), sentence.find(elmt) + len(elmt)]
					})
	return snippets

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
