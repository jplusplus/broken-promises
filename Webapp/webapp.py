#!/usr/bin/env python
# Encoding: utf-8
# -----------------------------------------------------------------------------
# Project : Broken Promises
# -----------------------------------------------------------------------------
# Author : Edouard Richard                                  <edou4rd@gmail.com>
# -----------------------------------------------------------------------------
# License : proprietary journalism++
# -----------------------------------------------------------------------------
# Creation : 29-Oct-2013
# Last mod : 30-Oct-2013
# -----------------------------------------------------------------------------
from flask import Flask, render_template, request, send_file, \
	send_from_directory, Response, abort, session, redirect, url_for, make_response
from flask.ext.assets import Environment
from eve import Eve
import os

class CustomFlask(Eve):
	jinja_options = Flask.jinja_options.copy()
	jinja_options.update(dict(
		block_start_string    = '[%',
		block_end_string      = '%]',
		variable_start_string = '[[',
		variable_end_string   = ']]',
		comment_start_string  = '[#',
		comment_end_string    = '#]',
	))

app = CustomFlask(__name__, 
	settings = os.path.join(os.path.abspath(os.path.dirname(__file__)), "settings.py")
)
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
