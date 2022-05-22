"""
Provides data manipulation methods here
"""

from decimal import Decimal
import json
import logging
import requests
from warnings import filterwarnings

from admin import (
    BOT_ENV,
    LOGGING_URL,
)

logger = logging.getLogger()

# See https://tinyurl.com/yuh2jzp3
filterwarnings(action='ignore', message=r'.*CallbackQueryHandler')

class DecimalEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Decimal):
            return float(obj)
        super().default(obj)  # Let the json module throw the error

def float_to_decimal(obj):
    """DynamoDB require Decimal in place of float"""
    return json.loads(json.dumps(obj, cls=DecimalEncoder), parse_float=Decimal)

def decimal_to_float(obj):
    return json.loads(json.dumps(obj, cls=DecimalEncoder))


def update_rental_log(update_list):
    """Updates rental logs with headers:
       bike,username,start_time,end_time
    """
    file = 'rental' if BOT_ENV == 'production' else 'testing'

    data = decimal_to_float(update_list)
    requests.post(f"{LOGGING_URL}?file={file}", json=data)

def update_report_log(update_list):
    """Updates report logs with headers:
       username,time,report
    """
    file = 'report' if BOT_ENV == 'production' else 'testing'
    data = decimal_to_float(update_list)
    requests.post(f"{LOGGING_URL}?file={file}", json=data)

def update_finance_log(update_list):
    """Updates finance logs with headers:
       username,time,initial_amt,change_amt,final_amt
    """
    file = 'finance' if BOT_ENV == 'production' else 'testing'
    data = decimal_to_float(update_list)
    requests.post(f"{LOGGING_URL}?file={file}", json=data)
