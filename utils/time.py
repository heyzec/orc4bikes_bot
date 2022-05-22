from datetime import timedelta, datetime

from admin import (
    BOT_GMT_OFFSET,
)

DEFAULT_FORMAT = "%Y/%m/%d, %H:%M:%S"

def to_readable_td(diff: timedelta):
    d = diff.days
    h = diff.seconds // 3600
    m = (diff.seconds % 3600) // 60
    s = (diff.seconds % 3600) % 60
    if diff.days:
        output = f"{d} days, {h} hours, {m} minutes and {s} seconds."
    else:
        output = f"{h} hours, {m} minutes and {s} seconds."
    return output

def now(gmt=None):
    if gmt is None:
        gmt = BOT_GMT_OFFSET
    return datetime.utcnow() + timedelta(hours=gmt)

def now_formatted(gmt=None, fmt=None):
    if fmt is None:
        fmt = DEFAULT_FORMAT
    return now(gmt).strftime(fmt)
