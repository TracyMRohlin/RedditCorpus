__author__ = 'tracyrohlin'

import datetime
import time
import os

def make_time_interval(firstdate):
    end_point = firstdate - 1
    start_point = end_point - (360 * 24 * 7 * 240)
    return start_point, end_point

def extract_date(filepath):
    """Returns a tuple of the starting and ending point for time stamp searching on Reddit."""

    # Initially set the date to be 1 year to six months previously based on the fact that Reddit closes voting on those
    # posts older than six months
    pattern = "%Y-%m-%d"
    date_six_months_ago = str(datetime.datetime.utcnow() - datetime.timedelta(days=180)).split(" ")[0]
    last = datetime.datetime.strptime(date_six_months_ago, pattern)
    date_year_ago = str(last - datetime.timedelta(days=365)).split(" ")[0]
    # convert to epoch time
    end_point = int(time.mktime(time.strptime(date_six_months_ago, pattern)))
    start_point = int(time.mktime(time.strptime(date_year_ago, pattern)))

    try:
        os.chdir(filepath)
    except:
        return start_point, end_point

    try:
        dates = []
        for file in os.listdir("."):
            if not str(file).endswith("txt"):
                continue
            with open(file) as f:
                text = f.read().split()
                i = text.index('Date:')
                date = int(float(text[i+1]))
                dates.append(date)
        # receives the oldest date from the text files and sets the endtime to one second before that
        # then the start set is set to 6 months previous
        start_point, end_point = make_time_interval(min(dates))
        return start_point, end_point

    except:
        return start_point, end_point



