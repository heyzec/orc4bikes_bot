from datetime import datetime
import logging

from utils.functions import (
    calc_deduct,
    now,
    to_readable_td,
)
from database import (
    get_bikes,
    get_user,
    get_user_id,
)


logger = logging.getLogger()


def reminder(context):
    """Callback Reminder for return, every hour"""
    bikes_data = get_bikes()
    for bike_data in bikes_data:
        username = bike_data['username']
        if not username:
            continue

        chat_id = get_user_id(username)
        user_data = get_user(username=username)
        status = user_data['status']
        start = datetime.fromisoformat(status)
        curr = now()
        diff = curr - start
        readable_diff = to_readable_td(diff)
        status_text = f"You have been renting {user_data['bike_name']} for {readable_diff}."
        deduction = calc_deduct(diff)
        status_text += (
            f"\n\nCREDITS:"
            f"\nCurrent: {user_data['credits']}"
            f"\nThis trip: {deduction}"
            f"\nProjected final: {user_data['credits'] - deduction}"
        )
        context.bot.send_message(
            chat_id=chat_id,
            text=status_text)
        context.bot.send_message(
            chat_id=chat_id,
            text="Please remember to /return your bike! Check your bike status with /status.")
