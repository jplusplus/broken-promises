#!/usr/bin/env python
# Encoding: utf-8
# -----------------------------------------------------------------------------
# Project : Broken Promises
# -----------------------------------------------------------------------------
# Author : Edouard Richard                                  <edou4rd@gmail.com>
# -----------------------------------------------------------------------------
# License : GNU General Public License
# -----------------------------------------------------------------------------
# Creation : 29-Oct-2013
# Last mod : 30-Oct-2013
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

from flask import Flask, render_template, request, send_file, \
	send_from_directory, Response, abort, session, redirect, url_for, make_response
from flask.ext.assets import Environment
from rq_dashboard import RQDashboard
from eve import Eve
import os
import json

class CustomFlask(Eve):
	jinja_options = Flask.jinja_options.copy()
	jinja_options.update(dict(
		block_start_string    = '[%',
		block_end_string      = '%]',
		variable_start_string = '[[',
		variable_end_string   = ']]',
		comment_start_string  = '[#',
		comment_end_string    = '#]'))

app = CustomFlask(__name__, 
	settings = os.path.join(os.path.abspath(os.path.dirname(__file__)), "settings.py")
)
RQDashboard(app)

assets = Environment(app)
# -----------------------------------------------------------------------------
#
# Site pages
#
# -----------------------------------------------------------------------------
@app.route('/ui')
def index():
	response = make_response(render_template('home.html'))
	return response

@app.route("/register_collection", methods=['post'])
def register_collection():
	return json.dumps({"status": "ok"})

# -----------------------------------------------------------------------------
#
# Main
#
# -----------------------------------------------------------------------------
if __name__ == '__main__':
	import os
	app.run(
		extra_files=[os.path.join(os.path.dirname(__file__), "settings.py")]
	)

# EOF
