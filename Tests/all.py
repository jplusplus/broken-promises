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
# Last mod : 29-Oct-2013
# -----------------------------------------------------------------------------

import unittest

if __name__ == "__main__":
	tests = unittest.TestLoader().discover("brokenpromises", "*.py")
	unittest.TextTestRunner(verbosity=2).run(tests)

# EOF
