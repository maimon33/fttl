import re
import sys

from datetime import datetime, timedelta

import click

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
Options for life expectancy are limited.
You can use h, d, w or none for minutes"""
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
def fttl(ttl):
    """Set life Expectancy for files in minutes.
    Use *h for Hours, *d for days, *w for weeks. 
    """
    ttl = convert_to_minutes(ttl)
    if ttl >= 525600:
        print "File TTL cannot exceed one year"
        sys.exit()
    print convert_datetime_to_cron(get_datetime(ttl))