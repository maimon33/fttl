import re

from datetime import datetime, timedelta

import click
from click_didyoumean import DYMGroup

def get_datetime(minutes):
    return datetime.now() + timedelta(minutes=minutes)

def convert_datetime_to_cron(requested_date):
    return requested_date.strftime("%M %H %d %m *")

def convert_to_int_and_strip_non_numeric(ttl):
    return int(re.sub('[^0-9]','', ttl))

def match_time_frame(ttl):
    if re.search("h", ttl):
        return convert_to_int_and_strip_non_numeric(ttl) * 60
    elif re.search("d", ttl):
        return convert_to_int_and_strip_non_numeric(ttl) * 1440
    elif re.search("w", ttl):
        return convert_to_int_and_strip_non_numeric(ttl) * 10080


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
    ttl = match_time_frame(ttl)
    print convert_datetime_to_cron(get_datetime(ttl))