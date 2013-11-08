#!/usr/bin/env python
# Encoding: utf-8
# -----------------------------------------------------------------------------
# Project : Broken Promises
# -----------------------------------------------------------------------------
# Author : Steven Bird                                 <sb@csse.unimelb.edu.au>
#          Edward Loper                        <edloper@gradient.cis.upenn.edu>
#          Ewan Klein                                       <ewan@inf.ed.ac.uk>
#          Edouard Richard                              <edouard@jplusplus.org>
# -----------------------------------------------------------------------------
# License : Copyright (C) 2001-2011 NLTK Project
#  
#  Licensed under the Apache License, Version 2.0 (the 'License');
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#  
#     http://www.apache.org/licenses/LICENSE-2.0
#  
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an 'AS IS' BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.
# -----------------------------------------------------------------------------
# Creation : 05-Nov-2013
# Last mod : 08-Nov-2013
# -----------------------------------------------------------------------------
# From https://code.google.com/p/nltk/source/browse/trunk/nltk_contrib/nltk_contrib/timex.py

import re
# Requires eGenix.com mx Base Distribution
# http://www.egenix.com/products/python/mxBase/
# import mx.DateTime

# Predefined strings.
RE_NUMBERS  = "(^a(?=\s)|one|two|three|four|five|six|seven|eight|nine|ten|\
eleven|twelve|thirteen|fourteen|fifteen|sixteen|seventeen|\
eighteen|nineteen|twenty|thirty|forty|fifty|sixty|seventy|eighty|\
ninety|hundred|thousand)"
RE_DAY      = "(monday|tuesday|wednesday|thursday|friday|saturday|sunday)"
RE_WEEK_DAY = "(monday|tuesday|wednesday|thursday|friday|saturday|sunday)"
RE_MONTH    = "(?P<month>january|february|march|april|may|june|july|august|september|\
october|november|december|jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec)"
RE_DMY      = "(year|day|week|month)"
RE_REL_DAY  = "(today|yesterday|tomorrow|tonight|tonite)"
RE_EXP1     = "(before|after|earlier|later|ago)"
RE_EXP2     = "(this|next|last)"
RE_Y        = "(?P<year>(?<=\s)(19|20)\d\d|^(19|20)\d\d)"
RE_REGXP1   = "((\d+|(" + RE_NUMBERS + "[-\s]?)+) " + RE_DMY + "s? " + RE_EXP1 + ")"
RE_REGXP2   = "(" + RE_EXP2 + " (" + RE_DMY + "|" + RE_WEEK_DAY + "|" + RE_MONTH + "))"

# -----------------------------------------------------------------------------
#
#    ABSOLUTE DATES
#
# -----------------------------------------------------------------------------

# ISO -----------------------
# [X] 2013-10-3
# [X] 2013/10/3
RE_ISO1      = re.compile("(?P<year>[0-9]{4})[/-](?P<month>[0-9]{2})[/-](?P<day>[0-9]{2})")
# [X] 3-10-2013
# [X] 3/10/2013
RE_ISO2      = re.compile("(?P<day>[0-9]{2})[/-](?P<month>[0-9]{2})[/-](?P<year>[0-9]{4})")

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
RE_FULL_DATE = re.compile("(?<!\d)(?P<day>\d{1,2})(?:th)? (?:by |in |of )?" + RE_MONTH + "[,]? " + RE_Y, re.IGNORECASE)

# Month ---------------------
# [X] October 2013
# [X] October, 2013
RE_FULL_MONTH = re.compile(RE_MONTH + "[,]? " + RE_Y, re.IGNORECASE)

# Year ---------------------
# [X] 2013
RE_YEAR = re.compile(RE_Y, re.IGNORECASE)

# REG1 = re.compile(RE_REGXP1, re.IGNORECASE)
# REG2 = re.compile(RE_REGXP2, re.IGNORECASE)
# REG3 = re.compile(RE_REL_DAY, re.IGNORECASE)
# REG4 = re.compile(RE_ISO)
# REG5 = re.compile(RE_Y)
# FULL_DATE = re.compile(FULL_DATE, re.IGNORECASE)
# REGS = (REG1,REG2,REG3,REG4,REG5,REG6)
# REGS = (REG6,)

# Hash function for week days to simplify the grounding task.
# [Mon..Sun] -> [0..6]
HASH_WEEK_DAYS = {
    'Monday'    : 0,
    'Tuesday'   : 1,
    'Wednesday' : 2,
    'Thursday'  : 3,
    'Friday'    : 4,
    'Saturday'  : 5,
    'Sunday'    : 6
}

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

    find_regex(RE_FULL_DATE, (
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

# def __hash_num(number):
#     """

#     Hash number in words into the corresponding integer value

#     """

#     if re.match(r'one|^a\b' , number, re.IGNORECASE): return 1
#     if re.match(r'two'      , number, re.IGNORECASE): return 2
#     if re.match(r'three'    , number, re.IGNORECASE): return 3
#     if re.match(r'four'     , number, re.IGNORECASE): return 4
#     if re.match(r'five'     , number, re.IGNORECASE): return 5
#     if re.match(r'six'      , number, re.IGNORECASE): return 6
#     if re.match(r'seven'    , number, re.IGNORECASE): return 7
#     if re.match(r'eight'    , number, re.IGNORECASE): return 8
#     if re.match(r'nine'     , number, re.IGNORECASE): return 9
#     if re.match(r'ten'      , number, re.IGNORECASE): return 10
#     if re.match(r'eleven'   , number, re.IGNORECASE): return 11
#     if re.match(r'twelve'   , number, re.IGNORECASE): return 12
#     if re.match(r'thirteen' , number, re.IGNORECASE): return 13
#     if re.match(r'fourteen' , number, re.IGNORECASE): return 14
#     if re.match(r'fifteen'  , number, re.IGNORECASE): return 15
#     if re.match(r'sixteen'  , number, re.IGNORECASE): return 16
#     if re.match(r'seventeen', number, re.IGNORECASE): return 17
#     if re.match(r'eighteen' , number, re.IGNORECASE): return 18
#     if re.match(r'nineteen' , number, re.IGNORECASE): return 19
#     if re.match(r'twenty'   , number, re.IGNORECASE): return 20
#     if re.match(r'thirty'   , number, re.IGNORECASE): return 30
#     if re.match(r'forty'    , number, re.IGNORECASE): return 40
#     if re.match(r'fifty'    , number, re.IGNORECASE): return 50
#     if re.match(r'sixty'    , number, re.IGNORECASE): return 60
#     if re.match(r'seventy'  , number, re.IGNORECASE): return 70
#     if re.match(r'eighty'   , number, re.IGNORECASE): return 80
#     if re.match(r'ninety'   , number, re.IGNORECASE): return 90
#     if re.match(r'hundred'  , number, re.IGNORECASE): return 100
#     if re.match(r'thousand' , number, re.IGNORECASE): return 1000


# # def ground(tagged_text, base_date):
# def parse_dates(dates, base_date):
#     """

#     Given a timex_tagged_text and a Date object set to base_date,
#     returns timex_grounded_text

#     """

#     for date, position in dates:
        
#         date_val = 'UNKNOWN' # Default value

#         date_ori = date   # Backup original date for later substitution

#         # If numbers are given in words, hash them into corresponding numbers.
#         # eg. twenty five days ago --> 25 days ago
#         if re.search(RE_NUMBERS, date, re.IGNORECASE):
#             split_date = re.split(r'\s(?=days?|months?|years?|weeks?)', \
#                                                               date, re.IGNORECASE)
#             value = split_date[0]
#             unit = split_date[1]
#             num_list = map(lambda s:__hash_num(s),re.findall(RE_NUMBERS + '+', \
#                                           value, re.IGNORECASE))
#             date = `sum(num_list)` + ' ' + unit

#         # If date matches ISO format, remove 'time' and reorder 'date'
#         if re.match(r'\d+[/-]\d+[/-]\d+ \d+:\d+:\d+\.\d+', date):
#             dmy = re.split(r'\s', date)[0]
#             dmy = re.split(r'/|-', dmy)
#             date_val = str(dmy[2]) + '-' + str(dmy[1]) + '-' + str(dmy[0])

#         # Specific dates
#         elif re.match(r'\d{4}', date):
#             date_val = str(date)

#         # Relative dates
#         elif re.match(r'tonight|tonite|today', date, re.IGNORECASE):
#             date_val = str(base_date)
#         elif re.match(r'yesterday', date, re.IGNORECASE):
#             date_val = str(base_date + mx.DateTime.RelativeDateTime(days=-1))
#         elif re.match(r'tomorrow', date, re.IGNORECASE):
#             date_val = str(base_date + mx.DateTime.RelativeDateTime(days=+1))

#         # Weekday in the previous week.
#         elif re.match(r'last ' + RE_WEEK_DAY, date, re.IGNORECASE):
#             day = HASH_WEEK_DAYS[date.split()[1]]
#             date_val = str(base_date + mx.DateTime.RelativeDateTime(weeks=-1, \
#                             weekday=(day,0)))

#         # Weekday in the current week.
#         elif re.match(r'this ' + RE_WEEK_DAY, date, re.IGNORECASE):
#             day = HASH_WEEK_DAYS[date.split()[1]]
#             date_val = str(base_date + mx.DateTime.RelativeDateTime(weeks=0, \
#                             weekday=(day,0)))

#         # Weekday in the following week.
#         elif re.match(r'next ' + RE_WEEK_DAY, date, re.IGNORECASE):
#             day = HASH_WEEK_DAYS[date.split()[1]]
#             date_val = str(base_date + mx.DateTime.RelativeDateTime(weeks=+1, \
#                               weekday=(day,0)))

#         # Last, this, next week.
#         elif re.match(r'last week', date, re.IGNORECASE):
#             year = (base_date + mx.DateTime.RelativeDateTime(weeks=-1)).year

#             # iso_week returns a triple (year, week, day) hence, retrieve
#             # only week value.
#             week = (base_date + mx.DateTime.RelativeDateTime(weeks=-1)).iso_week[1]
#             date_val = str(year) + 'W' + str(week)
#         elif re.match(r'this week', date, re.IGNORECASE):
#             year = (base_date + mx.DateTime.RelativeDateTime(weeks=0)).year
#             week = (base_date + mx.DateTime.RelativeDateTime(weeks=0)).iso_week[1]
#             date_val = str(year) + 'W' + str(week)
#         elif re.match(r'next week', date, re.IGNORECASE):
#             year = (base_date + mx.DateTime.RelativeDateTime(weeks=+1)).year
#             week = (base_date + mx.DateTime.RelativeDateTime(weeks=+1)).iso_week[1]
#             date_val = str(year) + 'W' + str(week)

#         # # Month in the previous year.
#         # elif re.match(r'last ' + month, date, re.IGNORECASE):
#         #     month = HASH_MONTHS[date.split()[1]]
#         #     date_val = str(base_date.year - 1) + '-' + str(month)

#         # # Month in the current year.
#         # elif re.match(r'this ' + month, date, re.IGNORECASE):
#         #     month = HASH_MONTHS[date.split()[1]]
#         #     date_val = str(base_date.year) + '-' + str(month)

#         # # Month in the following year.
#         # elif re.match(r'next ' + month, date, re.IGNORECASE):
#         #     month = HASH_MONTHS[date.split()[1]]
#         #     date_val = str(base_date.year + 1) + '-' + str(month)
#         elif re.match(r'last month', date, re.IGNORECASE):

#             # Handles the year boundary.
#             if base_date.month == 1:
#                 date_val = str(base_date.year - 1) + '-' + '12'
#             else:
#                 date_val = str(base_date.year) + '-' + str(base_date.month - 1)
#         elif re.match(r'this month', date, re.IGNORECASE):
#                 date_val = str(base_date.year) + '-' + str(base_date.month)
#         elif re.match(r'next month', date, re.IGNORECASE):

#             # Handles the year boundary.
#             if base_date.month == 12:
#                 date_val = str(base_date.year + 1) + '-' + '1'
#             else:
#                 date_val = str(base_date.year) + '-' + str(base_date.month + 1)
#         elif re.match(r'last year', date, re.IGNORECASE):
#             date_val = str(base_date.year - 1)
#         elif re.match(r'this year', date, re.IGNORECASE):
#             date_val = str(base_date.year)
#         elif re.match(r'next year', date, re.IGNORECASE):
#             date_val = str(base_date.year + 1)
#         elif re.match(r'\d+ days? (ago|earlier|before)', date, re.IGNORECASE):

#             # Calculate the offset by taking '\d+' part from the date.
#             offset = int(re.split(r'\s', date)[0])
#             date_val = str(base_date + mx.DateTime.RelativeDateTime(days=-offset))
#         elif re.match(r'\d+ days? (later|after)', date, re.IGNORECASE):
#             offset = int(re.split(r'\s', date)[0])
#             date_val = str(base_date + mx.DateTime.RelativeDateTime(days=+offset))
#         elif re.match(r'\d+ weeks? (ago|earlier|before)', date, re.IGNORECASE):
#             offset = int(re.split(r'\s', date)[0])
#             year = (base_date + mx.DateTime.RelativeDateTime(weeks=-offset)).year
#             week = (base_date + \
#                             mx.DateTime.RelativeDateTime(weeks=-offset)).iso_week[1]
#             date_val = str(year) + 'W' + str(week)
#         elif re.match(r'\d+ weeks? (later|after)', date, re.IGNORECASE):
#             offset = int(re.split(r'\s', date)[0])
#             year = (base_date + mx.DateTime.RelativeDateTime(weeks=+offset)).year
#             week = (base_date + mx.DateTime.RelativeDateTime(weeks=+offset)).iso_week[1]
#             date_val = str(year) + 'W' + str(week)
#         elif re.match(r'\d+ months? (ago|earlier|before)', date, re.IGNORECASE):
#             extra = 0
#             offset = int(re.split(r'\s', date)[0])

#             # Checks if subtracting the remainder of (offset / 12) to the base month
#             # crosses the year boundary.
#             if (base_date.month - offset % 12) < 1:
#                 extra = 1

#             # Calculate new values for the year and the month.
#             year = str(base_date.year - offset // 12 - extra)
#             month = str((base_date.month - offset % 12) % 12)

#             # Fix for the special case.
#             if month == '0':
#                 month = '12'
#             date_val = year + '-' + month
#         elif re.match(r'\d+ months? (later|after)', date, re.IGNORECASE):
#             extra = 0
#             offset = int(re.split(r'\s', date)[0])
#             if (base_date.month + offset % 12) > 12:
#                 extra = 1
#             year = str(base_date.year + offset // 12 + extra)
#             month = str((base_date.month + offset % 12) % 12)
#             if month == '0':
#                 month = '12'
#             date_val = year + '-' + month
#         elif re.match(r'\d+ years? (ago|earlier|before)', date, re.IGNORECASE):
#             offset = int(re.split(r'\s', date)[0])
#             date_val = str(base_date.year - offset)
#         elif re.match(r'\d+ years? (later|after)', date, re.IGNORECASE):
#             offset = int(re.split(r'\s', date)[0])
#             date_val = str(base_date.year + offset)

#         # Remove 'time' from date_val.
#         # For example, If date_val = 2000-02-20 12:23:34.45, then
#         # date_val = 2000-02-20
#         date_val = re.sub(r'\s.*', '', date_val)

#         # # Substitute tag+date in the text with grounded tag+date.
#         # tagged_text = re.sub('<date2>' + date_ori + '</date2>', '<date2 val=\"' \
#         #     + date_val + '\">' + date_ori + '</date2>', tagged_text)

#     return tagged_text

####
# def demo():
#     text = "\n".join(open("text.txt").readlines()[:1000])
#     for date in find_dates(text, mx.DateTime.today()):
#         print date
    # print ground(tag(text), mx.DateTime.today())

# if __name__ == '__main__':
#     demo()

# EOF
