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

import os
# import brokenpromises.operations
# from brokenpromises.operations import CollectArticles

class RedisWorker(object):

	def __init__(self):
		import rq
		import redis
		conn       = redis.from_url(os.getenv('REDISTOGO_URL', 'redis://localhost:6379'))
		self.queue = rq.Queue(connection=conn)

	def run(self, job, *arg, **kwargs):
		return self.queue.enqueue(job.run, *arg, **kwargs)

class SimpleWorker(object):

	def __init__(self):
		pass

	def run(self, job, *arg, **kwargs):
		return job.run(*arg, **kwargs)

worker = RedisWorker()

# EOF
