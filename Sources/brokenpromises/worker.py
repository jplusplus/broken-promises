#!/usr/bin/env python
# Encoding: utf-8
# -----------------------------------------------------------------------------
# Project : Broken Promises
# -----------------------------------------------------------------------------
# Author : Edouard Richard                                  <edou4rd@gmail.com>
# -----------------------------------------------------------------------------
# License : GNU General Public License
# -----------------------------------------------------------------------------
# Creation : 20-Nov-2013
# Last mod : 20-Nov-2013
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

from brokenpromises import settings
import datetime
import calendar

class RedisWorker(object):
	TIMEOUT    = settings.JOB_TIMEOUT
	FREQUENCES = ["hourly", "daily", "weekly", "monthly", "yearly"]

	def __init__(self):
		import rq
		import redis
		from   rq_scheduler import Scheduler
		self.conn       = redis.from_url(settings.REDIS_URL)
		self.queue      = rq.Queue("default", connection=self.conn, default_timeout=RedisWorker.TIMEOUT)
		self.scheduler  = Scheduler("high"  , connection=self.conn)

	def run(self, collector, **kwargs):
		class_name       = "%s.%s" % (collector.__class__.__module__, collector.__class__.__name__)
		collector_params = collector.get_params()
		return self.queue.enqueue(collector.run, collector=class_name, params=collector_params, **kwargs)

	def schedule_with_interval(self, date, interval_s, collector, *arg, **kwargs):
		date   = date or datetime.datetime.now()
		kwargs.update({
			"collector" : "%s.%s" % (collector.__class__.__module__, collector.__class__.__name__),
			"params"    : collector.get_params()
		})
		res  = self.scheduler.schedule(
			scheduled_time = date,           # Time for first execution
			func           = collector.run,  # Function to be queued
			args           = arg,            # Arguments passed into function when executed
			kwargs         = kwargs,         # Keyword arguments passed into function when executed
			interval       = interval_s,     # Time before the function is called again, in seconds
			repeat         = None,           # Repeat this number of times (None means repeat forever)
			timeout        = RedisWorker.TIMEOUT
		)
		return res

	def schedule_periodically(self, date, frequence, collector, *arg, **kwargs):
		from brokenpromises.worker import RunAndReplaceIntTheQueuePeriodically
		assert frequence in RedisWorker.FREQUENCES, "frequence %s unknown."
		if frequence == "hourly":
			next_date = date + datetime.timedelta(hours=1)
		if frequence == "daily":
			next_date = date + datetime.timedelta(days=1)
		if frequence == "weekly":
			next_date = date + datetime.timedelta(weeks=1)
		if frequence == "monthly":
			year      = date.year + (date.month + 1) / 12
			month     = date.month % 12 + 1
			day       = min(date.day, calendar.monthrange(year, month)[1])
			next_date = datetime.datetime(year, month, day, date.hour, date.minute, date.second)
		if frequence == "yearly":
			year      = date.year + 1
			day       = min(date.day, calendar.monthrange(year, date.month)[1])
			next_date = datetime.datetime(year, date.month, day, date.hour, date.minute, date.second)
		self.schedule(date, RunAndReplaceIntTheQueuePeriodically(next_date, frequence, collector), *arg, **kwargs)

	def schedule(self, date, collector, *arg, **kwargs):
		res    = None
		kwargs = kwargs.update({
			"collector" : "%s.%s" % (collector.__class__.__module__, collector.__class__.__name__),
			"params"    : collector.get_params()
		})
		if type(date) is datetime.timedelta:
			res = self.scheduler.enqueue_in(date, collector.run, *arg, **kwargs)

		elif type(date) is datetime.datetime:
			res = self.scheduler.enqueue_at(date, collector.run, *arg, **kwargs)
		return res

worker = RedisWorker()

class RunAndReplaceIntTheQueuePeriodically(object):
	""" Wrapper for perodic collector """

	def __init__(self, collector, next_date):
		self.collector = collector

	def run(self, **kwargs):
		worker.schedule_periodically(self.next_date, self.frequence, self.collector)
		self.collector.run()

# EOF
