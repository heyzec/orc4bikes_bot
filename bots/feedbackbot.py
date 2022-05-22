import requests

from telegram import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
)
from telegram.ext import (
    CallbackQueryHandler,
    CommandHandler,
    ConversationHandler,
    Filters,
    MessageHandler,
)

from bots.telebot import (
    get_user,
    update_user,
)
from functions import now

from admin import (
    LOGGING_URL,
)

def save_feedback(feedback_data, filename=None):
    requests.post(f"{LOGGING_URL}?file=feedback", json=list(feedback_data.values()))

def whichevent(update, context):
    questiontext = (
        "A penny for your thoughts! You get one credit for doing this feedback :)"
        "\nWhich of the events did you participate in?"
        "\nPress /cancel if you entered this feedback function accidentally."
    )
    keyboard = [
        [
            InlineKeyboardButton("One-North 15 Aug", callback_data="One-North 15 Aug"),
            InlineKeyboardButton("uTown 18 Aug", callback_data="uTown 18 Aug")
        ], [
            InlineKeyboardButton("Holland 25 Aug", callback_data="Holland 25 Aug"),
            InlineKeyboardButton("IKEA 17 Sep", callback_data="IKEA 17 Sep")
        ], [
            InlineKeyboardButton("Marina Bay 21 Sep", callback_data="Marina Bay 21 Sep"),
            InlineKeyboardButton("Jurong Lakes 22 Sep", callback_data="Jurong Lakes 22 Sep"),
        ], [
            InlineKeyboardButton("Kent Ridge 6 Oct", callback_data="Kent Ridge 6 Oct"),
            InlineKeyboardButton("Quarry 19 Oct", callback_data="Quarry 19 Oct")
        ], [
            InlineKeyboardButton("Haw Par Villa 27 Oct", callback_data="Haw Par Villa 27 Oct")
        ],
    ]
    update.message.reply_text(
        questiontext,
        reply_markup=InlineKeyboardMarkup(keyboard))
    context.user_data['feedback_data'] = {
        'user': None,
        'time': None
    }
    return 101

def whichevent_button(update, context):
    query = update.callback_query
    if query is not None:
        query.answer()
        whicheventinput = query.data
        query.edit_message_text(text=f"Event: {query.data}")
        context.user_data['feedback_data']['event'] = whicheventinput

        question_text = "On a scale of 0-10 (10 being the best), how do you feel about this event?"
        query.message.reply_text(question_text)
        return 102

def eventrank(update, context):
    rank = update.message.text
    if rank not in [str(i) for i in range(1, 11)]:
        reply = "Please send a number from 0 to 10!"
        update.message.reply_text(reply)
        return 102

    update.message.reply_text(f"Event rating: {rank}")
    context.user_data['feedback_data']['rating'] = rank
    question_text = "The length of the event was"
    keyboard = [
        [InlineKeyboardButton("Too short", callback_data="Too short")],
        [InlineKeyboardButton("Just nice", callback_data="Just nice")],
        [InlineKeyboardButton("Too long", callback_data="Too long")],
    ]
    update.message.reply_text(
        question_text,
        reply_markup=InlineKeyboardMarkup(keyboard))
    return 103

def eventlength_button(update, context):
    query = update.callback_query
    query.answer()
    query.edit_message_text(text=f"Event length: {query.data}")
    context.user_data['feedback_data']['length'] = query.data

    question_text = "The difficulty of the route was"
    keyboard = [
        [InlineKeyboardButton("Easy", callback_data="Easy")],
        [InlineKeyboardButton("Okay", callback_data="Okay")],
        [InlineKeyboardButton("Hard", callback_data="Hard")],
    ]

    query.message.reply_text(
        question_text,
        reply_markup=InlineKeyboardMarkup(keyboard))
    return 104

def eventdifficulty_button(update, context):
    query = update.callback_query
    query.answer()
    query.edit_message_text(text=f"Route difficulty: {query.data}")
    context.user_data['feedback_data']['difficulty'] = query.data

    question_text = "The pace of the route was"
    keyboard = [
        [InlineKeyboardButton("Easy", callback_data="Easy")],
        [InlineKeyboardButton("Okay", callback_data="Okay")],
        [InlineKeyboardButton("Hard", callback_data="Hard")],
    ]

    query.message.reply_text(
        question_text,
        reply_markup=InlineKeyboardMarkup(keyboard))
    return 105

def eventpace_button(update, context):
    query = update.callback_query
    query.answer()
    query.edit_message_text(text=f"Pace of route: {query.data}")
    context.user_data['feedback_data']['pace'] = query.data

    question_text = (
        "If you rented a bike: On a scale of 1-10 (10 being the best),"
        "how serviceable was the bike provided by orc4bikes?"
    )

    query.message.reply_text(question_text)
    return 106

def bikeservice(update, context):
    rank = update.message.text
    if rank not in [str(i) for i in range(1, 11)]:
        update.message.reply_text("Please send a number from 0 to 10!")
        return 106

    update.message.reply_text(f"Bike servicing rating: {rank}")
    context.user_data['feedback_data']['servicing'] = rank
    update.message.reply_text(
        "Do you have any places that you want orc4bike to head to in the next event?"
        "If none, please send NIL")
    return 107

def placetogo(update, context):
    rank = update.message.text  # saving the response?
    update.message.reply_text(f"Other places to go: {rank}")
    context.user_data['feedback_data']['other_places'] = rank

    update.message.reply_text(
        "Do you have any other feedback, suggestions, area of improvement?")
    return 108

def other(update, context):
    rank = update.message.text  # saving the response?
    update.message.reply_text("Other feedback: " + rank)
    context.user_data['feedback_data']['other_feedback'] = rank

    update.message.reply_text(
        "Feedback captured. Thank you for your time!")

    context.user_data['feedback_data']['user'] = update.message.from_user.username
    context.user_data['feedback_data']['time'] = now().strftime(
        "%Y.%m.%d,%H.%M.%S")
    save_feedback(feedback_data=context.user_data['feedback_data'])

    user_data = get_user(username=update.message.from_user.username)
    if user_data is not None:
        user_data["credits"] += 1
        update_user(user_data)
        update.message.reply_text(
            "One penny has been given for your thoughts!"
            f"You now have {user_data['credits']} credits.")

    return -1


feedback_conversation = ConversationHandler(
    entry_points = [
        CommandHandler('feedback', whichevent),
    ],
    states = {
        101: [CallbackQueryHandler(whichevent_button)],
        102: [MessageHandler(filters=Filters.text, callback=eventrank)],
        103: [CallbackQueryHandler(eventlength_button)],
        104: [CallbackQueryHandler(eventdifficulty_button)],
        105: [CallbackQueryHandler(eventpace_button)],
        106: [MessageHandler(filters=Filters.text, callback=bikeservice)],
        107: [MessageHandler(filters=Filters.text, callback=placetogo)],
        108: [MessageHandler(filters=Filters.text, callback=other)],
    },
    fallbacks=[]
)
