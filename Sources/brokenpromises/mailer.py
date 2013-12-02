#!/usr/bin/env python
# Encoding: utf-8
# -----------------------------------------------------------------------------
# Project : Broken Promises
# -----------------------------------------------------------------------------
# Author : Edouard Richard                                  <edou4rd@gmail.com>
# -----------------------------------------------------------------------------
# License : GNU General Public License
# -----------------------------------------------------------------------------
# Creation : 25-Sep-2013
# Last mod : 25-Sep-2013
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

import mandrill
from brokenpromises import settings

mandrill_client = mandrill.Mandrill(settings.MANDRILL_APIKEY)

def send_email(to, subject="", body="", send_from=None):
	send_from = send_from or "noreply@brokenpromises.org"
	if type(to) in (str, unicode):
		to = [{"email":to}]
	else:
		to = [{"email":_} for _ in to]
	message = {
	'from_email' : send_from,
	'from_name'  : 'Broken-Promises',
	'to'         : to,
	'subject'    : subject,
	'text'       : body,
	}
	mandrill_client.messages.send(message=message, async=True)
	pass

# -----------------------------------------------------------------------------
#
# TESTS
#
# -----------------------------------------------------------------------------
import unittest

class TestMailer(unittest.TestCase):
	'''Test Class'''

	def test_send_mail(self):
		send_email("ed.ou4rd@gmail.com", "coucou", "ça roule?", "edou4rd@gmail.com")

if __name__ == "__main__":
	# unittest.main()
	suite = unittest.TestLoader().loadTestsFromTestCase(TestMailer)
	unittest.TextTestRunner(verbosity=2).run(suite)
# EOF
