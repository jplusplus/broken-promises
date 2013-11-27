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
# Last mod : 12-Nov-2013
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

from models import Article, Report
import os
import importlib

ENVIRONMENT_VARIABLE = "BP_SETTINGS"

class Settings:

	def __init__(self):
			try:
				settings_module = os.environ[ENVIRONMENT_VARIABLE]
			except KeyError or not settings_module:
				raise Exception("Settings are not configured. You must define the environment variable '%s'" % (ENVIRONMENT_VARIABLE))
			mod = importlib.import_module(settings_module)
			for setting in dir(mod):
				if setting == setting.upper():
					setattr(self, setting, getattr(mod, setting))

	def __getitem__(self, name): return getattr(self, name)

settings = Settings()

# launch scheduled jobs
import rq
import datetime
from brokenpromises.worker     import worker
from rq_scheduler              import Scheduler
from brokenpromises.operations import CollectNext7days, CollectNext2Months, CollectNext2Years

rq.use_connection()  # Use RQ's default Redis connection
scheduler = Scheduler()
scheduled_jobs = scheduler.get_jobs()
# remove all jobs with interval
for job in scheduled_jobs:
	if job.meta.get('interval'):
		scheduler.cancel(job)

today = datetime.date.today()
next_midnight = today + datetime.timedelta(days=1)
next_midnight = datetime.datetime(next_midnight.year, next_midnight.month, next_midnight.day, 0, 10)

# collect all the week
all_the_days = 60 * 60 * 24
worker.schedule_with_interval(date=next_midnight, interval_s=all_the_days, collector=CollectNext7days())

# collect this month
all_the_2_weeks = all_the_days * 15
worker.schedule_with_interval(date=next_midnight, interval_s=all_the_2_weeks, collector=CollectNext2Months())

#collect this year and the next year
new_year = datetime.datetime(today.year + 1, 1, 1, 0, 20)
worker.schedule_with_interval(date=new_year, interval_s=31556926, collector=CollectNext2Years())

# EOF
