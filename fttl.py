import os
import re
import sys
import psutil
import fileinput
import subprocess

from os.path import expanduser
from datetime import datetime, timedelta

import click

DEFAULT_FILE = '{}/.fttl'.format(expanduser("~"))

def get_datetime(minutes):
    return datetime.now() + timedelta(minutes=minutes)

def convert_datetime_to_cron(requested_date):
    return requested_date.strftime("%M %H %d %m *")

def return_digits(ttl):
    return int(re.sub('[^0-9]','', ttl))

def convert_to_minutes(ttl):
    if re.match("\d+[h,H]$", ttl):
        return return_digits(ttl) * 60
    elif re.match("\d+[d,D]$", ttl):
        return return_digits(ttl) * 1440
    elif re.match("\d+[w,W]$", ttl):
        return return_digits(ttl) * 10080
    elif ttl.isdigit():
        return int(ttl)
    else:
        print """Bad request!
##########################################################
Options for life expectancy are limited.
You can use h, d, w or none for minutes
##########################################################"""
        sys.exit()


CLICK_CONTEXT_SETTINGS = dict(
    help_option_names=['-h', '--help'],
    token_normalize_func=lambda param: param.lower(),
    ignore_unknown_options=True)
    
@click.command(context_settings=CLICK_CONTEXT_SETTINGS)
@click.option('-t',
              '--ttl',
              default='48h',
              help="File Life Expectancy in Minutes\n"
              "Default to 48 Hours")
@click.argument('path', 
                default=DEFAULT_FILE)
def fttl(path, ttl):
    """Set life Expectancy for files in minutes.

    \b
    Use *h for Hours, *d for days, *w for weeks.
    PATH where to place your file.
    
    Defaults to `~/.fttl`
    """

    # Handle File expectancy duration limitation and tranlation
    ttl = convert_to_minutes(ttl)
    if ttl >= 525600:
        print "File TTL cannot exceed one year"
        sys.exit()
    # File Creation section
    path = sys.argv[1]
    if os.path.isfile(path):
        if click.confirm('File Exists!\nDo you want to overwrite it?',
                         default=True):
                             open(path, 'a').close()
    else:
        open(path, 'a').close()
    # print convert_datetime_to_cron(get_datetime(ttl))
    # if __name__ == '__main__':
    # print path