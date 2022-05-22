from datetime import datetime
import logging

from telegram.ext import (
    CommandHandler,
)

from database import (
    check_user,
    get_bike,
    get_bikes,
    get_user,
    update_user,
    update_user_id,
)
from utils.functions import (
    calc_deduct,
)
from utils.time import (
    now,
    to_readable_td,
)
from utils.decorators import send_typing_action

from admin import (
    ADMIN_LIST,
    BOT_ENV,
)

from text.bot_text import HELP_TEXT
from text.others import (
    EMOJI,
    GUIDE_PIC,
)


logger = logging.getLogger()

def start_command(update, context):
    """Initializes the bot
    This is where we initialize a new user
    If the user is not created, a new entry is created
    in the database with primary key as chat_id
    """
    chat_id = update.effective_chat.id

    if BOT_ENV != 'production' and chat_id not in ADMIN_LIST:
        update.message.reply_text(f"Hi {update.message.from_user.first_name}, please head over to @orc4bikes_bot!")
        return

    if chat_id < 0:  # Telegram groups have negative chat ids
        update.message.reply_text(
            f"Hi @{update.message.from_user.username}, please start the bot privately, and not in groups!!")
        return
    user_data = get_user(update, context)
    if user_data is not None:
        text = f"Welcome back, {update.message.from_user.first_name}! "
    else:
        user_data = {
            'chat_id': chat_id,
            'first_name': update.message.from_user.first_name,
            'last_name': update.message.from_user.last_name,
            'username': update.message.from_user.username,
            'credits': 0,
            'finance': [],
            'log': [],
            'bike_name': '',
            'status': None,
        }
        update_user(user_data)
        text = f"Hello, {update.message.from_user.first_name}! "

    text += (
        "This is your orc4bikes friendly neighbourhood bot :)"
        "\n"
        "\nFor available commands, send /help"
        "\nTo use our bikes, /topup now!"
    )

    update.message.reply_text(text)

    if update.effective_chat.id > 0:
        username = update.message.from_user.username
        if username:
            update_user_id(username, update.effective_chat.id)

def help_command(update, context):
    """Show a list of possible commands"""
    update.message.reply_text(HELP_TEXT)

def guide_command(update, context):
    """Shows you guide to renting bike"""
    update.message.reply_photo(
        photo=GUIDE_PIC,
        caption="Here's the guide! Do you want to /rent?")

@send_typing_action
def history_command(update, context):
    """Shows past 10 transaction history"""
    if not check_user(update, context):
        return -1
    user_data = get_user(update, context)
    data = user_data.get('finance', [])[-10:]  # get the last 10 transactions
    if not data:
        update.message.reply_text(
            "You haven't cycled with us before :( Send /rent to start renting now!")
        return

    text = f"Your past {len(data)} transaction history are as follows:\n"
    for i, line in enumerate(data, 1):
        text += '\n'
        if line['type'] == 'admin':
            text += (
                f"--: An admin {'added' if line['change'] >= 0 else 'deducted'} {line['change']} credits on {line['time']}."
                f" You now have {line['final']} credits."
            )
        elif line['type'] == 'payment':
            text += (
                f"--: You topped up {line['change']} credits on {line['time']}."
                f" You now have {line['final']} credits."
            )
        elif line['type'] == 'rental':
            text += (
                f"--: You rented a bike on {line['time']}, and spent {line['spent']} credits."
                f" You now have {line['remaining']} credits."
            )
    update.message.reply_text(text)

@send_typing_action
def bikes_command(update, context):
    """Show all available bikes. Used in /rent"""
    bikes_data = get_bikes()
    avail, not_avail = [], []
    for bike in bikes_data:
        if not bike['status']:
            avail.append(bike)
        else:
            not_avail.append(bike)

    avail_text = '\n'.join(f"{b['name']} {EMOJI['tick']}" for b in avail)
    not_avail_text = '\n'.join(f"{b['name']} {EMOJI['cross']} -- {'on rent' if b['username'] else b['status']}" for b in not_avail)
    action_text = "To start your journey, send /rent"
    text = '\n\n'.join(["<b>Bicycles:</b>", avail_text, not_avail_text, action_text])

    update.message.reply_html(text)

@send_typing_action
def status_command(update, context):
    """Check the user rental status and current credits"""
    if not check_user(update, context):
        return -1
    user_data = get_user(update, context)

    status = user_data.get('status', None)
    if status is not None:
        status = datetime.fromisoformat(status)
        curr = now()
        diff = curr - status
        readable_diff = to_readable_td(diff)
        status_text = f"You have been renting {user_data['bike_name']} for {readable_diff}. "
        deduction = calc_deduct(diff)
        status_text += (
            f"\n\nCREDITS:"
            f"\nCurrent: {user_data['credits']}"
            f"\nThis trip: {deduction}"
            f"\nProjected final: {user_data['credits'] - deduction}"
        )
    else:
        creds = user_data.get('credits', 0)
        status_text = f"You are not renting...\n\nYou have {creds} credits left. Would you like to /topup?"
        if creds < 100:
            status_text += " Please top up soon!"
    status_text += "\n\nFor more details, send /history."
    status_text += "\nTo start your journey, send /rent."
    update.message.reply_text(status_text)

@send_typing_action
def getpin_command(update, context):
    """Gets pin of current renting bike.
    Not available if not renting
    """
    if not check_user(update, context):
        return -1
    user_data = get_user(update, context)
    bike_name = user_data.get('bike_name', None)
    if not bike_name:
        update.message.reply_text(
            "You are not renting... Start /rent to get the pin for a bike!")
        return

    bike_data = get_bike(bike_name)
    pin = bike_data['pin']
    update.message.reply_text(
        f"Your bike pin is {pin}! Please do not share this pin..."
        " Can't unlock? Please contact one of the admins!")

# User related commands
start_command_handler = CommandHandler('start', start_command)
help_command_handler = CommandHandler('help', help_command)
guide_command_handler = CommandHandler('guide', guide_command)
history_command_handler = CommandHandler('history', history_command)

# Bike related commands
bikes_command_handler = CommandHandler('bikes', bikes_command)
status_command_handler = CommandHandler('status', status_command)
getpin_command_handler = CommandHandler('getpin', getpin_command)

user_command_handlers = [
    start_command_handler,
    help_command_handler,
    guide_command_handler,
    history_command_handler,
    bikes_command_handler,
    status_command_handler,
    getpin_command_handler,
]
