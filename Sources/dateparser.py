#!/usr/bin/env python
# Encoding: utf-8
# -----------------------------------------------------------------------------
# Project : Broken Promises
# -----------------------------------------------------------------------------
# Author : Edouard Richard                              <edouard@jplusplus.org>
# -----------------------------------------------------------------------------
# License : GNU General Public License
# -----------------------------------------------------------------------------
# Creation : 07-Nov-2013
# Last mod : 07-Nov-2013
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

# Inspired from https://code.google.com/p/nltk/source/browse/trunk/nltk_contrib/nltk_contrib/timex.py
import re

RE_NUMBERS  = "(^a(?=\s)|one|two|three|four|five|six|seven|eight|nine|ten|\
eleven|twelve|thirteen|fourteen|fifteen|sixteen|seventeen|\
eighteen|nineteen|twenty|thirty|forty|fifty|sixty|seventy|eighty|\
ninety|hundred|thousand)"
RE_DAY      = "(monday|tuesday|wednesday|thursday|friday|saturday|sunday)"
RE_MONTH    = "(?P<month>january|february|march|april|may|june|july|august|september|\
october|november|december|jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec)"
RE_DMY      = "(year|day|week|month)"
RE_REL_DAY  = "(today|yesterday|tomorrow|tonight|tonite)"
RE_EXP1     = "(before|after|earlier|later|ago)"
RE_EXP2     = "(this|next|last)"
RE_Y        = "(?P<year>(?<=\s)(19|20)\d\d|^(19|20)\d\d)"

# -----------------------------------------------------------------------------
#
#    ABSOLUTE DATES
#
# -----------------------------------------------------------------------------

# ISO -----------------------
# [X] 2013-10-3
# [X] 2013/10/3
RE_ISO1      = re.compile("(?P<year>[0-9]{4})[/-](?P<month>0[1-9]|1[0-2]|[1-9])[/-](?P<day>0[1-9]|[12][0-9]|3[01]|[1-9])")
# [X] 3-10-2013
# [X] 3/10/2013
RE_ISO2      = re.compile("(?P<day>0[1-9]|[12][0-9]|3[01]|[1-9])[/-](?P<month>0[1-9]|1[0-2]|[1-9])[/-](?P<year>[0-9]{4})")

# Full Dates ----------------
# [x] 3 October 2013
# [x] 3 October, 2013
# [X] 3 by October 2013
# [X] 3 by October, 2013
# [X] 3 in October 2013
# [X] 3 in October, 2013
# [X] 3 of October 2013
# [X] 3 of October, 2013
# [X] 3th October 2013
# [X] 3th by October 2013
# [X] 3th by October, 2013
# [X] 3th in October 2013
# [X] 3th in October, 2013
# [X] 3th of October 2013
# [X] 3th of October, 2013
RE_FULL_DATE1 = re.compile("(?<!\d)(?P<day>0[1-9]|[12][0-9]|3[01]|[1-9])(?:th)? (?:by |in |of )?" + RE_MONTH + "[,]? " + RE_Y, re.IGNORECASE)
# [X] October 3, 2013
# [X] October 3 2013
RE_FULL_DATE2 = re.compile(RE_MONTH + " (?P<day>0[1-9]|[12][0-9]|3[01]|[1-9])(?:th)?[,]? " + RE_Y, re.IGNORECASE)

# Month ---------------------
# [X] October 2013
# [X] October, 2013
RE_FULL_MONTH = re.compile(RE_MONTH + "[,]? " + RE_Y, re.IGNORECASE)

# Year ---------------------
# [X] 2013
RE_YEAR = re.compile(RE_Y, re.IGNORECASE)

# Hash function for months to simplify the grounding task.
# [Jan..Dec] -> [1..12]
HASH_MONTHS = {
    'january'   : 1,
    'jan'       : 1,
    'february'  : 2,
    'feb'       : 2,
    'march'     : 3,
    'mar'       : 3,
    'april'     : 4,
    'apr'       : 4,
    'may'       : 5,
    'may'       : 5,
    'june'      : 6,
    'jun'       : 6,
    'july'      : 7,
    'jul'       : 7,
    'august'    : 8,
    'aug'       : 8,
    'september' : 9,
    'sep'       : 9,
    'october'   : 10,
    'oct'       : 10,
    'november'  : 11,
    'nov'       : 11,
    'december'  : 12,
    'dec'       : 12,
}

def _parse_month(month):
    return HASH_MONTHS[month.lower()]

def get_date_obj(mx_date):
    return (mx_date.year, mx_date.month, mx_date.day)

def find_dates(text, base_date=None):
    """

    If base_date is given, returns the parsed dates

    """
    dates_found = []

    def already_full_parsed(this_row, this_pos):
        for date_obj, date_row, date_pos in dates_found:
            if this_pos[0]      >= date_pos[0] \
                and this_pos[1] <= date_pos[1] \
                and this_row    in date_row:
                return True
        return False

    def find_regex(regex, infos):
        for date in regex.finditer(text):
            date_row = date.group()
            if already_full_parsed(date_row, date.span()):
                continue
            date_obj = {
                "day"   : None,
                "month" : None,
                "year"  : None
            }
            for key, parser in infos:
                date_obj[key] = parser(date.group(key))
            dates_found.append(
                (
                    (date_obj['year'], date_obj['month'], date_obj['day']),
                    date_row, date.span()
                )
            )

    find_regex(RE_FULL_DATE1, (
        ("day"   , int),
        ("month" , _parse_month),
        ("year"  , int)
    ))
    find_regex(RE_FULL_DATE2, (
        ("day"   , int),
        ("month" , _parse_month),
        ("year"  , int)
    ))
    find_regex(RE_ISO1, (
        ("day"   , int),
        ("month" , int),
        ("year"  , int)
    ))
    find_regex(RE_ISO2, (
        ("month" , int),
        ("year"  , int),
        ("day"   , int)
    ))
    find_regex(RE_FULL_MONTH, (
        ("month" , _parse_month),
        ("year"  , int)
    ))
    find_regex(RE_YEAR, (
        ("year"  , int),
    ))

    return dates_found

# EOF
