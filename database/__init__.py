import database.controller as db

from admin import (
    ADMIN_HEAD,
)
from text.bot_text import (
    BAN_MESSAGE,
    START_MESSAGE,
)


def check_user(update, context):
    """Check if user is registered, and not banned."""
    user_data = get_user(update, context)
    if user_data is None:
        update.effective_chat.send_message(START_MESSAGE)
        return False
    if user_data.get('is_ban'):
        update.effective_chat.send_message(BAN_MESSAGE.format(**{
            'ADMIN_HEAD': ADMIN_HEAD
        }))
        return False
    return True

def get_user(update=None, context=None, username=None) -> dict or None:
    """Gets the user data."""
    if username is not None:
        chat_id = get_user_id(username)
        if chat_id is None:
            return None
    else:
        chat_id = update.effective_chat.id
    user_data = db.get_user_data(chat_id)
    return user_data

def update_user(user_data):
    chat_id = user_data.get('chat_id', None)
    if not chat_id:
        return None
    db.set_user_data(chat_id, user_data)

def get_user_id(username) -> int:
    return db.get_username(username)

def update_user_id(username, chat_id):
    db.set_username(username, chat_id)

def get_bikes() -> dict:
    return db.get_all_bikes()

def get_bike(bike_name) -> dict:
    return db.get_bike_data(bike_name)

def update_bike(bike_data) -> None:
    bike_name = bike_data['name']
    if not bike_name:
        return
    db.set_bike_data(bike_name, bike_data)
