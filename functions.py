from datetime import timedelta, datetime
from decimal import Decimal

from admin import (
    BOT_DEDUCT_RATE,
    BOT_GMT_OFFSET,
)


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

def calc_deduct(time_diff):
    """Calculate credits deductable given a time period."""
    deduction = time_diff.seconds // BOT_DEDUCT_RATE + int(time_diff.seconds % BOT_DEDUCT_RATE > 0)
    deduction += time_diff.days * 86400 / BOT_DEDUCT_RATE
    return Decimal(deduction)
