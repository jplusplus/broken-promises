#!/usr/bin/env python
# Encoding: utf-8
# -----------------------------------------------------------------------------
# Project : Broken Promises
# -----------------------------------------------------------------------------
# Author : Edouard Richard                                  <edou4rd@gmail.com>
# -----------------------------------------------------------------------------
# License : GNU General Public License
# -----------------------------------------------------------------------------
# Creation : 12-Nov-2013
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

import os

BP_CHANNEL_GUARDIAN_API_KEY = os.environ['BP_CHANNEL_GUARDIAN_API_KEY']
BP_CHANNEL_NYTIMES_API_KEY  = os.environ['BP_CHANNEL_NYTIMES_API_KEY']

MONGODB_URI = os.getenv("MONGOLAB_URI", "mongodb://localhost/broken-promises")

REDIS_URL = os.getenv("REDISCLOUD_URL", "redis://localhost:6379")

# set cache for http requests
import requests_cache
from pymongo import MongoClient
requests_cache.install_cache(MONGODB_URI.split("/")[-1], backend='mongodb', connection=MongoClient(MONGODB_URI), expire_after=345600)

# EOF
