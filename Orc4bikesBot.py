from datetime import timedelta
import logging

from telegram.ext import (
    CallbackQueryHandler,
    CommandHandler,
    Filters,
    MessageHandler,
    Updater,
)

from bots import all_handlers
from bots.reminder import reminder

from admin import (
    TELE_API_TOKEN,
)

logger = logging.getLogger()

def echo_command(update, context):
    update.message.reply_text(update.message.text)

def convo_outside_command(update, context):
    """Inform user when update occurs outside of a ConversationHandler."""
    update.message.reply_text("This command was a little out of place...")
    context.user_data.clear()
    return -1

def dummy_command(update, context):
    update.message.reply_text("This feature will be added soon! Where art thou, bikes...?")

def unrecognized_command(update, context):
    """Inform user when command is unrecognized."""
    update.message.reply_text("Unrecognized command. Send /help for available commands.")

def unrecognized_buttons(update, context):
    """Edit query so the user knows button is not accepted."""
    query = update.callback_query
    query.answer()
    query.edit_message_text(
        f"{query.message.text_html}"
        "\n\n<i>Sorry, this button has expired. Please send the previous command again.</i>",
        parse_mode='HTML')

def err(update, context):
    """Error handler callback for dispatcher."""
    error = context.error
    logger.exception(error)
    if update is not None and update.effective_user is not None:
        update.effective_chat.send_message(
            "I'm sorry, an error has occurred. The devs have been alerted!")

def main():
    updater = Updater(token=TELE_API_TOKEN, use_context=True)
    dispatcher = updater.dispatcher

    for handler in all_handlers:
        dispatcher.add_handler(handler)

    # Check if user sends converation commands outside of ConversationHandler (ConvoBot)
    dispatcher.add_handler(CommandHandler('cancel', convo_outside_command))
    dispatcher.add_handler(CommandHandler('done', convo_outside_command))

    # Lastly, Filters all unknown commands, and remove unrecognized queries
    dispatcher.add_handler(MessageHandler(Filters.command, unrecognized_command))
    dispatcher.add_handler(CallbackQueryHandler(unrecognized_buttons))

    # Schedule reminder to be run
    job_queue = updater.job_queue
    logger.debug('getting daily queue')
    job_queue.run_repeating(
        callback=reminder,
        interval=timedelta(hours=1))

    dispatcher.add_error_handler(err)
    logger.info("Initializing bot...")
    updater.start_polling()
    updater.idle()
