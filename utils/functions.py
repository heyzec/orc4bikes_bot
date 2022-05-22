from decimal import Decimal

from admin import (
    BOT_DEDUCT_RATE,
)

def calc_deduct(time_diff):
    """Calculate credits deductable given a time period."""
    deduction = time_diff.seconds // BOT_DEDUCT_RATE + int(time_diff.seconds % BOT_DEDUCT_RATE > 0)
    deduction += time_diff.days * 86400 / BOT_DEDUCT_RATE
    return Decimal(deduction)
