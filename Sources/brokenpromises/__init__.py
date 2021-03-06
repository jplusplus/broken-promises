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
import datetime
from brokenpromises.worker     import worker
from rq_scheduler              import Scheduler
from brokenpromises.operations import CollectNext7days, CollectNext2Months, CollectNext2Years, CollectToday, MrClean
import redis
conn           = redis.from_url(settings.REDIS_URL)
scheduler      = Scheduler(connection=conn)
scheduled_jobs = scheduler.get_jobs()
# remove all jobs with interval
for job in scheduled_jobs:
	if "RunAndReplaceIntTheQueuePeriodically" in job.description:
		scheduler.cancel(job)

today = datetime.datetime.now()
# net midnight
next_midnight = today + datetime.timedelta(days=1)
next_midnight = datetime.datetime(next_midnight.year, next_midnight.month, next_midnight.day, 0, 10)
# next month
year          = today.year + (today.month + 1) / 12
month         = today.month % 12 + 1
next_month    = datetime.datetime(year, month, 1, 0, 10)
#next new year
next_year     = datetime.datetime(today.year + 1, 1, 1, 0, 20)

# enqueue periodic jobs
worker.schedule_periodically(date=next_midnight, frequence="daily"  , collector=CollectToday())
worker.schedule_periodically(date=next_midnight, frequence="daily"  , collector=CollectNext7days())
worker.schedule_periodically(date=next_midnight, frequence="daily"  , collector=MrClean())
worker.schedule_periodically(date=next_month   , frequence="monthly", collector=CollectNext2Months())
worker.schedule_periodically(date=next_year    , frequence="yearly" , collector=CollectNext2Years())

# EOF
