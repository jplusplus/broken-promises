#!/usr/bin/env python
# Encoding: utf-8
# -----------------------------------------------------------------------------
# Project : Broken Promises
# -----------------------------------------------------------------------------
# Author : Edouard Richard                                  <edou4rd@gmail.com>
# -----------------------------------------------------------------------------
# License : GNU General Public License
# -----------------------------------------------------------------------------
# Creation : 21-Nov-2013
# Last mod : 21-Nov-2013
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

from brokenpromises.operations import CollectArticles
from brokenpromises.worker     import worker
from brokenpromises.channels   import get_available_channels

import datetime

today = datetime.date.today()
dates = [(today.year, today.month, today.day)] #today

for day in range(1, 7):
	date = today + datetime.timedelta(days=day)
	dates.append((date.year, date.month, date.day))

for date in dates:
	collector = CollectArticles(get_available_channels(), *date, use_storage=True)
	worker.run(collector)

# EOF
